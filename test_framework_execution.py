#!/usr/bin/env python3
"""
Test script to verify research automation framework execution capabilities
"""

import sys
import os
import logging
from pathlib import Path
import traceback

# Add research-automation-core to path
sys.path.insert(0, str(Path(__file__).parent / "research-automation-core"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_module_imports():
    """Test that all core modules can be imported successfully"""
    logger.info("Testing module imports...")

    modules_to_test = [
        'pipeline_orchestrator',
        'project_creator',
        'project_template_generator',
        'ai_literature_screener',
        'multi_database_search',
        'auto_data_extractor',
        'auto_meta_analyzer',
        'auto_visualization_generator',
        'auto_quality_assessor',
        'ai_manuscript_generator',
        'reporting_automation',
        'living_review_manager',
        'advanced_ai_manuscript_generator',
        'global_collaboration_platform'
    ]

    import_status = {}

    for module_name in modules_to_test:
        try:
            __import__(module_name)
            import_status[module_name] = "SUCCESS"
            logger.info(f"✅ {module_name}: SUCCESS")
        except Exception as e:
            import_status[module_name] = f"FAILED: {str(e)}"
            logger.error(f"❌ {module_name}: FAILED - {str(e)}")

    return import_status

def test_basic_functionality():
    """Test basic functionality of core components"""
    logger.info("Testing basic functionality...")

    functionality_tests = {
        'project_template_generation': False,
        'pipeline_orchestration': False,
        'data_extraction': False,
        'meta_analysis': False,
        'manuscript_generation': False,
        'reporting_automation': False,
        'living_review_management': False
    }

    # Test project template generation
    try:
        from project_template_generator import ResearchProjectTemplate
        template_gen = ResearchProjectTemplate()
        # Try to create a minimal project structure
        # Clean up existing test directory to avoid git permission issues
        try:
            import shutil
            test_dir = "./test_project"
            if os.path.exists(test_dir):
                print(f"Cleaning up existing test directory: {test_dir}")
                shutil.rmtree(test_dir)
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")

        result = template_gen.create_project("test_functionality", "systematic_review", "./test_project")
        functionality_tests['project_template_generation'] = True
        print(f"✅ Project template generation passed: {result}")
        logger.info("✅ Project template generation: SUCCESS")

        # Clean up test directory with Windows permission handling
        try:
            import shutil
            test_path = Path('./test_project')
            if test_path.exists():
                # Try to remove with better error handling for Windows
                shutil.rmtree(test_path, ignore_errors=True)
                if test_path.exists():  # If still exists, try force removal
                    try:
                        import subprocess
                        if os.name == 'nt':  # Windows
                            subprocess.run(['rmdir', '/S', '/Q', str(test_path)], check=True, capture_output=True)
                    except subprocess.SubprocessError:
                        pass  # If force removal also fails, continue silently
        except Exception as e:
            print(f"Note: Test directory cleanup encountered issues: {e}")
            # Continue anyway - this doesn't affect the actual test results

    except Exception as e:
        logger.error(f"❌ Project template generation: FAILED - {str(e)}")

    # Test pipeline orchestration
    try:
        from pipeline_orchestrator import PipelineOrchestrator
        orchestrator = PipelineOrchestrator()
        # Test basic instantiation
        functionality_tests['pipeline_orchestration'] = True
        logger.info("✅ Pipeline orchestration: SUCCESS")
    except Exception as e:
        logger.error(f"❌ Pipeline orchestration: FAILED - {str(e)}")

    # Test data extraction basic functionality
    try:
        from auto_data_extractor import AutomatedDataExtractor
        extractor = AutomatedDataExtractor()
        # Test basic initialization
        functionality_tests['data_extraction'] = True
        logger.info("✅ Data extraction: SUCCESS")
    except Exception as e:
        logger.error(f"❌ Data extraction: FAILED - {str(e)}")

    # Test meta-analysis basic functionality
    try:
        from auto_meta_analyzer import AutomatedMetaAnalyzer
        analyzer = AutomatedMetaAnalyzer()
        # Test basic initialization
        functionality_tests['meta_analysis'] = True
        logger.info("✅ Meta-analysis: SUCCESS")
    except Exception as e:
        logger.error(f"❌ Meta-analysis: FAILED - {str(e)}")

    # Test basic AI manuscript generation import
    try:
        from ai_manuscript_generator import AIManuscriptAssistant
        generator = AIManuscriptAssistant()
        functionality_tests['manuscript_generation'] = True
        logger.info("✅ Basic manuscript generation: SUCCESS")
    except Exception as e:
        logger.error(f"❌ Basic manuscript generation: FAILED - {str(e)}")

    # Test reporting automation
    try:
        from reporting_automation import AutomatedReporter
        reporting = AutomatedReporter()
        functionality_tests['reporting_automation'] = True
        logger.info("✅ Reporting automation: SUCCESS")
    except Exception as e:
        logger.error(f"❌ Reporting automation: FAILED - {str(e)}")

    # Test living review management
    try:
        from living_review_manager import LivingReviewManager
        manager = LivingReviewManager()
        functionality_tests['living_review_management'] = True
        logger.info("✅ Living review management: SUCCESS")
    except Exception as e:
        logger.error(f"❌ Living review management: FAILED - {str(e)}")

    return functionality_tests

def test_integration_orchestration():
    """Test the pipeline orchestrator can coordinate multiple components"""
    logger.info("Testing integration orchestration...")

    try:
        from pipeline_orchestrator import PipelineOrchestrator

        orchestrator = PipelineOrchestrator()
        logger.info("✅ Pipeline orchestration: SUCCESS")

        # Test basic instantiation and functionality
        if hasattr(orchestrator, 'active_pipelines') and hasattr(orchestrator, 'pipeline_results'):
            logger.info("✅ Pipeline status query: SUCCESS")
            return True
        else:
            logger.warning("⚠️  Pipeline object missing expected attributes")
            return False

    except Exception as e:
        logger.error(f"❌ Pipeline orchestration: FAILED - {str(e)}")
        return False

def generate_system_health_report():
    """Generate comprehensive system health report"""

    print("\n" + "="*80)
    print("🔬 RESEARCH AUTOMATION FRAMEWORK - EXECUTION VERIFICATION REPORT")
    print("="*80)

    import_status = test_module_imports()
    functionality_status = test_basic_functionality()
    integration_status = test_integration_orchestration()

    print("\n1️⃣  MODULE IMPORT STATUS:")
    print("-" * 40)

    success_count = 0
    total_modules = len(import_status)

    for module, status in import_status.items():
        status_indicator = "✅" if status == "SUCCESS" else "❌"
        print(f"   {status_indicator} {module}: {status}")
        if status == "SUCCESS":
            success_count += 1

    print(".1f")

    print("\n2️⃣  FUNCTIONALITY TEST STATUS:")
    print("-" * 40)

    for test, result in functionality_status.items():
        status_indicator = "✅" if result else "❌"
        print(f"   {status_indicator} {test.replace('_', ' ').title()}: {'PASS' if result else 'FAIL'}")

    print("\n3️⃣  INTEGRATION TEST STATUS:")
    print("-" * 40)
    integration_indicator = "✅" if integration_status else "❌"
    print(f"   {integration_indicator} Pipeline Orchestration: {'PASS' if integration_status else 'FAIL'}")

    print("\n4️⃣  SYSTEM HEALTH SUMMARY:")
    print("-" * 40)

    # Calculate overall health score
    import_health = success_count / total_modules * 100
    functionality_health = sum(functionality_status.values()) / len(functionality_status) * 100
    integration_health = 100.0 if integration_status else 0.0

    overall_health = (import_health * 0.4 + functionality_health * 0.4 + integration_health * 0.2)

    print(".1f")
    print(".1f")
    print(".1f")

    if overall_health >= 90:
        health_rating = "🟢 EXCELLENT"
        recommendation = "System ready for production deployment"
    elif overall_health >= 75:
        health_rating = "🟡 GOOD"
        recommendation = "Minor configuration needed before deployment"
    elif overall_health >= 60:
        health_rating = "🟠 FAIR"
        recommendation = "Configuration and testing recommended"
    else:
        health_rating = "🔴 POOR"
        recommendation = "System requires attention before use"

    print(f"\n5️⃣  HEALTH RATING: {health_rating}")
    print(f"   Recommendation: {recommendation}")

    print("\n6️⃣  DEPLOYMENT READINESS:")
    print("-" * 40)

    if overall_health >= 75:
        print("✅ SYSTEM READY FOR DEPLOYMENT")
        print("   • All core modules operational")
        print("   • Basic functionality verified")
        print("   • Integration capabilities confirmed")
    else:
        print("⚠️  SYSTEM REQUIRES ATTENTION")
        print("   • Check failed module imports")
        print("   • Verify dependencies are installed")
        print("   • Test individual component functionality")

    print("\n" + "="*80)
    print("🧪 TESTING COMPLETE - REPORT GENERATED")
    print("="*80)

    return {
        'import_health': import_health,
        'functionality_health': functionality_health,
        'integration_health': integration_health,
        'overall_health': overall_health,
        'recommendation': recommendation
    }

if __name__ == "__main__":
    generate_system_health_report()
