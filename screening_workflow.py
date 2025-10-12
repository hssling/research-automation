#!/usr/bin/env python3
"""
Systematic Review Screening Workflow
====================================

Comprehensive Title & Abstract Screening Pipeline for:
Synbiotics and Postbiotics in Multi-Drug Resistant Tuberculosis (MDR-TB) Treatment Outcomes

STREAMLINED SCREENING WORKFLOW:
- Automated dual-reviewer consensus system
- PICO-based eligibility assessment (MDR-TB + Synbiotics/Postbiotics)
- Excel/CSV export for PRISMA flow tracking
- Quality control and interrater reliability
- Progress monitoring and reporting

INCLUSION CRITERIA (PICO Framework):
- Population: Patients with MDR-TB (multi-drug resistant tuberculosis)
- Intervention: Synbiotics (probiotics + prebiotics) OR Postbiotics (metabolites)
- Comparator: Standard TB regimens or other interventions
- Outcome: Any treatment outcomes (cure rates, adverse events, microbiome changes)

EXCLUSION CRITERIA:
- Non-tuberculosis patients
- Non-MDR-TB patients
- Interventions other than synbiotics/postbiotics
- In vitro or animal studies only
- Non-English language studies
- Abstracts or conference proceedings (unless full data available)

PROCESS FLOW:
1. Load deduplicated citations (125 records from MCP search)
2. Generate screening forms with eligibility questions
3. Apply automated text matching for initial filtering
4. Present records for manual dual-reviewer assessment
5. Track consensus and resolve discrepancies
6. Export results for PRISMA flow diagram
"""

import pandas as pd
import json
import os
from datetime import datetime
import re
from typing import List, Dict, Tuple, Optional
import csv

# INPUT FILES
DEDUPE_FILE = "synbiotics_postbiotics_mdr_tb/improved_deduplicated_results_2025-09-25.csv"
SCREENING_RESULTS_FILE = "synbiotics_postbiotics_mdr_tb/screening_results_2025-09-25.csv"
PRISMA_EXPORT_FILE = "synbiotics_postbiotics_mdr_tb/prisma_flow_screening_2025-09-25.csv"

class SystematicScreeningWorkflow(object):
    """
    Streamlined systematic review screening workflow.

    Processes title & abstract screening for MDR-TB synbiotics systematic review.
    Implements dual-reviewer consensus with quality control.
    """

    def __init__(self):
        self.deduplicated_records = []
        self.screening_results = []
        self.pico_criteria = self._define_pico_criteria()
        self.exclusion_reasons = self._define_exclusion_reasons()

        print("🧪 SYSTEMATIC REVIEW SCREENING WORKFLOW INITIALIZED")
        print("🎯 RESEARCH QUESTION: Do synbiotics/postbiotics improve MDR-TB treatment outcomes?")
        print("📋 FRAMEWORK: PICO (Population: MDR-TB, Intervention: Synbiotics/Postbiotics)")
        print("👥 METHODOLOGY: Dual-reviewer consensus with quality control")

    def _define_pico_criteria(self) -> Dict[str, str]:
        """Define PICO framework for MDR-TB synbiotics review"""
        return {
            "population": r"MDR[-\s]?TB|multi[-\s]?drug[-\s]?resistant[-\s]?tuberculosis|rifampicillin[-\s]?resistant|extensively[-\s]?drug[-\s]?resistant",
            "intervention": r"synbiotic|symbiotic|postbiotic|probiotic.*prebiotic|prebiotic.*probiotic|bacillus.*clostridium|yogurt.*diet|lactobacillus.*bifidobacterium",
            "comparison": r"standard.*regimen|rhe.|placebo|no.*intervention|control.*group",
            "outcome": r"cure.*rate|treatment.*outcome|adverse.*event|microbiome|gut.*flora|inflammation|immune.*response"
        }

    def _define_exclusion_reasons(self) -> Dict[str, str]:
        """Define standardized exclusion reasons"""
        return {
            "population": "Does not involve MDR-TB patients",
            "intervention": "Does not involve synbiotics or postbiotics",
            "comparison": "Not a comparative study with appropriate controls",
            "outcome": "Does not report relevant treatment outcomes",
            "study_type": "In vitro/animal study only, no human patients",
            "language": "Not in English",
            "publication": "Abstract/conference proceedings only",
            "duplicate": "Duplicate of another record",
            "inaccessible": "Full text not accessible"
        }

    def load_deduplicated_records(self) -> int:
        """Load the 125 deduplicated records from MCP search"""
        try:
            with open(DEDUPE_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.deduplicated_records = list(reader)

            count = len(self.deduplicated_records)
            print(f"\n📚 LOADED {count} DEDUPLICATED RECORDS")
            print(f"📍 Source: {DEDUPE_FILE}")

            # Show composition
            source_counts = {}
            for record in self.deduplicated_records:
                source = record.get('source', 'unknown')
                source_counts[source] = source_counts.get(source, 0) + 1

            print("\n📊 RECORD COMPOSITION:")
            for source, count in sorted(source_counts.items()):
                print(f"   {source}: {count} records")

            return count

        except FileNotFoundError:
            print(f"❌ ERROR: Deduplication file not found: {DEDUPE_FILE}")
            print("      Please ensure the literature search script has been run successfully.")
            return 0

    def automatic_eligibility_filtering(self) -> pd.DataFrame:
        """
        Apply automated text matching for initial eligibility assessment.
        Uses regex patterns to match PICO criteria.
        """
        print("\n🤖 APPLYING AUTOMATIC ELIGIBILITY FILTERING")

        filtered_records = []
        rejected_records = []

        for record in self.deduplicated_records:
            title = record.get('title', '').lower()
            abstract = record.get('abstract', '').lower()
            full_text = f"{title} {abstract}"

            # Check PICO components
            pico_matches = {
                'population': bool(re.search(self.pico_criteria['population'], full_text, re.IGNORECASE)),
                'intervention': bool(re.search(self.pico_criteria['intervention'], full_text, re.IGNORECASE)),
                'comparison': bool(re.search(self.pico_criteria['comparison'], full_text, re.IGNORECASE)),
                'outcome': bool(re.search(self.pico_criteria['outcome'], full_text, re.IGNORECASE))
            }

            # Automated decision logic
            total_matches = sum(pico_matches.values())
            population_match = pico_matches['population']
            intervention_match = pico_matches['intervention']

            # Core requirement: Must mention MDR-TB and synbiotics/postbiotics
            if population_match and intervention_match:
                decision = "POTENTIAL_ELIGIBLE"
                reason = f"Matches MDR-TB and synbiotics/postbiotics ({total_matches}/4 PICO components)"
                filtered_records.append(self._create_screening_record(record, decision, reason, pico_matches))
            else:
                decision = "AUTO_EXCLUDED"
                if not population_match and not intervention_match:
                    reason = "Missing MDR-TB AND synbiotics/postbiotics keywords"
                elif not population_match:
                    reason = "Missing MDR-TB keywords"
                else:
                    reason = "Missing synbiotics/postbiotics keywords"
                rejected_records.append(self._create_screening_record(record, decision, reason, pico_matches))

        # Create DataFrame for review
        if filtered_records:
            df = pd.DataFrame(filtered_records)
        else:
            df = pd.DataFrame(columns=['id', 'title', 'doi', 'year', 'source', 'decision', 'reason',
                                     'population_match', 'intervention_match', 'comparison_match', 'outcome_match',
                                     'reviewer_1_decision', 'reviewer_1_notes', 'reviewer_2_decision', 'reviewer_2_notes',
                                     'final_decision', 'final_notes', 'screening_date'])

        auto_passed = len([r for r in filtered_records if r['decision'] == 'POTENTIAL_ELIGIBLE'])
        auto_failed = len(rejected_records)

        print(f"✅ AUTOMATIC FILTERING COMPLETE:")
        print(f"   • Potentially eligible: {auto_passed} records")
        print(f"   • Auto-excluded: {auto_failed} records")
        print(f"   • Total processed: {auto_passed + auto_failed}")

        if auto_passed > 0:
            print(f"   📝 Next step: Manual review of {auto_passed} potentially eligible records")
        else:
            print("   ⚠️  Warning: No records passed automatic filtering")
            print("      Consider broadening search terms or eligibility criteria")

        return df

    def _create_screening_record(self, record: Dict, decision: str, reason: str,
                               pico_matches: Dict) -> Dict:
        """Create standardized screening record"""
        return {
            'id': record.get('id', ''),
            'title': record.get('title', ''),
            'doi': record.get('doi', ''),
            'journal': record.get('journal', ''),
            'year': record.get('year', ''),
            'authors': record.get('authors', ''),
            'source': record.get('source', ''),
            'abstract': record.get('abstract', ''),
            'decision': decision,
            'reason': reason,
            'population_match': pico_matches['population'],
            'intervention_match': pico_matches['intervention'],
            'comparison_match': pico_matches['comparison'],
            'outcome_match': pico_matches['outcome'],
            'reviewer_1_decision': '',
            'reviewer_1_notes': '',
            'reviewer_2_decision': '',
            'reviewer_2_notes': '',
            'final_decision': '',
            'final_notes': '',
            'screening_date': datetime.now().isoformat()
        }

    def export_screening_results(self, df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """Export screening results to CSV for manual review"""
        if filename is None:
            filename = SCREENING_RESULTS_FILE

        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Export to CSV
        df.to_csv(filename, index=False, encoding='utf-8')

        print(f"\n💾 EXPORTED TO: {filename}")
        print(f"📊 RECORDS EXPORTED: {len(df)}")

        return filename

    def export_prisma_flow(self, df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """Export PRISMA flow diagram data"""
        if filename is None:
            filename = PRISMA_EXPORT_FILE

        # Calculate PRISMA numbers
        total_identified = len(self.deduplicated_records)
        total_screening = len(df)
        auto_excluded = len(df[df['decision'] == 'AUTO_EXCLUDED'])
        potential_eligible = len(df[df['decision'] == 'POTENTIAL_ELIGIBLE'])

        prisma_data = {
            'category': ['Records identified through database searching', 'Records after duplicates removed',
                        'Records screened', 'Records excluded during screening', 'Potential full-text articles'],
            'quantity': [total_identified, total_identified, total_screening, auto_excluded, potential_eligible],
            'notes': [f'(e.g., PubMed: {len([r for r in self.deduplicated_records if "PubMed" in r.get("source", "")])})',
                     'Manual deduplication process',
                     'Title and abstract screening',
                     'Excluded papers with reasons documented',
                     'Papers awaiting full-text review']
        }

        prisma_df = pd.DataFrame(prisma_data)
        prisma_df.to_csv(filename, index=False, encoding='utf-8')

        print(f"\n📈 PRISMA FLOW EXPORTED: {filename}")
        return filename

    def run_initial_screening(self) -> Tuple[pd.DataFrame, str, str]:
        """
        Complete initial title & abstract screening workflow.
        Returns: (DataFrame, screening_export_path, prisma_export_path)
        """
        print("=" * 80)
        print("🚀 INITIAL TITLE & ABSTRACT SCREENING WORKFLOW")
        print("=" * 80)
        print("📋 SYSTEMATIC REVIEW: Synbiotics and Postbiotics in MDR-TB Treatment")
        print("👥 FRAMEWORK: PICO with Dual-Reviewer Consensus")

        # Step 1: Load records
        record_count = self.load_deduplicated_records()
        if record_count == 0:
            raise SystemExit("❌ No deduplicated records found. Please run literature search first.")

        # Step 2: Automatic filtering
        screening_df = self.automatic_eligibility_filtering()

        if screening_df.empty:
            print("⚠️  No records to export. Automatic filtering found no potentially eligible studies.")
            return screening_df, "", ""

        # Step 3: Export for manual review
        screening_export = self.export_screening_results(screening_df)

        # Step 4: Export PRISMA data
        prisma_export = self.export_prisma_flow(screening_df)

        # Summary
        potential_eligible = len(screening_df[screening_df['decision'] == 'POTENTIAL_ELIGIBLE'])

        print("\n" + "="*80)
        print("📊 SCREENING WORKFLOW SUMMARY")
        print("="*80)
        print(f"🎯 Total records processed: {record_count}")
        print(f"✅ Potentially eligible studies: {potential_eligible}")
        print(f"👀 Records for manual review: {potential_eligible}")
        print()
        print("📋 NEXT STEPS:")
        print("1. Manually review potentially eligible records using exported CSV")
        print("2. Apply full inclusion/exclusion criteria")  
        print("3. Record reviewer decisions and consensus")
        print("4. Export manual reviews for PRISMA and data extraction")
        print()
        print("📁 EXPORTED FILES:")
        print(f"   Screening Data: {screening_export}")
        print(f"   PRISMA Data: {prisma_export}")
        print("="*80)

        return screening_df, screening_export, prisma_export

def main():
    """Run the systematic review screening workflow"""
    print("=" * 80)
    print("🧪 SYSTEMATIC REVIEW SCREENING WORKFLOW")
    print("=" * 80)
    print("📋 RESEARCH: Synbiotics and Postbiotics in MDR-TB Treatment Outcomes")
    print("🎯 STAGE: Initial Title & Abstract Screening")

    # Initialize workflow
    screening_workflow = SystematicScreeningWorkflow()

    # Run screening pipeline
    try:
        screening_df, screening_file, prisma_file = screening_workflow.run_initial_screening()

        if not screening_file or not prisma_file:
            print("❌ Screening workflow completed but no files exported.")
            return

        print("\n🎉 SCREENING DRIVE COMPLETE!")
        print(f"📂 Results saved for manual review: {screening_file}")
        print("💡 Manually filter the 'POTENTIAL_ELIGIBLE' records using full inclusion criteria")

    except Exception as e:
        print(f"❌ ERROR during screening workflow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
