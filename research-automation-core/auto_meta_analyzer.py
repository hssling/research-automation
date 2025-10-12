"""
Automated Meta-Analysis System
Statistical synthesis and analysis for systematic reviews and meta-analyses
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.meta_analysis import (
    combine_effects, effectsize_smd, effectsize_2proportions
)
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EffectSizeCalculator:
    """Calculate effect sizes for different outcome types"""

    @staticmethod
    def cohen_d(intervention_mean: float, control_mean: float,
                intervention_sd: float, control_sd: float,
                intervention_n: int, control_n: int) -> Tuple[float, float]:
        """Calculate Cohen's d effect size"""

        # Calculate pooled standard deviation
        pooled_sd = np.sqrt(((intervention_n - 1) * intervention_sd**2 +
                           (control_n - 1) * control_sd**2) /
                          (intervention_n + control_n - 2))

        # Calculate Cohen's d
        d = (intervention_mean - control_mean) / pooled_sd

        # Calculate standard error
        se = np.sqrt((intervention_n + control_n) / (intervention_n * control_n) +
                    d**2 / (2 * (intervention_n + control_n)))

        return d, se

    @staticmethod
    def odds_ratio(events_intervention: int, total_intervention: int,
                  events_control: int, total_control: int) -> Tuple[float, float]:
        """Calculate odds ratio for binary outcomes"""

        # Add continuity correction if needed
        if events_intervention == 0 or events_control == 0:
            events_intervention += 0.5
            events_control += 0.5
            total_intervention += 1
            total_control += 1

        or_value = ((events_intervention / (total_intervention - events_intervention)) /
                   (events_control / (total_control - events_control)))

        # Standard error calculation
        se = np.sqrt(1/events_intervention + 1/(total_intervention - events_intervention) +
                    1/events_control + 1/(total_control - events_control))

        return or_value, se

    @staticmethod
    def risk_difference(events_intervention: int, total_intervention: int,
                       events_control: int, total_control: int) -> Tuple[float, float]:
        """Calculate risk difference"""

        p1 = events_intervention / total_intervention
        p2 = events_control / total_control

        rd = p1 - p2

        # Standard error
        se = np.sqrt(p1*(1-p1)/total_intervention + p2*(1-p2)/total_control)

        return rd, se


class MetaAnalysisModel:
    """Statistical meta-analysis model with heterogeneity assessment"""

    def __init__(self, effect_sizes: np.ndarray, variances: np.ndarray,
                 study_labels: List[str] = None):
        self.effect_sizes = np.array(effect_sizes)
        self.variances = np.array(variances)
        self.se = np.sqrt(variances)
        self.study_labels = study_labels or [f"Study {i+1}" for i in range(len(effect_sizes))]

        # Initialize results storage
        self.results = {}

    def _tau_squared_estimator(self, method: str = 'DL') -> float:
        """Estimate tau-squared (between-study variance)"""

        if method == 'DL':
            # DerSimonian-Laird estimator
            weights = 1 / self.variances
            weighted_mean = np.sum(weights * self.effect_sizes) / np.sum(weights)

            q = np.sum(weights * (self.effect_sizes - weighted_mean)**2)

            # Degrees of freedom
            df = len(self.effect_sizes) - 1

            # Tau-squared estimate
            if q > df:
                tau2 = (q - df) / (np.sum(weights) - np.sum(weights**2)/np.sum(weights))
                tau2 = max(0, tau2)
            else:
                tau2 = 0

        elif method == 'SJ':
            # Sidik-Jonkman estimator (empirical Bayes)
            # Simplified implementation when statsmodels function unavailable
            # Use a basic empirical Bayes approach
            try:
                # Simple empirical Bayes tau-squared estimator
                var_effects = np.var(self.effect_sizes, ddof=1)
                var_within = np.mean(self.variances)

                if var_effects > var_within and var_within > 0:
                    tau2 = var_effects - var_within
                else:
                    tau2 = max(0, var_effects * 0.1)  # Conservative estimate
            except:
                tau2 = 0

        else:
            tau2 = 0

        return tau2

    def fixed_effects_model(self) -> Dict[str, Any]:
        """Conduct fixed-effects meta-analysis"""

        weights = 1 / self.variances
        sum_weights = np.sum(weights)
        weighted_sum = np.sum(weights * self.effect_sizes)

        # Overall effect
        overall_effect = weighted_sum / sum_weights

        # Standard error of overall effect
        se_overall = 1 / np.sqrt(sum_weights)

        # Z-statistic and p-value
        z_stat = overall_effect / se_overall
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # 95% Confidence interval
        ci_lower = overall_effect - 1.96 * se_overall
        ci_upper = overall_effect + 1.96 * se_overall

        return {
            'method': 'fixed_effects',
            'overall_effect': overall_effect,
            'se': se_overall,
            'z_stat': z_stat,
            'p_value': p_value,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'weights': weights,
            'heterogeneity_test': {'Q': None, 'p_value': None, 'I2': None}  # Not applicable for FE
        }

    def random_effects_model(self, tau_method: str = 'DL') -> Dict[str, Any]:
        """Conduct random-effects meta-analysis"""

        # Estimate tau-squared
        tau2 = self._tau_squared_estimator(tau_method)

        # Adjust variances
        adjusted_variances = self.variances + tau2
        weights = 1 / adjusted_variances
        sum_weights = np.sum(weights)
        weighted_sum = np.sum(weights * self.effect_sizes)

        # Overall effect
        overall_effect = weighted_sum / sum_weights

        # Standard error of overall effect
        se_overall = 1 / np.sqrt(sum_weights)

        # Z-statistic and p-value
        z_stat = overall_effect / se_overall
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # 95% Confidence interval
        ci_lower = overall_effect - 1.96 * se_overall
        ci_upper = overall_effect + 1.96 * se_overall

        # Heterogeneity statistics
        q = np.sum((1 / self.variances) * (self.effect_sizes - overall_effect)**2)
        df = len(self.effect_sizes) - 1

        # Q statistic p-value
        if df > 0:
            q_p_value = 1 - stats.chi2.cdf(q, df)
        else:
            q_p_value = 1.0

        # I-squared
        if q <= df:
            i2 = 0
        else:
            i2 = ((q - df) / q) * 100

        return {
            'method': 'random_effects',
            'tau2': tau2,
            'overall_effect': overall_effect,
            'se': se_overall,
            'z_stat': z_stat,
            'p_value': p_value,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'weights': weights,
            'heterogeneity_test': {
                'Q': q,
                'p_value': q_p_value,
                'I2': i2
            }
        }

    def conduct_analysis(self, method: str = 'auto') -> Dict[str, Any]:
        """Main analysis method"""

        # Always conduct both fixed and random effects
        fe_results = self.fixed_effects_model()
        re_results = self.random_effects_model()

        # Choose primary method based on heterogeneity
        if method == 'auto':
            # Use random effects if significant heterogeneity
            q_p = re_results['heterogeneity_test']['p_value']
            if q_p is not None and q_p < 0.10:  # Significant heterogeneity
                primary_method = 'random_effects'
                primary_results = re_results
            else:
                primary_method = 'fixed_effects'
                primary_results = fe_results
        elif method == 'fixed':
            primary_method = 'fixed_effects'
            primary_results = fe_results
        else:  # 'random'
            primary_method = 'random_effects'
            primary_results = re_results

        return {
            'primary_method': primary_method,
            'primary_results': primary_results,
            'fixed_effects': fe_results,
            'random_effects': re_results,
            'study_effects': {
                'effects': self.effect_sizes.tolist(),
                'variances': self.variances.tolist(),
                'study_labels': self.study_labels
            }
        }


class MetaAnalysisVisualizer:
    """Generate publication-quality meta-analysis plots"""

    def __init__(self, figsize: Tuple[int, int] = (10, 8)):
        self.figsize = figsize
        plt.style.use('seaborn-v0_8-whitegrid')

    def forest_plot(self, analysis_results: Dict[str, Any],
                   title: str = "Forest Plot", save_path: str = None) -> plt.Figure:
        """Generate forest plot"""

        fig, ax = plt.subplots(figsize=self.figsize)

        study_effects = analysis_results['study_effects']['effects']
        study_labels = analysis_results['study_effects']['study_labels']

        # Get results
        primary_results = analysis_results['primary_results']

        # Plot study effects
        y_positions = np.arange(len(study_effects))

        # Study effect sizes with error bars
        study_se = np.sqrt(analysis_results['study_effects']['variances'])
        ax.errorbar(study_effects, y_positions, xerr=1.96*study_se,
                   fmt='s', color='blue', markersize=8, capsize=3)

        # Overall effect
        overall_effect = primary_results['overall_effect']
        overall_ci = [primary_results['ci_lower'], primary_results['ci_upper']]

        # Plot overall effect line
        ax.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        ax.plot(overall_effect, len(study_effects), 'D', color='red', markersize=10)

        # Overall effect confidence interval
        ax.plot([overall_ci[0], overall_ci[1]], [len(study_effects), len(study_effects)],
               color='red', linewidth=2)

        # Set labels
        all_labels = study_labels + ['Overall Effect']
        ax.set_yticks(range(len(all_labels)))
        ax.set_yticklabels(all_labels)

        ax.set_xlabel('Effect Size')
        ax.set_title(title)

        # Add CI text for overall effect
        ci_text = f"Overall: {overall_effect:.3f} [{overall_ci[0]:.3f}, {overall_ci[1]:.3f}]"
        ax.text(0.02, 0.98, ci_text, transform=ax.transAxes, fontsize=10,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Forest plot saved to {save_path}")

        return fig

    def funnel_plot(self, analysis_results: Dict[str, Any],
                   title: str = "Funnel Plot", save_path: str = None) -> plt.Figure:
        """Generate funnel plot for publication bias assessment"""

        fig, ax = plt.subplots(figsize=self.figsize)

        study_effects = analysis_results['study_effects']['effects']
        study_se = np.sqrt(analysis_results['study_effects']['variances'])

        # Plot studies
        ax.scatter(study_effects, study_se, alpha=0.7, s=50)

        # Add pseudo confidence intervals
        se_range = np.linspace(min(study_se), max(study_se), 100)

        # Fixed effect line (theoretical no-effect line)
        ax.plot([0, 0], [min(study_se), max(study_se)], '--', color='red', alpha=0.7)

        ax.set_xlabel('Effect Size')
        ax.set_ylabel('Standard Error')
        ax.set_title(title)
        ax.invert_yaxis()  # Convention in meta-analysis

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Funnel plot saved to {save_path}")

        return fig

    def heterogeneity_plot(self, analysis_results: Dict[str, Any],
                          title: str = "Heterogeneity Assessment", save_path: str = None) -> plt.Figure:
        """Generate heterogeneity visualization"""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)

        # Heterogeneity statistics
        het_stats = analysis_results['random_effects']['heterogeneity_test']

        # I-squared plot
        i2 = het_stats['I2'] or 0
        ax1.bar(['I²'], [i2], color='skyblue', alpha=0.7)
        ax1.set_ylabel('I² (%)')
        ax1.set_title('Heterogeneity (I²)')
        ax1.text(0, i2 + 1, f'{i2:.1f}', ha='center')

        # Q statistic plot
        q_stat = het_stats['Q'] or 0
        q_p = het_stats['p_value'] or 1
        colors = ['red' if q_p < 0.05 else 'green']
        ax2.bar(['Q'], [q_stat], color=colors[0], alpha=0.7)
        ax2.set_ylabel('Q Statistic')
        ax2.set_title('Cochran Q Test')

        plt.suptitle(title)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Heterogeneity plot saved to {save_path}")

        return fig


class AutomatedMetaAnalyzer:
    """Main automated meta-analysis system"""

    def __init__(self):
        self.effect_calculator = EffectSizeCalculator()
        self.visualizer = MetaAnalysisVisualizer()

    def prepare_data_from_csv(self, csv_file: str, effect_type: str = 'continuous',
                             intervention_col: str = None, control_col: str = None) -> pd.DataFrame:
        """Prepare data for meta-analysis from CSV"""

        logger.info(f"Loading data from {csv_file}")
        df = pd.read_csv(csv_file)

        logger.info(f"Loaded {len(df)} studies for meta-analysis")

        # Initialize result columns
        prepared_data = df.copy()

        prepared_data['effect_size'] = np.nan
        prepared_data['effect_se'] = np.nan
        prepared_data['effect_type'] = effect_type

        for idx, row in df.iterrows():
            try:
                if effect_type == 'continuous':
                    # For continuous outcomes, expect mean, SD, n for both groups
                    intervention_mean = row.get('intervention_mean')
                    intervention_sd = row.get('intervention_sd')
                    intervention_n = row.get('intervention_n')

                    control_mean = row.get('control_mean')
                    control_sd = row.get('control_sd')
                    control_n = row.get('control_n')

                    if all(x is not None for x in [intervention_mean, intervention_sd, intervention_n,
                                                 control_mean, control_sd, control_n]):
                        if intervention_n > 0 and control_n > 0 and intervention_sd > 0 and control_sd > 0:
                            effect, se = self.effect_calculator.cohen_d(
                                intervention_mean, control_mean, intervention_sd, control_sd,
                                int(intervention_n), int(control_n)
                            )

                            prepared_data.at[idx, 'effect_size'] = effect
                            prepared_data.at[idx, 'effect_se'] = se

                elif effect_type == 'binary':
                    # For binary outcomes, expect events and totals for both groups
                    intervention_events = row.get('intervention_events')
                    intervention_total = row.get('intervention_n')
                    control_events = row.get('control_events')
                    control_total = row.get('control_n')

                    # Try OR first
                    if all(x is not None for x in [intervention_events, intervention_total,
                                                 control_events, control_total]):
                        if all(x > 0 for x in [intervention_total, control_total]):
                            try:
                                effect, se = self.effect_calculator.odds_ratio(
                                    int(intervention_events), int(intervention_total),
                                    int(control_events), int(control_total)
                                )

                                prepared_data.at[idx, 'effect_size'] = effect
                                prepared_data.at[idx, 'effect_se'] = se
                            except:
                                # Fallback to risk difference if OR fails
                                effect, se = self.effect_calculator.risk_difference(
                                    int(intervention_events), int(intervention_total),
                                    int(control_events), int(control_total)
                                )

                                prepared_data.at[idx, 'effect_size'] = effect
                                prepared_data.at[idx, 'effect_se'] = se

                elif effect_type == 'pre_calculated':
                    # Effect size already calculated
                    effect = row.get('effect_size')
                    se = row.get('effect_se')

                    if effect is not None:
                        prepared_data.at[idx, 'effect_size'] = effect
                        prepared_data.at[idx, 'effect_se'] = se or 0.1  # Default SE if missing

            except Exception as e:
                logger.warning(f"Error processing study {idx}: {e}")
                continue

        # Remove studies without valid effect sizes
        valid_studies = prepared_data.dropna(subset=['effect_size', 'effect_se'])
        logger.info(f"Valid studies for analysis: {len(valid_studies)}/{len(prepared_data)}")

        return valid_studies

    def conduct_meta_analysis(self, prepared_data: pd.DataFrame,
                            analysis_method: str = 'auto',
                            study_label_col: str = 'study_id') -> Dict[str, Any]:
        """Conduct meta-analysis on prepared data"""

        logger.info(f"Conducting meta-analysis with {len(prepared_data)} studies")

        # Extract effect sizes and variances
        effect_sizes = prepared_data['effect_size'].values
        variances = (prepared_data['effect_se'] ** 2).values

        # Study labels
        study_labels = prepared_data[study_label_col].fillna(
            [f"Study {i+1}" for i in range(len(prepared_data))]).tolist()

        # Create meta-analysis model
        model = MetaAnalysisModel(effect_sizes, variances, study_labels)

        # Conduct analysis
        results = model.conduct_analysis(method=analysis_method)

        # Add study-level data
        results['study_data'] = prepared_data.to_dict('records')
        results['analysis_timestamp'] = datetime.now().isoformat()
        results['total_studies'] = len(prepared_data)

        logger.info("Meta-analysis completed successfully")

        return results

    def generate_plots(self, results: Dict[str, Any], output_dir: str = "meta_analysis_plots") -> Dict[str, str]:
        """Generate all meta-analysis plots"""

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        plots = {}

        # Forest plot
        forest_fig = self.visualizer.forest_plot(
            results,
            title="Meta-Analysis Forest Plot",
            save_path=str(output_path / "forest_plot.png")
        )
        plots['forest_plot'] = str(output_path / "forest_plot.png")

        # Funnel plot
        funnel_fig = self.visualizer.funnel_plot(
            results,
            title="Funnel Plot (Publication Bias Assessment)",
            save_path=str(output_path / "funnel_plot.png")
        )
        plots['funnel_plot'] = str(output_path / "funnel_plot.png")

        # Heterogeneity plot
        heterogeneity_fig = self.visualizer.heterogeneity_plot(
            results,
            title="Heterogeneity Assessment",
            save_path=str(output_path / "heterogeneity_plot.png")
        )
        plots['heterogeneity_plot'] = str(output_path / "heterogeneity_plot.png")

        logger.info(f"Generated plots: {list(plots.keys())}")

        return plots

    def generate_report(self, results: Dict[str, Any], plots: Dict[str, str] = None) -> str:
        """Generate comprehensive meta-analysis report"""

        primary_results = results['primary_results']

        report = f"""
# Meta-Analysis Results Report

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method:** {results['primary_method'].replace('_', ' ').title()}
**Total Studies:** {results['total_studies']}

## Overall Results

- **Overall Effect Size:** {primary_results['overall_effect']:.4f}
- **95% Confidence Interval:** [{primary_results['ci_lower']:.4f}, {primary_results['ci_upper']:.4f}]
- **Z-statistic:** {primary_results['z_stat']:.4f}
- **P-value:** {primary_results['p_value']:.4f}

**Interpretation:** {'Significant effect detected' if primary_results['p_value'] < 0.05 else 'No significant effect detected'}

## Heterogeneity Assessment

"""

        # Heterogeneity section
        het_test = primary_results['heterogeneity_test']
        if het_test['Q'] is not None:
            report += f"""
- **Q Statistic:** {het_test['Q']:.4f}
- **Q P-value:** {het_test['p_value']:.4f}
- **I²:** {het_test['I2']:.1f}%
"""

            # Heterogeneity interpretation
            i2 = het_test['I2']
            if i2 < 25:
                het_level = "Low heterogeneity"
            elif i2 < 50:
                het_level = "Moderate heterogeneity"
            elif i2 < 75:
                het_level = "Substantial heterogeneity"
            else:
                het_level = "Considerable heterogeneity"

            report += f"**Heterogeneity Level:** {het_level}\n\n"
        else:
            report += "- Heterogeneity assessment not applicable for fixed-effects model\n\n"

        # Study effects table
        report += "## Study-Level Effects\n\n"
        report += "| Study | Effect Size | 95% CI | Weight |\n"
        report += "|-------|-------------|---------|--------|\n"

        study_data = results['study_data']
        weights = primary_results['weights']

        for i, study in enumerate(study_data):
            effect = study['effect_size']
            se = study.get('effect_se', 0)
            ci_lower = effect - 1.96 * se
            ci_upper = effect + 1.96 * se
            weight_pct = (weights[i] / np.sum(weights)) * 100

            study_label = study.get('study_id', f"Study {i+1}")
            report += f"| {study_label} | {effect:.4f} | [{ci_lower:.4f}, {ci_upper:.4f}] | {weight_pct:.1f}% |\n"

        # Add total row
        total_weight = 100.0
        report += f"| **Overall** | **{primary_results['overall_effect']:.4f}** | **[{primary_results['ci_lower']:.4f}, {primary_results['ci_upper']:.4f}]** | **{total_weight:.1f}%** |\n\n"

        if plots:
            report += "## Generated Figures\n\n"
            for plot_name, plot_path in plots.items():
                report += f"- **{plot_name.replace('_', ' ').title()}:** `{plot_path}`\n"

        return report

    def full_analysis_pipeline(self, csv_file: str, effect_type: str = 'continuous',
                             output_dir: str = 'meta_analysis_results',
                             study_label_col: str = 'study_id') -> Dict[str, Any]:
        """Complete meta-analysis pipeline from data to report"""

        logger.info("Starting complete meta-analysis pipeline")

        # Step 1: Prepare data
        prepared_data = self.prepare_data_from_csv(
            csv_file, effect_type=effect_type, study_label_col=study_label_col
        )

        if len(prepared_data) == 0:
            raise ValueError("No valid studies found for meta-analysis")

        # Step 2: Conduct analysis
        results = self.conduct_meta_analysis(
            prepared_data, study_label_col=study_label_col
        )

        # Step 3: Generate plots
        output_path = Path(output_dir)
        plots = self.generate_plots(results, str(output_path / "plots"))

        # Step 4: Generate report
        report = self.generate_report(results, plots)

        # Save report
        report_path = output_path / "meta_analysis_report.md"
        with open(report_path, 'w') as f:
            f.write(report)

        # Save results as JSON
        results_path = output_path / "analysis_results.json"
        with open(results_path, 'w') as f:
            # Convert numpy types to Python types for JSON serialization
            json_results = self._convert_numpy_types(results)
            json.dump(json_results, f, indent=2)

        logger.info("Meta-analysis pipeline completed successfully")
        logger.info(f"Results saved to: {output_dir}")

        return {
            'results': results,
            'plots': plots,
            'report': report,
            'output_files': {
                'report': str(report_path),
                'results_json': str(results_path),
                'plots_dir': str(output_path / "plots")
            }
        }

    def _convert_numpy_types(self, obj):
        """Convert numpy types to Python types for JSON serialization"""
        if isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        else:
            return obj


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automated Meta-Analysis System")
    parser.add_argument("csv_file", help="CSV file with study data")
    parser.add_argument("--effect-type", choices=['continuous', 'binary', 'pre_calculated'],
                       default='continuous', help="Type of effect size")
    parser.add_argument("--output-dir", default='meta_analysis_results',
                       help="Output directory")
    parser.add_argument("--study-label-col", default='study_id',
                       help="Column name for study labels")

    args = parser.parse_args()

    analyzer = AutomatedMetaAnalyzer()
    results = analyzer.full_analysis_pipeline(
        args.csv_file,
        effect_type=args.effect_type,
        output_dir=args.output_dir,
        study_label_col=args.study_label_col
    )

    print(f"Meta-analysis completed! Results saved to: {args.output_dir}")
    print(f"Report: {results['output_files']['report']}")
    print("\nPlots generated:")
    for plot_name, plot_path in results['plots'].items():
        print(f"  {plot_name}: {plot_path}")
