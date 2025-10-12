import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import date

# Output folder
OUTPUT_DIR = "synbiotics_postbiotics_mdr_tb"
os.makedirs(OUTPUT_DIR, exist_ok=True)
today = date.today().isoformat()


def clean_text(s):
    if not s:
        return ""
    return re.sub(r"\W+", " ", str(s)).strip().lower()


def pubmed_search():
    print("[1/5] PubMed Search...")
    query = "(multidrug-resistant tuberculosis OR MDR tuberculosis) AND (synbiotic OR postbiotic OR probiotic OR prebiotic OR microbiome)"
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": 200}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    ids = resp.json()["esearchresult"]["idlist"]

    records = []
    if ids:
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        fetch_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
        fetch_resp = requests.get(fetch_url, params=fetch_params)
        fetch_resp.raise_for_status()
        summaries = fetch_resp.json()["result"]
        for pid in ids:
            if pid in summaries:
                item = summaries[pid]
                records.append({
                    "source": "PubMed",
                    "id": pid,
                    "title": item.get("title"),
                    "doi": item.get("elocationid"),
                    "year": item.get("pubdate", "").split(" ")[0],
                })

    print(f"✓ PubMed: {len(records)} records")
    return records


def clinicaltrials_search():
    print("[2/5] ClinicalTrials.gov Search...")
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": "multidrug-resistant tuberculosis OR MDR tuberculosis",
        "query.term": "synbiotic OR postbiotic OR probiotic OR prebiotic OR microbiome",
        "pageSize": 100,
        "countTotal": "true",
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    studies = []
    for s in data.get("studies", []):
        idn = s.get("protocolSection", {}).get("identificationModule", {})
        title = idn.get("officialTitle") or idn.get("briefTitle")
        studies.append({
            "source": "ClinicalTrials.gov",
            "id": idn.get("nctId"),
            "title": title,
            "doi": None,
            "year": s.get("protocolSection", {}).get("statusModule", {}).get("startDateStruct", {}).get("year"),
        })
    print(f"✓ ClinicalTrials.gov: {len(studies)} records")
    return studies


def who_ictrp_search():
    print("[3/5] WHO ICTRP CSV Download...")
    url = "https://trialsearch.who.int/export/trialsearch.csv"
    resp = requests.get(url)
    resp.raise_for_status()

    df = pd.read_csv(StringIO(resp.text))
    keywords = ["MDR", "multidrug", "tuberculosis", "probiotic", "synbiotic", "postbiotic", "prebiotic", "microbiome"]
    mask = df.apply(lambda row: any(k.lower() in str(row).lower() for k in keywords), axis=1)
    filtered = df[mask]

    records = []
    for _, row in filtered.iterrows():
        records.append({
            "source": "WHO ICTRP",
            "id": row.get("TrialID"),
            "title": row.get("Scientific_title"),
            "doi": None,
            "year": row.get("Date_registration")[:4] if pd.notna(row.get("Date_registration")) else None,
        })
    print(f"✓ WHO ICTRP: {len(records)} matching trials")
    return records


def crossref_search():
    print("[4/5] CrossRef Search...")
    url = "https://api.crossref.org/works"
    params = {
        "query": "multidrug-resistant tuberculosis synbiotic postbiotic probiotic prebiotic microbiome",
        "rows": 100,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    records = []
    for item in data["message"]["items"]:
        records.append({
            "source": "CrossRef",
            "id": item.get("DOI"),
            "title": item.get("title", [""])[0],
            "doi": item.get("DOI"),
            "year": item.get("created", {}).get("date-parts", [[None]])[0][0],
        })
    print(f"✓ CrossRef: {len(records)} records")
    return records


def cochrane_scrape():
    print("[5/5] Cochrane Scrape...")
    search_url = "https://www.cochranelibrary.com/cdsr/reviews/topics?searchTerm=MDR%20tuberculosis%20synbiotic"
    resp = requests.get(search_url)
    if resp.status_code != 200:
        print("✗ Cochrane search failed")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    titles = [a.text.strip() for a in soup.find_all("a", class_="result-title")]
    records = [{"source": "Cochrane", "id": None, "title": t, "doi": None, "year": None} for t in titles]
    print(f"✓ Cochrane: {len(records)} records")
    return records


def deduplicate(records):
    seen = set()
    unique = []
    for r in records:
        key = clean_text(r.get("title")) or r.get("doi") or r.get("id")
        if key and key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def main():
    all_records = []
    try:
        all_records.extend(pubmed_search())
    except Exception as e:
        print(f"PubMed search failed: {e}")

    try:
        all_records.extend(clinicaltrials_search())
    except Exception as e:
        print(f"ClinicalTrials.gov search failed: {e}")

    try:
        all_records.extend(who_ictrp_search())
    except Exception as e:
        print(f"WHO ICTRP search failed: {e}")

    try:
        all_records.extend(crossref_search())
    except Exception as e:
        print(f"CrossRef search failed: {e}")

    try:
        all_records.extend(cochrane_scrape())
    except Exception as e:
        print(f"Cochrane search failed: {e}")

    print("\n[Deduplication]")
    unique_records = deduplicate(all_records)
    print(f"Total before deduplication: {len(all_records)}")
    print(f"Total unique after deduplication: {len(unique_records)}")

    # Save JSON
    out_json = os.path.join(OUTPUT_DIR, f"improved_search_results_{today}.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2)

    # Save CSV
    out_csv = os.path.join(OUTPUT_DIR, f"improved_deduplicated_results_{today}.csv")
    pd.DataFrame(unique_records).to_csv(out_csv, index=False)

    print("\n============================================================")
    print("IMPROVED SEARCH EXECUTION SUMMARY")
    print("============================================================")
    print(f"Total Records Collected: {len(all_records)}")
    print(f"After Deduplication: {len(unique_records)}")
    print(f"JSON saved: {out_json}")
    print(f"CSV saved:  {out_csv}")


if __name__ == "__main__":
    main()
