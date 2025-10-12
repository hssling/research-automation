"""
Research Automation Pipeline Orchestrator
A modular framework for managing and executing research workflows
"""

import os
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
import importlib.util
import subprocess
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PipelineStep:
    """Represents a single step in a research pipeline"""
    name: str
    description: str
    script_path: str
    dependencies: List[str]
    inputs: Dict[str, Any]
    outputs: List[str]
    validators: List[str]
    retry_count: int = 0
    max_retries: int = 3

@dataclass
class PipelineConfig:
    """Configuration for a research pipeline"""
    name: str
    description: str
    version: str
    author: str
    created_date: str
    research_type: str
    steps: List[PipelineStep]
    global_config: Dict[str, Any]

@dataclass
class PipelineResult:
    """Result of pipeline execution"""
    pipeline_name: str
    start_time: datetime
    end_time: datetime
    steps_executed: List[str]
    success: bool
    errors: List[str]
    output_paths: Dict[str, str]

class PipelineOrchestrator:
    """
    Core orchestrator for managing automated research pipelines
    """

    def __init__(self, config_dir: str = "research-automation-core/pipelines"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.active_pipelines: Dict[str, PipelineConfig] = {}
        self.pipeline_results: Dict[str, PipelineResult] = {}

        # Create necessary subdirectories
        (self.config_dir / "configs").mkdir(exist_ok=True)
        (self.config_dir / " results").mkdir(exist_ok=True)
        (self.config_dir / "logs").mkdir(exist_ok=True)

        logger.info("Pipeline Orchestrator initialized")

    def create_pipeline_template(self, name: str, research_type: str) -> str:
        """
        Create a template pipeline configuration for a specific research type

        Args:
            name: Pipeline name
            research_type: Type of research (systematic_review, meta_analysis, etc.)

        Returns:
            Path to created template configuration
        """

        templates = {
            "systematic_review": self._get_systematic_review_template(name),
            "meta_analysis": self._get_meta_analysis_template(name),
            "bibliometrics": self._get_bibliometrics_template(name),
            "omics_single": self._get_omics_template(name),
            "custom": self._get_custom_template(name)
        }

        template = templates.get(research_type, self._get_custom_template(name))

        config_path = self.config_dir / "configs" / f"{name}_pipeline.yaml"

        with open(config_path, 'w') as f:
            yaml.dump(asdict(template), f, default_flow_style=False)

        logger.info(f"Created pipeline template: {config_path}")
        return str(config_path)

    def load_pipeline(self, config_path: str) -> PipelineConfig:
        """
        Load a pipeline configuration from YAML file

        Args:
            config_path: Path to configuration file

        Returns:
            Loaded PipelineConfig object
        """
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)

            # Convert steps to PipelineStep objects
            steps = []
            for step_data in config_data['steps']:
                steps.append(PipelineStep(**step_data))

            config = PipelineConfig(
                name=config_data['name'],
                description=config_data['description'],
                version=config_data['version'],
                author=config_data['author'],
                created_date=config_data['created_date'],
                research_type=config_data['research_type'],
                steps=steps,
                global_config=config_data['global_config']
            )

            self.active_pipelines[config.name] = config
            logger.info(f"Loaded pipeline: {config.name}")
            return config

        except Exception as e:
            logger.error(f"Failed to load pipeline config: {e}")
            raise

    def execute_pipeline(self, pipeline_name: str,
                        working_dir: str = None,
                        dry_run: bool = False) -> PipelineResult:
        """
        Execute a loaded pipeline

        Args:
            pipeline_name: Name of the pipeline to execute
            working_dir: Working directory (defaults to pipeline name dir)
            dry_run: If True, only validate without executing

        Returns:
            PipelineResult object
        """

        if pipeline_name not in self.active_pipelines:
            raise ValueError(f"Pipeline {pipeline_name} not loaded")

        pipeline = self.active_pipelines[pipeline_name]
        start_time = datetime.now()

        working_dir = working_dir or pipeline_name
        working_dir = Path(working_dir)
        working_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Starting pipeline execution: {pipeline_name}")

        executed_steps = []
        errors = []
        output_paths = {}
        success = True

        # Store original directory and change to working directory
        original_dir = os.getcwd()
        os.chdir(working_dir)

        try:
            for step in pipeline.steps:
                logger.info(f"Executing step: {step.name}")

                if dry_run:
                    logger.info(f"Dry run - would execute: {step.description}")
                    executed_steps.append(step.name)
                    continue

                try:
                    self._execute_step(step, pipeline.global_config)
                    executed_steps.append(step.name)
                    logger.info(f"Completed step: {step.name}")
                except Exception as e:
                    error_msg = f"Step {step.name} failed: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)

                    if step.retry_count < step.max_retries:
                        step.retry_count += 1
                        logger.info(f"Retrying step {step.name} (attempt {step.retry_count})")
                        # Retry logic would go here
                    else:
                        success = False
                        break

        except Exception as e:
            success = False
            errors.append(f"Pipeline execution failed: {str(e)}")
            logger.error(f"Pipeline execution failed: {e}")

        end_time = datetime.now()

        result = PipelineResult(
            pipeline_name=pipeline_name,
            start_time=start_time,
            end_time=end_time,
            steps_executed=executed_steps,
            success=success,
            errors=errors,
            output_paths=output_paths
        )

        self.pipeline_results[pipeline_name] = result

        # Save results
        self._save_execution_results(result)

        logger.info(f"Pipeline {pipeline_name} completed. Success: {success}")
        return result

    def _execute_step(self, step: PipelineStep, global_config: Dict[str, Any]):
        """
        Execute a single pipeline step

        Args:
            step: PipelineStep to execute
            global_config: Global pipeline configuration
        """

        script_path = Path(step.script_path)

        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        # Prepare execution environment
        env = os.environ.copy()

        # Add pipeline configuration to environment
        for key, value in global_config.items():
            env[f"PIPELINE_{key.upper()}"] = str(value)

        for key, value in step.inputs.items():
            env[f"STEP_{key.upper()}"] = str(value)

        # Execute based on script type
        if script_path.suffix == '.py':
            cmd = [sys.executable, str(script_path)]
        elif script_path.suffix == '.R':
            cmd = ['Rscript', str(script_path)]
        elif script_path.suffix == '.sh':
            cmd = ['bash', str(script_path)]
        else:
            raise ValueError(f"Unsupported script type: {script_path.suffix}")

        try:
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, cmd, result.stdout, result.stderr
                )

            logger.info(f"Step output: {result.stdout}")

        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Step {step.name} timed out after 5 minutes")

        # Run validators if specified
        for validator in step.validators:
            self._run_validator(validator, step.outputs)

    def _run_validator(self, validator_name: str, expected_outputs: List[str]):
        """
        Run a validation function for step outputs

        Args:
            validator_name: Name of validator function
            expected_outputs: List of expected output files
        """
        logger.info(f"Running validator: {validator_name}")

        # Validation logic would be implemented based on validator type
        # For now, just check file existence
        for output in expected_outputs:
            if not Path(output).exists():
                logger.warning(f"Expected output not found: {output}")

    def _save_execution_results(self, result: PipelineResult):
        """Save pipeline execution results to file"""
        results_dir = self.config_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        results_file = results_dir / f"{result.pipeline_name}_result_{result.start_time.strftime('%Y%m%d_%H%M%S')}.json"

        with open(results_file, 'w') as f:
            json.dump({
                'pipeline_name': result.pipeline_name,
                'start_time': result.start_time.isoformat(),
                'end_time': result.end_time.isoformat(),
                'steps_executed': result.steps_executed,
                'success': result.success,
                'errors': result.errors,
                'output_paths': result.output_paths
            }, f, indent=2)

        logger.info(f"Saved execution results: {results_file}")

    def _get_systematic_review_template(self, name: str) -> PipelineConfig:
        """Get template for systematic review pipeline"""
        return PipelineConfig(
            name=name,
            description=f"Systematic review pipeline for {name}",
            version="1.0.0",
            author="Research Automation System",
            created_date=datetime.now().isoformat(),
            research_type="systematic_review",
            steps=[
                PipelineStep(
                    name="literature_search",
                    description="Search PubMed and other databases",
                    script_path="scripts/pubmed_search.py",
                    dependencies=[],
                    inputs={"search_terms": "", "databases": "pubmed,cochrane"},
                    outputs=["data/pubmed_search_results.csv"],
                    validators=["check_search_results"]
                ),
                PipelineStep(
                    name="deduplication",
                    description="Remove duplicate studies",
                    script_path="scripts/deduplication.py",
                    dependencies=["literature_search"],
                    inputs={"input_file": "data/pubmed_search_results.csv"},
                    outputs=["data/deduplicated_studies.csv"],
                    validators=["check_duplicates_removed"]
                ),
                PipelineStep(
                    name="screening",
                    description="Title and abstract screening",
                    script_path="scripts/screening.py",
                    dependencies=["deduplication"],
                    inputs={"input_file": "data/deduplicated_studies.csv"},
                    outputs=["data/screened_studies.csv"],
                    validators=["check_screening_complete"]
                )
            ],
            global_config={"working_dir": "data", "log_level": "INFO"}
        )

    def _get_meta_analysis_template(self, name: str) -> PipelineConfig:
        """Get template for meta-analysis pipeline"""
        return PipelineConfig(
            name=name,
            description=f"Meta-analysis pipeline for {name}",
            version="1.0.0",
            author="Research Automation System",
            created_date=datetime.now().isoformat(),
            research_type="meta_analysis",
            steps=[
                PipelineStep(
                    name="data_extraction",
                    description="Extract data from included studies",
                    script_path="scripts/data_extraction.py",
                    dependencies=[],
                    inputs={"studies_file": "data/screened_studies.csv"},
                    outputs=["data/extracted_data.csv"],
                    validators=["check_data_extraction"]
                ),
                PipelineStep(
                    name="meta_analysis",
                    description="Perform meta-analysis calculations",
                    script_path="scripts/meta_analysis.py",
                    dependencies=["data_extraction"],
                    inputs={"data_file": "data/extracted_data.csv"},
                    outputs=["results/meta_analysis_results.json"],
                    validators=["check_meta_analysis"]
                ),
                PipelineStep(
                    name="visualization",
                    description="Generate forest plots and figures",
                    script_path="scripts/plot_generator.py",
                    dependencies=["meta_analysis"],
                    inputs={"results_file": "results/meta_analysis_results.json"},
                    outputs=["results/forest_plot.png", "results/funnel_plot.png"],
                    validators=["check_plots_generated"]
                )
            ],
            global_config={"working_dir": "data", "analysis_type": "fixed_effects"}
        )

    def _get_bibliometrics_template(self, name: str) -> PipelineConfig:
        """Get template for bibliometrics analysis pipeline"""
        return PipelineConfig(
            name=name,
            description=f"Bibliometric analysis pipeline for {name}",
            version="1.0.0",
            author="Research Automation System",
            created_date=datetime.now().isoformat(),
            research_type="bibliometrics",
            steps=[
                PipelineStep(
                    name="citation_analysis",
                    description="Analyze citation networks",
                    script_path="scripts/bibliometric_analysis.py",
                    dependencies=[],
                    inputs={"literature_file": "data/comprehensive_literature.csv"},
                    outputs=["results/citation_network.json"],
                    validators=["check_citation_data"]
                ),
                PipelineStep(
                    name="co_authorship_analysis",
                    description="Analyze collaboration patterns",
                    script_path="scripts/coauthorship_analysis.py",
                    dependencies=["citation_analysis"],
                    inputs={"network_file": "results/citation_network.json"},
                    outputs=["results/collaboration_network.png"],
                    validators=["check_collaboration_viz"]
                )
            ],
            global_config={"working_dir": "data", "analysis_scope": "comprehensive"}
        )

    def _get_omics_template(self, name: str) -> PipelineConfig:
        """Get template for omics analysis pipeline"""
        return PipelineConfig(
            name=name,
            description=f"Omics analysis pipeline for {name}",
            version="1.0.0",
            author="Research Automation System",
            created_date=datetime.now().isoformat(),
            research_type="omics_single",
            steps=[
                PipelineStep(
                    name="data_preprocessing",
                    description="Preprocess omics data",
                    script_path="scripts/omics_preprocessing.py",
                    dependencies=[],
                    inputs={"raw_data_dir": "data/omics_raw"},
                    outputs=["data/processed_omics.rda"],
                    validators=["check_preprocessing_qc"]
                ),
                PipelineStep(
                    name="differential_expression",
                    description="Perform differential expression analysis",
                    script_path="scripts/de_analysis.R",
                    dependencies=["data_preprocessing"],
                    inputs={"processed_data": "data/processed_omics.rda"},
                    outputs=["results/de_results.csv"],
                    validators=["check_de_significance"]
                ),
                PipelineStep(
                    name="pathway_analysis",
                    description="Perform pathway enrichment analysis",
                    script_path="scripts/pathway_analysis.R",
                    dependencies=["differential_expression"],
                    inputs={"de_results": "results/de_results.csv"},
                    outputs=["results/pathway_enrichment.csv"],
                    validators=["check_pathway_results"]
                )
            ],
            global_config={"working_dir": "data", "organism": "human", "p_value_threshold": "0.05"}
        )

    def _get_custom_template(self, name: str) -> PipelineConfig:
        """Get basic custom pipeline template"""
        return PipelineConfig(
            name=name,
            description=f"Custom research pipeline for {name}",
            version="1.0.0",
            author="Research Automation System",
            created_date=datetime.now().isoformat(),
            research_type="custom",
            steps=[
                PipelineStep(
                    name="init",
                    description="Initialize research project",
                    script_path="scripts/init_project.py",
                    dependencies=[],
                    inputs={},
                    outputs=["project_config.yaml"],
                    validators=["check_project_init"]
                )
            ],
            global_config={"working_dir": "data", "custom_config": True}
        )


def main():
    """Main function for command line usage"""

    import argparse

    parser = argparse.ArgumentParser(description="Research Automation Pipeline Orchestrator")
    parser.add_argument("action", choices=[
        "create", "load", "execute", "run", "list"
    ])
    parser.add_argument("--name", help="Pipeline name")
    parser.add_argument("--type", help="Research type for new pipelines")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--workdir", help="Working directory for execution")
    parser.add_argument("--dry-run", action="store_true", help="Validate without executing")

    args = parser.parse_args()

    orchestrator = PipelineOrchestrator()

    if args.action == "create":
        if not args.name:
            parser.error("--name required for create action")
        if not args.type:
            args.type = "custom"

        config_path = orchestrator.create_pipeline_template(args.name, args.type)
        print(f"Created pipeline template: {config_path}")

    elif args.action == "load":
        if not args.config:
            parser.error("--config required for load action")

        pipeline = orchestrator.load_pipeline(args.config)
        print(f"Loaded pipeline: {pipeline.name}")

    elif args.action == "execute":
        if not args.name:
            parser.error("--name required for execute action")

        result = orchestrator.execute_pipeline(
            args.name,
            working_dir=args.workdir,
            dry_run=args.dry_run
        )

        print(f"Pipeline execution completed: {result.success}")
        if not result.success:
            print("Errors:", result.errors)

    elif args.action == "run":
        if not args.config:
            parser.error("--config required for run action")
        if not args.name:
            parser.error("--name required for run action")

        # Load and then execute
        pipeline = orchestrator.load_pipeline(args.config)
        print(f"Loaded pipeline: {pipeline.name}")

        result = orchestrator.execute_pipeline(
            args.name,
            working_dir=args.workdir,
            dry_run=args.dry_run
        )

        print(f"Pipeline execution completed: {result.success}")
        if not result.success:
            print("Errors:", result.errors)

    elif args.action == "list":
        print("Available pipeline types:")
        print("- systematic_review")
        print("- meta_analysis")
        print("- bibliometrics")
        print("- omics_single")
        print("- custom")


if __name__ == "__main__":
    main()
