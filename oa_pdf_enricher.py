#!/usr/bin/env python3
"""
Open Access PDF Enricher for Literature Search Results

This script enriches literature search results with free PDF links from:
1. Unpaywall API - Extensive OA database
2. Semantic Scholar - Academic research database
3. CORE - CORE repository (free access)

Usage:
python oa_pdf_enricher.py

Requires:
- pandas
- requests
- Email for Unpaywall API (sign up at unpaywall.org)

This enhances systematic review workflows by automatically finding free PDFs
for discovered literature.
"""

import pandas as pd
import requests
import time
import os

# CONFIG
INPUT_CSV = "synbiotics_postbiotics_mdr_tb/improved_deduplicated_results_2025-09-25.csv"
OUTPUT_CSV = "synbiotics_postbiotics_mdr_tb/deduplicated_results_with_oa.csv"
UNPAYWALL_EMAIL = "research@example.com"   # TODO: Replace with actual email

def check_unpaywall(doi):
    """Check Unpaywall for OA PDF availability"""
    if not doi:
        return None
    url = f"https://api.unpaywall.org/v2/{doi}"
    try:
        resp = requests.get(url, params={"email": UNPAYWALL_EMAIL}, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            oa_location = data.get("best_oa_location")
            if oa_location and "url_for_pdf" in oa_location:
                return oa_location["url_for_pdf"]
    except Exception as e:
        print(f"Unpaywall error for {doi}: {e}")
    return None

def check_semanticscholar(doi):
    """Check Semantic Scholar for OA PDF availability"""
    if not doi:
        return None
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    params = {"fields": "url,isOpenAccess,openAccessPdf"}
    try:
        resp = requests.get(url, params=params, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("isOpenAccess") and data.get("openAccessPdf"):
                return data["openAccessPdf"].get("url")
    except Exception as e:
        print(f"S2 error for {doi}: {e}")
    return None

def check_core(title, api_key=None):
    """Check CORE repository for OA PDF (limited without API key)"""
    # CORE needs an API key for full use, but public search is possible with query
    if not title:
        return None
    url = "https://core.ac.uk:443/api-v2/search/works"
    params = {"q": title, "page": 1, "pageSize": 1}
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results"):
                fulltext = data["results"][0].get("downloadUrl")
                return fulltext
    except Exception as e:
        print(f"CORE error for {title}: {e}")
    return None

def enrich_with_oa(df):
    """Enrich dataframe with OA PDF links"""
    oa_urls = []
    for i, row in df.iterrows():
        doi = row.get("doi")
        title = row.get("title")
        oa_link = None

        # Try Unpaywall first (most comprehensive)
        if doi:
            oa_link = check_unpaywall(doi)
            if oa_link:
                print(f"[{i+1}/{len(df)}] ✅ Unpaywall: {title[:60]}...")

        # Try Semantic Scholar if not found
        if not oa_link and doi:
            oa_link = check_semanticscholar(doi)
            if oa_link:
                print(f"[{i+1}/{len(df)}] ✅ S2: {title[:60]}...")

        # Try CORE as last resort
        if not oa_link and title:
            oa_link = check_core(title)
            if oa_link:
                print(f"[{i+1}/{len(df)}] ✅ CORE: {title[:60]}...")

        oa_urls.append(oa_link)
        if not oa_link:
            print(f"[{i+1}/{len(df)}] ❌ No OA found: {title[:60]}...")

        time.sleep(1)  # Be polite to APIs

    df["free_pdf_url"] = oa_urls
    return df

def main():
    """Main enrichment workflow"""
    print("🔍 Open Access PDF Enricher")
    print("=" * 50)

    if not os.path.exists(INPUT_CSV):
        print(f"❌ Input CSV not found: {INPUT_CSV}")
        print("Please ensure literature search has been completed first.")
        return

    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} records from {INPUT_CSV}")

    # Check email configuration
    if UNPAYWALL_EMAIL == "research@example.com":
        print("⚠️  Please configure UNPAYWALL_EMAIL with a real email address")
        print("   Get your API key at: unpaywall.org")
        return

    print("\n🎯 Starting OA PDF enrichment...")
    enriched = enrich_with_oa(df)

    # Calculate success rate
    oa_count = enriched['free_pdf_url'].notna().sum()
    success_rate = (oa_count / len(enriched)) * 100

    enriched.to_csv(OUTPUT_CSV, index=False)
    print(f"\n✅ OA-enriched results saved to {OUTPUT_CSV}")
    print(f"📊 OA Links Found: {oa_count}/{len(enriched)} ({success_rate:.1f}%)")

    # Summary report
    print("\nTop OA sources found:")
    oa_sources = []
    for _, row in enriched.iterrows():
        if pd.notna(row.get('free_pdf_url')):
            url = row['free_pdf_url']
            if 'unpaywall' in url.lower():
                oa_sources.append('Unpaywall')
            elif 'semanticscholar' in url.lower():
                oa_sources.append('Semantic Scholar')
            elif 'core' in url.lower():
                oa_sources.append('CORE')
            else:
                oa_sources.append('Other')

    from collections import Counter
    source_counts = Counter(oa_sources)
    for source, count in source_counts.most_common():
        print(f"  - {source}: {count} PDFs")

if __name__ == "__main__":
    main()
