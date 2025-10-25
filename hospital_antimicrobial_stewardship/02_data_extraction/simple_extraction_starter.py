#!/usr/bin/env python3
"""
Simple Extraction Starter for Hospital Antimicrobial Stewardship
Systematic Review - Batch 2 (Mortality Studies)

This script demonstrates starting the systematic data extraction workflow
for the deployed high-impact mortality studies batch.

Author: Research Team
Date: October 13, 2025
"""

import pandas as pd
import json
import os
from datetime import datetime

def main():
    """Main function to demonstrate extraction initiation."""

    print("🏥 HOSPITAL ANTIMICROBIAL STEWARDSHIP SYSTEMATIC REVIEW")
    print("=" * 70)
    print("📊 PHASE 3: Data Extraction - BATCH 2 INITIATION")
    print("⭐ Priority: High-Impact Mortality Studies")
    print("=" * 70)

    # File paths for Batch 2
    batch_package = "batch_2_extraction_instructions_20251013_143454.txt"
    batch_studies = "batch_2_studies_20251013_143454.csv"
    batch_forms = "batch_extraction_package_20251013_143454.json"

    print("🔍 BATCH 2 DEPLOYMENT SUMMARY:")
    print("-" * 50)
    print("📋 Studies: 2 High-Impact Mortality Studies")
    print("⏱️  Estimated Time: 100 minutes total (45-60 min per study)")
    print("🎯 Focus Areas: mortality, cdi, mdro, antibiotic_consumption, length_stay")
    print("📅 Deadline: October 27, 2025")

    print("
📚 ASSIGNED STUDIES:"    print("-" * 30)

    if os.path.exists(batch_studies):
        studies_df = pd.read_csv(batch_studies)
        for _, study in studies_df.iterrows():
            print(f"🔗 PMID {study['pmid']}: {study['study_id']}")
            print(f"   📖 Title: {study.get('title', 'N/A')[:80]}...")
            print(f"   ⭐ Priority: {study.get('priority_level', 'N/A')}")
            print()

    print("🚀 ARTICLE ACCESS WORKFLOW:")
    print("-" * 35)
    print("1. Open PubMed links for each PMID above")
    print("2. Click 'Full text links' to find free/full access")
    print("3. Use institutional library access if needed")
    print("4. Check PMC full text availability")
    print("5. Download PDFs and note access date/source")

    print("
📝 SYSTEMATIC EXTRACTION SEQUENCE:"    print("-" * 40)
    print("1. Study Characteristics (15-20 min)")
    print("   → Basic study info, design, population, setting")
    print()
    print("2. Intervention Details (20-25 min)")
    print("   → Complete intervention characterization")
    print()
    print("3. Outcome Data (25-30 min)")
    print("   → All effect estimates with confidence intervals")
    print()
    print("4. Quality Assessment (15-20 min)")
    print("   → Domain-specific risk of bias evaluation")
    print()
    print("5. Cross-Validation (10 min)")
    print("   → Internal consistency checks")

    print("
✅ QUALITY CONTROL REQUIREMENTS:"    print("-" * 42)
    print("• Double extraction: 50% of studies (both studies)")
    print("• Discrepancy resolution: Third reviewer arbitration")
    print("• Agreement threshold: 100% on key variables")

    print("
🔧 AVAILABLE FILES FOR EXTRACTION:"    print("-" * 40)
    print(f"• Study list: {batch_studies}")
    print(f"• Extraction forms: {batch_forms}")
    print(f"• Instructions: {batch_package}")

    print("
🎯 EXTRACTION READY TO BEGIN!"    print("🔬 Researchers can now start systematic data extraction")
    print(f"🏁 Extraction Deadline: October 27, 2025")

    # Create quick progress tracker
    print("
📊 CREATING EXTRACTION PROGRESS TRACKER..."    if os.path.exists(batch_studies):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tracker_file = f"batch_2_extraction_progress_{timestamp}.csv"

        progress_data = []
        for _, study in studies_df.iterrows():
            progress_data.append({
                'study_id': study['study_id'],
                'pmid': study['pmid'],
                'batch_number': 2,
                'priority_level': study.get('priority_level', ''),
                'access_status': 'Pending',
                'access_date': '',
                'extraction_status': 'Not Started',
                'extractor_initials': '',
                'completion_date': '',
                'double_extraction': 'Yes',  # Both for quality
                'verification_status': 'Pending',
                'notes': ''
            })

        progress_df = pd.DataFrame(progress_data)
        progress_df.to_csv(tracker_file, index=False)
        print(f"✅ Progress tracker created: {tracker_file}")

    print("
🏆 BATCH 2 EXTRACTION WORKFLOW INITIATED!"    print("📝 Research team can now begin systematic data extraction.")

if __name__ == "__main__":
    main()
