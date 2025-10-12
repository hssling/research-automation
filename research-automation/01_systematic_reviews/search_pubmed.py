#!/usr/bin/env python3
"""
Fetch articles from PubMed using Entrez API.
"""

import argparse
from Bio import Entrez
import time
import pandas as pd

def fetch_pubmed(query, retmax, outfile, email="your.email@example.com"):
    Entrez.email = email
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    record = Entrez.read(handle)
    ids = record["IdList"]

    # fetch details
    summaries = []
    for pmid in ids:
        time.sleep(0.3)  # be nice to NCBI
        fetch = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="xml")
        article = Entrez.read(fetch)
        summaries.append(article)

    # save as DataFrame
    rows = []
    for art in summaries:
        if "MedlineCitation" in art[0]:
            cit = art[0]["MedlineCitation"]
            art_title = cit["Article"]["ArticleTitle"]
            pmid = cit["PMID"]
            journal = cit["Article"]["Journal"]["Title"]
            rows.append({"PMID": pmid, "Title": art_title, "Journal": journal})

    df = pd.DataFrame(rows)
    df.to_csv(outfile, index=False)
    print(f"✅ Saved {len(df)} articles to {outfile}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="PubMed search query")
    parser.add_argument("--retmax", type=int, default=1000, help="Max results to fetch")
    parser.add_argument("--out", required=True, help="Output CSV file")
    args = parser.parse_args()

    fetch_pubmed(args.query, args.retmax, args.out)
