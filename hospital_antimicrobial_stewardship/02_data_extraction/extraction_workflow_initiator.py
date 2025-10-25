#!/usr/bin/env python3
"""
Hospital Antimicrobial Stewardship Systematic Review
Extraction Workflow Initiator

This script initializes the systematic data extraction workflow for deployed batches,
providing step-by-step guidance through the extraction process.

Author: Research Team
Date: October 13, 2025
"""

import json
import os
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List, Optional
import urllib.parse

class ArticleFetcher:
    """Fetcher for obtaining full-text articles."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Research-Automation/1.0)'
        })

    def fetch_pubmed_abstract(self, pmid: str) -> Optional[str]:
        """Fetch abstract from PubMed."""
        try:
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Basic text extraction (would need more sophisticated parsing in production)
            if "Abstract" in response.text:
                return f"Fetched abstract for PMID {pmid} (Length: {len(response.text)} chars)"
            else:
                return f"Abstract not found for PMID {pmid}"

        except Exception as e:
            return f"Error fetching PMID {pmid}: {str(e)}"

    def get_doi_link(self, doi: str) -> str:
        """Generate direct DOI link for article access."""
        return f"https://doi.org/{doi}"

class ExtractionWorkflowInitiator:
    """Manages the complete extraction workflow."""

    def __init__(self, batch_package_path: str, batch_studies_path: str):
        self.batch_package_path = batch_package_path
        self.batch_studies_path = batch_studies_path
        self.article_fetcher = ArticleFetcher()

        # Load batch data
        with open(batch_package_path, 'r') as f:
            self.batch_package = json.load(f)

        self.studies_df = pd.read_csv(batch_studies_path)

    def display_batch_overview(self):
        """Display comprehensive batch overview."""
        print("\n" + "="*80)
        print("🏥 HOSPITAL ANTIMICROBIAL STEWARDSHIP DATA EXTRACTION")
        print("="*80)

        batch_info = self.batch_package['batch_info']
        print(f"\n🎯 BATCH {batch_info['batch_number']} OVERVIEW")
        print(f"⭐ Priority Level: {batch_info['priority_level']}")
        print(f"📊 Studies: {batch_info['batch_size']}")
        print(f"⏱️ Estimated Time: {batch_info['estimated_completion_time']}")
        print(f"🎯 Focus: {', '.join(batch_info['extraction_priorities'])}")

        print(f"\n📅 Deadline: {self.batch_package['batch_metadata']['extraction_deadline']}")

        print(f"\n📋 KEY EXTRACTION TARGETS:")
        for i, priority in enumerate(batch_info['extraction_priorities'], 1):
            print(f"  {i}. {priority.upper()}")

    def display_study_list(self):
        """Display the list of studies in this batch with PMIDs."""
        print("\n📚 BATCH STUDIES:")
        print("-" * 70)

        studies_list = self.batch_package['studies_list']
        for i, study in enumerate(studies_list, 1):
            print(f"{i:2d}")
            print(f"   ➤ STUDY ID: {study['study_id']}")
            print(f"   ➤ PMID: {study['pmid']}")
            print(f"   ➤ Priority: {study.get('priority_level', 'N/A')}")
            print(f"   ➤ Targets: {study.get('extraction_targets', [])}")


    def demonstrate_article_access(self):
        """Demonstrate how to access articles for extraction."""
        print("\n🔍 ARTICLE ACCESS WORKFLOW:")
        print("-" * 50)

        # Get sample articles to demonstrate
        sample_studies = self.studies_df.head(3)  # Show first 3 as examples

        for _, study in sample_studies.iterrows():
            pmid = study['pmid']
            study_id = study['study_id']

            print(f"\n📄 STUDY: {study_id}")
            print(f"🔗 Direct PubMed Link: https://pubmed.ncbi.nlm.nih.gov/{pmid}/")

            # Try to get title for context
            title = study.get('title', '')[:100] + "..." if len(str(study.get('title', ''))) > 100 else study.get('title', '')
            print(f"📖 Title: {title}")

            print("\n📋 ACCESS METHODS:")
            print("  1. Open PubMed link above in browser")
            print("  2. Click 'Full text links' to find free/full access")
            print("  3. Use institutional library access if available")
            print("  4. Check for PMC full text availability")
            print("  5. Note access date and source in extraction form"
    def interactive_extraction_guide(self):
        """Provide interactive extraction guidance."""
        print("\n📝 SYSTEMATIC EXTRACTION WORKFLOW:")
        print("-" * 60)

        checklist = self.batch_package['extraction_forms']['extraction_checklist']

        for step in checklist:
            print(f"\n{step['step']}. {step['description'].upper()}")
            print(f"   ⏱️  Estimated Time: {step['estimated_time']}")

        print("\n🔧 EXTRACTION FORMS AVAILABLE:")
        forms = list(self.batch_package['extraction_forms'].keys())
        forms.remove('extraction_checklist')  # Remove from display
        forms.remove('validation_rules')

        for i, form in enumerate(forms, 1):
            form_name = form.replace('_', ' ').title()
            if 'form' in form_name.lower():
                print(f"  {i}. {form_name}")

        print("\n✅ VALIDATION RULES:")
        validation = self.batch_package['extraction_forms']['validation_rules']
        print(f"  • Study characteristics: {len(validation['study_characteristics'])} rules")
        print(f"  • Outcome data: {len(validation['outcome_data'])} rules")
        print(f"  • Cross-validation: {len(validation['cross_validation_rules'])} rules")

    def generate_researcher_instructions(self):
        """Generate detailed instructions for researchers."""
        print("\n🎯 DETAILED RESEARCHER INSTRUCTIONS:")
        print("=" * 70)

        print("""
1. ARTICLE ACQUISITION:
   • Locate PDF/full-text for each assigned study
   • Note access date and source (PubMed, publisher, institutional access)
   • Save DOI/reference information for documentation

2. QUALITY CONTROL SETUP:
   • Prepare spreadsheet software (Excel/Google Sheets)
   • Download batch study list and extraction forms
   • Set up validation tracking for double extractions

3. SYSTEMATIC EXTRACTION SEQUENCE:
   a) Study Characteristics (15-20 min)
      → Basic study info, design, population, setting

   b) Intervention Details (20-25 min)
      → Complete intervention characterization
      → Implementation strategy documentation

   c) Outcome Data (25-30 min)
      → All effect estimates with confidence intervals
      → Statistical model documentation

   d) Quality Assessment (15-20 min)
      → Domain-specific risk of bias evaluation

   e) Cross-Validation (10 min)
      → Internal consistency checks
      → Calculation verification

4. OUTPUT FORMATS:
   • Study characteristics: CSV format following template
   • Intervention details: Structured according to categories
   • Outcome data: Effect estimates, CIs, p-values
   • Quality assessment: Domain scores with evidence

5. QUALITY ASSURANCE:
   • Double extraction for 20% of studies (minimum)
   • Third reviewer arbitration for discrepancies
   • 100% agreement required on critical variables

6. DEADLINE MANAGEMENT:
   • Submit extractions within 2 weeks
   • Flag any access issues immediately
   • Request extensions only for documented technical issues
        """)

    def create_extraction_progress_tracker(self) -> str:
        """Create a progress tracking spreadsheet template."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tracker_file = f"extraction_progress_tracker_{timestamp}.csv"

        # Create progress tracker dataframe
        progress_data = []
        for _, study in self.studies_df.iterrows():
            progress_data.append({
                'study_id': study['study_id'],
                'pmid': study['pmid'],
                'batch_number': self.batch_package['batch_info']['batch_number'],
                'priority_level': study.get('priority_level', ''),
                'access_status': 'Pending',
                'access_date': '',
                'extraction_status': 'Not Started',
                'extractor_initials': '',
                'completion_date': '',
                'double_extraction': 'No',
                'verification_status': 'Pending',
                'notes': ''
            })

        progress_df = pd.DataFrame(progress_data)
        progress_df.to_csv(tracker_file, index=False)

        print(f"\n📊 Progress tracker created: {tracker_file}")
        return tracker_file

    def run_interactive_session(self):
        """Run the complete interactive extraction initiation session."""
        print("🏁 STARTING EXTRACTION WORKFLOW INITIALIZATION...")

        # Display comprehensive information
        self.display_batch_overview()
        self.display_study_list()
        self.demonstrate_article_access()
        self.interactive_extraction_guide()
        self.generate_researcher_instructions()

        # Create progress tracker
        tracker_file = self.create_extraction_progress_tracker()

        print("
🎯 EXTRACTION PHASE INITIATED"        print(f"📋 Progress Tracking: {tracker_file}")
        print("🏥 Hospital Antimicrobial Stewardship Review - Phase 3 Active
"        # Completion confirmation
        print("✅ WORKFLOW INITIALIZATION COMPLETE")
        print("📝 Ready to begin systematic data extraction")
        print("🔬 Good luck with the research extraction!"

def main():
    """Main function for extraction workflow initiation."""

    print("🔄 SELECTING EXTRACTION BATCH...")
    print("Available Batches:")
    print("1. Batch 1: Medium Priority Studies (8 studies)")
    print("2. Batch 2: High-Impact Mortality Studies (2 studies)")

    # Default to Batch 2 (recommended to start with high-impact studies)
    batch_choice = 2  # User would normally select this

    if batch_choice == 1:
        batch_package = "batch_extraction_package_20251013_143043.json"
        batch_studies = "batch_1_studies_20251013_143043.csv"
    elif batch_choice == 2:
        batch_package = "batch_extraction_package_20251013_143454.json"
        batch_studies = "batch_2_studies_20251013_143454.csv"
    else:
        print("Invalid choice")
        return

    # Check if files exist
    if not os.path.exists(batch_package) or not os.path.exists(batch_studies):
        print("❌ Error: Batch files not found. Run batch_extraction_starter.py first.")
        return

    # Initialize workflow
    initiator = ExtractionWorkflowInitiator(batch_package, batch_studies)
    initiator.run_interactive_session()

if __name__ == "__main__":
    main()
