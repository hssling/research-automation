"""
Upload ALL files under ./dist to Zenodo and publish the record.
- Reads metadata from ./metadata.yaml (YAML → Zenodo JSON).
- Uses ZENODO_TOKEN from environment.
- Uses production Zenodo by default; override with ZENODO_API_URL (e.g., https://sandbox.zenodo.org/api).
- Optional environment variables:
    ZENODO_CONCEPTRECID: If set, version this deposition under an existing concept DOI.
    ZENODO_ACCESS_RIGHT: "open" (default) | "embargoed" | "restricted" | "closed"
    ZENODO_EMBARGO_DATE: YYYY-MM-DD (if embargoed)
    ZENODO_PUBLISH: "true" (default) to publish; "false" to leave as draft.
"""
import os, sys, json, requests, mimetypes
from pathlib import Path

try:
    import yaml  # pyyaml
except ImportError:
    print("Please install pyyaml: pip install pyyaml")
    sys.exit(1)

DIST_DIR = Path("dist")
META_YAML = Path("metadata.yaml")

API_BASE = os.getenv("ZENODO_API_URL", "https://zenodo.org/api")
DEPOSIT_URL = f"{API_BASE}/deposit/depositions"
TOKEN = os.getenv("ZENODO_TOKEN")
if not TOKEN:
    print("ERROR: ZENODO_TOKEN is not set. Export it or add as GitHub Secret.")
    sys.exit(2)
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

PUBLISH = os.getenv("ZENODO_PUBLISH", "true").lower() == "true"
ACCESS_RIGHT = os.getenv("ZENODO_ACCESS_RIGHT", "open")
EMBARGO_DATE = os.getenv("ZENODO_EMBARGO_DATE", None)
CONCEPTRECID = os.getenv("ZENODO_CONCEPTRECID", None)

def load_metadata():
    if not META_YAML.exists():
        print("ERROR: metadata.yaml not found at repo root.")
        sys.exit(3)
    meta = yaml.safe_load(META_YAML.read_text(encoding="utf-8"))
    md = {
        "metadata": {
            "title": meta.get("title", "Untitled Zenodo Deposition"),
            "upload_type": meta.get("upload_type", "publication"),
            "publication_type": meta.get("publication_type", "preprint"),
            "description": meta.get("description", "Auto-generated deposition."),
            "creators": meta.get("creators", []),
            "keywords": meta.get("keywords", []),
            "language": meta.get("language", "eng"),
        }
    }
    for key in [
        "notes","communities","contributors","related_identifiers",
        "references","grants","imprint_publisher","imprint_place","partof_title",
        "doi","prereserve_doi","journal_title","journal_volume","journal_issue",
        "journal_pages","conference_title","conference_acronym","conference_dates",
        "conference_place","conference_url"
    ]:
        if key in meta and meta[key] not in (None, []):
            md["metadata"][key] = meta[key]

    md["metadata"]["access_right"] = ACCESS_RIGHT
    if ACCESS_RIGHT == "embargoed" and EMBARGO_DATE:
        md["metadata"]["embargo_date"] = EMBARGO_DATE

    if CONCEPTRECID:
        md["metadata"]["conceptrecid"] = CONCEPTRECID

    return md

def create_deposition():
    r = requests.post(DEPOSIT_URL, headers=HEADERS, json={})
    if r.status_code >= 300:
        print("Create deposition failed:", r.status_code, r.text)
        sys.exit(4)
    return r.json()

def update_metadata(dep_id, metadata):
    r = requests.put(f"{DEPOSIT_URL}/{dep_id}", headers=HEADERS, json=metadata)
    if r.status_code >= 300:
        print("Metadata update failed:", r.status_code, r.text)
        sys.exit(5)
    return r.json()

def upload_file(dep_id, file_path: Path):
    files_url = f"{DEPOSIT_URL}/{dep_id}/files"
    with file_path.open("rb") as fp:
        data = {"name": file_path.name}
        r = requests.post(files_url, headers=HEADERS, data=data, files={"file": fp})
    if r.status_code >= 300:
        print(f"File upload failed for {file_path}: {r.status_code} {r.text}")
        sys.exit(6)

def publish(dep_id):
    r = requests.post(f"{DEPOSIT_URL}/{dep_id}/actions/publish", headers=HEADERS)
    if r.status_code >= 300:
        print("Publish failed:", r.status_code, r.text)
        sys.exit(7)
    return r.json()

def main():
    if not DIST_DIR.exists():
        print("ERROR: ./dist directory not found. Put your files to upload inside ./dist")
        sys.exit(8)
    files = [p for p in DIST_DIR.rglob("*") if p.is_file()]
    if not files:
        print("ERROR: No files found under ./dist")
        sys.exit(9)

    dep = create_deposition()
    dep_id = dep["id"]
    print("Created Zenodo deposition ID:", dep_id)

    md = load_metadata()
    dep = update_metadata(dep_id, md)
    conceptdoi = dep.get("conceptdoi")
    print("Concept DOI:", conceptdoi)

    for f in files:
        rel = f.relative_to(DIST_DIR)
        print("Uploading:", rel)
        upload_file(dep_id, f)

    if PUBLISH:
        pub = publish(dep_id)
        doi = pub.get("doi") or pub.get("metadata", {}).get("prereserve_doi", {}).get("doi")
        html_url = pub.get("links", {}).get("html")
        print("✅ Published! DOI:", doi)
        print("🔗 Record URL:", html_url)
        Path("zenodo_result.json").write_text(json.dumps(pub, indent=2), encoding="utf-8")
    else:
        print("📝 Draft created. Not publishing (ZENODO_PUBLISH != true).")
        Path("zenodo_result.json").write_text(json.dumps(dep, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
