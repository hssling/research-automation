#!/usr/bin/env python3
"""
AI-Assisted Literature Screening for Systematic Reviews

This script uses machine learning to assist with title/abstract screening
of literature search results for inclusion in systematic reviews.

Author: Research Automation System
Date: September 24, 2025
"""

import pandas as pd
import numpy as np
import os
import sys
import json
from datetime import datetime
import argparse
from pathlib import Path

# Add research-automation-core to path
sys.path.append('../../research-automation-core')

from ai_literature_screener import AILiteratureScreener, train_ai_screener


class AutomatedLiteratureScreener:
    """Automated literature screening system"""

    def __init__(self, models_path: str = "../../research-automation-core/models"):
        self.models_path = Path(models_path)
        self.screener = AILiteratureScreener(model_path=str(self.models_path))
        self.screening_results = {}

    def load_or_train_model(self, training_data_path: str = None,
                           text_column: str = 'title_abstract',
                           label_column: str = 'decision') -> AILiteratureScreener:
        """
        Load existing model or train new one for screening

        Args:
            training_data_path: Path to labeled training data
            text_column: Column with text data
            label_column: Column with inclusion decisions

        Returns:
            Trained screener
        """

        # Check if models exist
        if (self.models_path / "vectorizer.pkl").exists():
            print("Loading existing screening models...")
            self.screener.load_models(str(self.models_path))
            if self.screener.models:
                print("✓ Loaded pretrained models")
                return self.screener

        # If no training data provided, create basic screener
        if not training_data_path or not Path(training_data_path).exists():
            print("No training data found. Using keyword-based screening...")
            return self.screener

        # Train new model
        print("Training new AI screening model...")
        trained_screener, eval_results = train_ai_screener(
            training_data_path=training_data_path,
            text_column=text_column,
            label_column=label_column,
            output_dir=str(self.models_path)
        )

        print("✓ Model training completed")
        print(f"✓ Best model: {eval_results.get('best_model', 'N/A')}")
        print(".3f")

        self.screener = trained_screener
        return self.screener

    def prepare_text_for_screening(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare text data for screening"""
        df = df.copy()

        # Create title_abstract combination
        title_col = 'title' if 'title' in df.columns else 'Title'
        abstract_col = 'abstract' if 'abstract' in df.columns else 'Abstract'

        df['title_abstract'] = df[title_col].fillna('') + ' ' + df[abstract_col].fillna('')

        # Remove empty text entries
        df = df[df['title_abstract'].str.strip() != '']

        return df

    def apply_screening_criteria(self, df: pd.DataFrame,
                                inclusion_keywords: list = None,
                                exclusion_keywords: list = None) -> pd.DataFrame:
        """
        Apply keyword-based screening criteria

        Args:
            df: DataFrame with literature
            inclusion_keywords: Keywords that suggest inclusion
            exclusion_keywords: Keywords that suggest exclusion

        Returns:
            DataFrame with keyword-based screening
        """

        if not inclusion_keywords:
            inclusion_keywords = [
                'fibromyalgia', 'fibromyalgia syndrome', 'fms',
                'microbiome', 'microbiota', 'microbial',
                'gut microbiome', 'intestinal microbiome'
            ]

        if not exclusion_keywords:
            exclusion_keywords = [
                'systematic review', 'meta analysis', 'review article',
                'editorial', 'letter', 'commentary',
                'animal', 'mouse', 'rat', 'mice', 'rats'
            ]

        df = df.copy()

        # Keyword screening
        def check_keywords(text: str, keywords: list) -> bool:
            text_lower = str(text).lower()
            return any(keyword.lower() in text_lower for keyword in keywords)

        df['has_inclusion_keywords'] = df['title_abstract'].apply(
            lambda x: check_keywords(x, inclusion_keywords)
        )
        df['has_exclusion_keywords'] = df['title_abstract'].apply(
            lambda x: check_keywords(x, exclusion_keywords)
        )

        # Combined decision
        df['keyword_based_decision'] = np.where(
            df['has_inclusion_keywords'] & ~df['has_exclusion_keywords'],
            'potentially_include',
            'potentially_exclude'
        )

        return df

    def screen_literature(self, input_file: str, output_file: str = None,
                         training_data_path: str = None,
                         confidence_threshold: float = 0.7) -> pd.DataFrame:
        """
        Complete automated screening workflow

        Args:
            input_file: CSV with literature to screen
            output_file: Path to save screening results
            training_data_path: Path to labeled training data for AI model
            confidence_threshold: Threshold for automatic decisions

        Returns:
            DataFrame with screening results
        """

        print("🔍 Starting automated literature screening...")
        print(f"📂 Input file: {input_file}")

        # Load literature data
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        print(f"✓ Loaded {len(df)} studies for screening")

        # Prepare text data
        df = self.prepare_text_for_screening(df)
        print(f"✓ Prepared text data for {len(df)} studies")

        # Apply keyword-based screening
        df = self.apply_screening_criteria(df)
        keyword_inclusion = (df['keyword_based_decision'] == 'potentially_include').sum()
        print(f"✓ Keyword screening: {keyword_inclusion} potentially relevant")

        # Load or train AI model
        trained_screener = self.load_or_train_model(training_data_path)

        # Apply AI screening
        screened_df = trained_screener.screen_literature(
            csv_file=input_file,
            text_column='title_abstract',
            output_file=None,
            confidence_threshold=confidence_threshold
        )

        # Merge keyword and AI results
        # For simplicity, use AI results as primary, keyword as secondary
        result_df = df.copy()

        # Add AI screening results if available
        if len(screened_df) > 0:
            ai_columns = ['ai_decision', 'ai_confidence', 'probability_include',
                         'probability_exclude', 'needs_review']
            for col in ai_columns:
                if col in screened_df.columns:
                    result_df[col] = screened_df[col]

        # Create final recommendations
        result_df['screening_recommendation'] = 'manual_review'

        # High AI confidence inclusion
        ai_include_mask = (
            (result_df.get('ai_decision', '') == 'include') &
            (result_df.get('ai_confidence', 0) > confidence_threshold)
        ) | result_df.get('probability_include', 0) > 0.8

        # Keyword-based inclusion
        keyword_include_mask = result_df['keyword_based_decision'] == 'potentially_include'

        # Combine decisions
        result_df.loc[ai_include_mask & keyword_include_mask, 'screening_recommendation'] = 'include'
        result_df.loc[~ai_include_mask & ~keyword_include_mask, 'screening_recommendation'] = 'exclude'

        # Add metadata
        result_df['screening_date'] = datetime.now().isoformat()
        result_df['screening_method'] = 'automated_ai_keyword'
        result_df['confidence_threshold_used'] = confidence_threshold

        # Screening statistics
        total_studies = len(result_df)
        ai_include = (result_df.get('ai_decision', '') == 'include').sum()
        keyword_include = (result_df['keyword_based_decision'] == 'potentially_include').sum()
        final_include = (result_df['screening_recommendation'] == 'include').sum()
        manual_review = (result_df['screening_recommendation'] == 'manual_review').sum()

        print("\n📊 Screening Results Summary:")
        print(f"  Total studies screened: {total_studies}")
        print(f"  AI suggests include: {ai_include}")
        print(f"  Keywords suggest include: {keyword_include}")
        print(f"  Final automated include: {final_include}")
        print(f"  Require manual review: {manual_review}")

        # Save results
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"✓ Screening results saved: {output_file}")

            # Save screening report
            report_path = output_file.replace('.csv', '_screening_report.json')
            report = {
                'screening_summary': {
                    'total_studies': total_studies,
                    'ai_suggestions_include': int(ai_include),
                    'keyword_suggestions_include': int(keyword_include),
                    'final_include': int(final_include),
                    'manual_review': int(manual_review),
                    'automation_rate': round((total_studies - manual_review) / total_studies * 100, 1)
                },
                'parameters': {
                    'confidence_threshold': confidence_threshold,
                    'training_data_used': training_data_path is not None,
                    'screening_date': datetime.now().isoformat()
                }
            }

            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"✓ Screening report saved: {report_path}")

        return result_df


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Automated literature screening')
    parser.add_argument('--input', required=True, help='Input CSV file to screen')
    parser.add_argument('--output', help='Output CSV file')
    parser.add_argument('--training-data', help='Path to labeled training data for AI model')
    parser.add_argument('--confidence-threshold', type=float, default=0.7,
                       help='AI confidence threshold for automatic decisions')

    args = parser.parse_args()

    screener = AutomatedLiteratureScreener()
    result_df = screener.screen_literature(
        args.input, args.output, args.training_data, args.confidence_threshold
    )

    print(f"\n✓ Literature screening completed for {len(result_df)} studies")


if __name__ == "__main__":
    main()
