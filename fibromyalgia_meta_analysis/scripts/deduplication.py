#!/usr/bin/env python3
"""
Automated Deduplication for Literature Search Results

This script removes duplicate studies from literature search results
using title similarity, PMID matching, and DOI matching algorithms.

Author: Research Automation System
Date: September 24, 2025
"""

import pandas as pd
import numpy as np
import re
import logging
from typing import List, Set
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LiteratureDeduplicator:
    """Automated deduplication of literature search results"""

    def __init__(self):
        self.deduplication_stats = {
            'original_count': 0,
            'unique_count': 0,
            'duplicates_removed': 0,
            'duplicates_by_pmid': 0,
            'duplicates_by_doi': 0,
            'duplicates_by_title': 0
        }

    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        if not text or pd.isna(text):
            return ""

        # Convert to lowercase, remove special chars, extra spaces
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def get_title_similarity(self, title1: str, title2: str, threshold: float = 0.85) -> bool:
        """Check if two titles are similar"""
        t1_norm = self.normalize_text(title1)
        t2_norm = self.normalize_text(title2)

        if not t1_norm or not t2_norm:
            return False

        # Simple word overlap similarity
        words1 = set(t1_norm.split())
        words2 = set(t2_norm.split())

        if not words1 or not words2:
            return False

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        similarity = len(intersection) / len(union)
        return similarity >= threshold

    def deduplicate_by_identifiers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicates using PMID, DOI, and PMCID"""
        logger.info("Removing duplicates by identifiers...")

        original_count = len(df)
        self.deduplication_stats['original_count'] = original_count

        # Create identifier columns
        identifier_cols = []
        if 'pmid' in df.columns:
            df['pmid_clean'] = df['pmid'].astype(str).str.strip()
            identifier_cols.append('pmid_clean')
        if 'doi' in df.columns:
            df['doi_clean'] = df['doi'].astype(str).str.strip().str.lower()
            identifier_cols.append('doi_clean')
        if 'pmcid' in df.columns:
            df['pmcid_clean'] = df['pmcid'].astype(str).str.strip()
            identifier_cols.append('pmcid_clean')

        if not identifier_cols:
            logger.warning("No identifier columns found")
            return df

        # Remove duplicates based on any identifier
        df = df.drop_duplicates(subset=identifier_cols, keep='first')

        identifiers_removed = original_count - len(df)
        self.deduplication_stats['duplicates_by_pmid'] = identifiers_removed

        logger.info(f"  Removed {identifiers_removed} duplicates by identifiers")
        return df

    def deduplicate_by_title(self, df: pd.DataFrame, similarity_threshold: float = 0.85) -> pd.DataFrame:
        """Remove duplicates with similar titles"""
        logger.info("Removing duplicates by title similarity...")

        if 'title' not in df.columns:
            logger.warning("No title column found")
            return df

        titles = df['title'].fillna('').tolist()
        keep_indices = []
        duplicates_found = set()

        for i, title1 in enumerate(titles):
            if i in duplicates_found:
                continue

            keep_indices.append(i)

            for j in range(i + 1, len(titles)):
                if j in duplicates_found:
                    continue

                title2 = titles[j]
                if self.get_title_similarity(title1, title2, similarity_threshold):
                    duplicates_found.add(j)
                    logger.debug(f"  Duplicate found: '{title1[:50]}...' vs '{title2[:50]}...'")

        df_deduped = df.iloc[keep_indices].copy()
        titles_removed = len(df) - len(df_deduped)
        self.deduplication_stats['duplicates_by_title'] = titles_removed

        logger.info(f"  Removed {titles_removed} duplicates by title similarity")
        return df_deduped

    def add_deduplication_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add deduplication metadata to the dataframe"""
        df = df.copy()
        df['deduplication_date'] = pd.Timestamp.now()
        df['process_stage'] = 'deduplication_completed'
        return df

    def generate_deduplication_report(self, df: pd.DataFrame, output_path: str = None) -> dict:
        """Generate deduplication statistics report"""
        self.deduplication_stats['unique_count'] = len(df)
        self.deduplication_stats['duplicates_removed'] = (
            self.deduplication_stats['original_count'] - self.deduplication_stats['unique_count']
        )

        report = {
            'deduplication_summary': self.deduplication_stats,
            'processing_details': {
                'timestamp': pd.Timestamp.now().isoformat(),
                'columns_processed': list(df.columns),
                'final_row_count': len(df)
            }
        }

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame([self.deduplication_stats]).to_json(
                output_path.replace('.csv', '_dedup_report.json'),
                orient='records', indent=2
            )

        return report

    def deduplicate(self, input_file: str, output_file: str = None,
                   similarity_threshold: float = 0.85) -> pd.DataFrame:
        """
        Complete deduplication workflow

        Args:
            input_file: Path to input CSV with literature results
            output_file: Path to save deduplicated results
            similarity_threshold: Title similarity threshold (0-1)

        Returns:
            Deduplicated DataFrame
        """
        logger.info(f"Starting deduplication of {input_file}")

        # Load data
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        logger.info(f"Loaded {len(df)} records for deduplication")

        # Step 1: Remove duplicates by identifiers
        df = self.deduplicate_by_identifiers(df)

        # Step 2: Remove duplicates by title similarity
        df = self.deduplicate_by_title(df, similarity_threshold)

        # Step 3: Add metadata
        df = self.add_deduplication_metadata(df)

        # Generate report
        report = self.generate_deduplication_report(df, output_file)

        # Save results
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"Saved deduplicated results to {output_file}")

        logger.info("Deduplication Summary:")
        logger.info(f"  Original records: {report['deduplication_summary']['original_count']}")
        logger.info(f"  Unique records: {report['deduplication_summary']['unique_count']}")
        logger.info(f"  Duplicates removed: {report['deduplication_summary']['duplicates_removed']}")

        return df


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='Literature deduplication')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', help='Output CSV file')
    parser.add_argument('--similarity-threshold', type=float, default=0.85,
                       help='Title similarity threshold')

    args = parser.parse_args()

    deduplicator = LiteratureDeduplicator()
    result_df = deduplicator.deduplicate(
        args.input, args.output, args.similarity_threshold
    )

    print(f"Deduplication completed. Unique records: {len(result_df)}")


if __name__ == "__main__":
    main()
