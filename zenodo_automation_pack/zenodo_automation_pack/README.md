# Zenodo Automation Pack

Automate **publishing everything in `./dist` to Zenodo** with DOI minting.

## Steps
1. Place files to upload in `./dist/` (PDF, figures, data, code).
2. Edit `metadata.yaml` (title, description, keywords, creators).
3. Export your token:
   ```bash
   export ZENODO_TOKEN=YOUR_LONG_TOKEN
   ```
4. Run:
   ```bash
   python upload_to_zenodo.py
   ```

### Options
- `ZENODO_API_URL` (default prod `https://zenodo.org/api`; use sandbox for tests)
- `ZENODO_PUBLISH` = "true" (default) or "false"
- `ZENODO_ACCESS_RIGHT` = open | embargoed | restricted | closed
- `ZENODO_EMBARGO_DATE` = YYYY-MM-DD
- `ZENODO_CONCEPTRECID` = version under existing concept DOI

### GitHub Actions
- Add secret `ZENODO_TOKEN`, then tag `publish-*` to trigger.

---
Preset **creator**:
- Dr. Siddalingaiah H. S., Professor of Community Medicine, SIMS&RH, Tumkur, India. ORCID: 0000-0002-4771-8285
