#!/usr/bin/env python3
"""
Literature Screening Script
Automated and semi-automated screening of titles and abstracts
"""

import pandas as pd
import re
import os

class LiteratureScreener:
    def __init__(self):
        self.inclusion_keywords = []
        self.exclusion_keywords = []

    def screen_titles_abstracts(self, csv_file, include_column='title_abstract', output_file=None):
        """Screen studies based on title/abstract"""
        if output_file is None:
            output_file = csv_file.replace('.csv', '_screened.csv')

        df = pd.read_csv(csv_file)

        # Apply inclusion/exclusion criteria
        df['screening_decision'] = df[include_column].apply(self._classify_abstract)

        # Save screened results
        df.to_csv(output_file, index=False)
        print(f"Screened {len(df)} studies. Results saved to {output_file}")

        return df

    def _classify_abstract(self, text):
        """Classify abstract based on keywords"""
        text_lower = str(text).lower()

        # Check exclusion keywords
        for keyword in self.exclusion_keywords:
            if keyword.lower() in text_lower:
                return 'exclude'

        # Check inclusion keywords
        include_count = 0
        for keyword in self.inclusion_keywords:
            if keyword.lower() in text_lower:
                include_count += 1

        # Decision logic
        if include_count >= 2:  # Require at least 2 inclusion keywords
            return 'include'
        elif include_count == 1:
            return 'maybe'
        else:
            return 'exclude'

def main():
    screen = LiteratureScreener()

    # Configure keywords
    screen.inclusion_keywords = [
        # Add your inclusion keywords
    ]

    screen.exclusion_keywords = [
        # Add your exclusion keywords
    ]

    # Screen literature
    screen.screen_titles_abstracts('literature_search_results.csv')

if __name__ == "__main__":
    main()