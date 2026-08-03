# AI Derivation Guide — Creating or Recreating a Scraper from this Template

**Audience:** AI agents tasked with deriving a new Python scraper from this ELECTROGRUP template for a different Romanian company.

**Scope:** Every step from "user gave me a target company" to "CI is green and scraper runs daily, jobs visible on peviitor.ro".

> **AI agents: after applying this guide to a derived repo, DELETE this file from the derived repo. It belongs only in the Python template.**

---

## 0. Decision tree — Use this guide when:

- User asks to create a scraper for company X → **CREATE flow**
- User asks to recreate / rewrite an existing scraper repo → **RECREATE flow** (delete + recreate via template)
- User points to an existing repo that wasn't created via template → **RECREATE flow** (badge won't appear unless re-done via template)

If unsure, ask the user.

---

## 1. Prerequisites

Before starting, confirm:

1. **`gh` CLI is authenticated** (`gh auth status`)
2. **Target company info is known**:
   - Legal name (`SRL`, `SA`, `SCA` — get the real one, may differ from repo slug)
   - CIF (Romanian fiscal code; can be 7-9 digits)
   - Brand (commercial name, may differ from legal)
   - Career URL
3. **Target site is understood** — fetch the career page first to identify:
   - JSON API? HTML scrape with BeautifulSoup? POST AJAX returning HTML?
   - Pagination? Filters? Required headers/cookies?
4. **Python template is in `is_template: true` state** (check via `gh api repos/peviitor-scrapers/electrogrup-sa-python-scraper -q .is_template`)

---

## 2. CREATE flow — fresh new scraper

### 2.1 Create repo from template (gets the "Generated from" badge)

```bash
gh repo create peviitor-scrapers/<slug>-python-scraper \
  --template peviitor-scrapers/electrogrup-sa-python-scraper \
  --public \
  --description "Scraper automat pentru locurile de muncă <LEGAL_NAME> (CIF: <CIF>) — extrage de pe <CAREER_URL> și publică pe peviitor.ro"
```

**Verify the badge is set:**

```bash
gh api repos/peviitor-scrapers/<slug>-python-scraper -q '.template_repository.full_name'
# expect: peviitor-scrapers/electrogrup-sa-python-scraper
```

If the badge is missing → the repo was created without `--template`. Delete and retry.

### 2.2 Clone locally

```bash
git clone https://github.com/peviitor-scrapers/<slug>-python-scraper.git
cd <slug>-python-scraper
```

---

## 3. RECREATE flow — replace an existing repo

The badge "Generated from" can only appear if the repo is created via the template feature. If the existing repo was created manually, you must delete and recreate.

### 3.1 Learn from the existing repo first

```bash
gh api repos/peviitor-scrapers/<slug>-python-scraper/contents/scraper/index.py -q .content | base64 -d
gh api repos/peviitor-scrapers/<slug>-python-scraper/contents/scraper/config/company.json -q .content | base64 -d 2>/dev/null
```

Identify:
- **Identity** — CIF, legal name, brand
- **Scraping URL + method** (API/HTML/AJAX)
- **Selectors / API params** (e.g. POST body, BeautifulSoup selectors)
- **City/workmode rules** (defaults, mappings)

### 3.2 Delete and recreate

```bash
gh repo delete peviitor-scrapers/<slug>-python-scraper --yes
# then follow Section 2 (CREATE flow)
```

---

## 4. Apply company-specific changes

**Single edit point principle:** the template was designed so the only file you edit for identity is `scraper/config/company.json`. All scraper code, CI workflows, and the static HTML read from this file.

### 4.1 Edit `scraper/config/company.json`

```json
{
  "id": "<CIF/CUI, 8 digits>",
  "company": "<COMPANY NAME LEGAL>",
  "brand": "<Commercial brand>",
  "status": "activ",
  "location": ["<city>"],
  "website": ["https://..."],
  "career": ["https://..."],
  "scraperFile": "https://github.com/peviitor-scrapers/<slug>-python-scraper/actions/workflows/job-seeker-ro-spider.yml"
}
```

Edit `scraper/config/scraper.json` for the board base/path/department filter. Also overwrite `docs/company.json` with the same content — it's the copy served by GitHub Pages.

### 4.2 Rewrite `scraper/index.py` scraping logic

Only the listing/scrape functions should be company-specific: `build_listing_url`, `fetch_listing`, `parse_api_jobs`. The rest (mapping, transformation, SOLR upsert, markdown generation) is generic — do not change.

**Common scraping patterns:**

| Pattern | Approach |
|---------|----------|
| Paginated JSON API | GET + loop pages until empty |
| Single-page HTML | GET, BeautifulSoup selector on response |
| POST AJAX → HTML | POST with form params, BeautifulSoup on response |
| Teamtailor HTML | GET, navigate team-tailor-style markup |

**Probe the endpoint first** with `curl` to see what params are required.

### 4.3 Delete stale ANAF cache + stale published jobs.md

```bash
rm -f scraper/anaf_cache.json   # template's ANAF cache (ELECTROGRUP identity)
rm -f docs/jobs.md              # template's last scraped jobs
rm -f scraper/jobs.json         # last scraped jobs payload
```

Both files are regenerated automatically on the first scrape.

---

## 5. Update tests (mandatory — CI gates on them)

The template has 4 test layers; ALL must pass before merge.

### 5.1 `tests/unit/test_index.py` — rewrite the parser block

Replace the applytojob parser tests with tests for your new parser:
- Use an HTML fixture matching your target site's response
- Test title/URL/location/workmode extraction
- Test edge cases (empty response, missing fields)

### 5.2 `tests/unit/test_anaf.py` — update the ANAF mock constant

Rename `ELECTROGRUP` mock data to match the new ANAF/CUIScan response.

### 5.3 `tests/unit/test_api.py` — CIF is used as-is

CIFs are never zero-padded. Update hardcoded CIFs if needed.

### 5.4 `tests/integration/test_company_real.py` — make config-driven

Replace hardcoded `COMPANY_CIF` with the config value. For ANAF searches that return multiple matches, find by CIF (deterministic).

### 5.5 `tests/e2e/test_scraper.py` — rewrite fully

Replace the applytojob scrape with your new scraping method. Adjust `EXPECTED_MIN_JOBS`. Increase timeout if your target site is in Romania (Azure GH runners are slow to RO IPs).

### 5.6 `tests/consistency/test_repo.py` — make brand assertions dynamic

Read the brand from `company.json` instead of hardcoding `ELECTROGRUP SA`.

---

## 6. Documentation sweep

After bulk rename (via `sed` or manual), do these manual review passes:

1. **README.md** — restore the "Template repo" link (sed will have changed it to be self-referential)
2. **CONTRIBUTING.md** — replace the inherited "Deriving a New Scraper" checklist with a slim intro pointing back to the Python template
3. **AGENTS.md** — change "🌱 Template repo" to "🌱 Derived Scraper" wording as appropriate
4. **ROBOTS.md** — analyze the new target site's `robots.txt`
5. **CHANGELOG.md** — REPLACE with a fresh `1.0.0` entry
6. **docs/index.html** — i18n strings still contain "ELECTROGRUP". Replace with new brand.
7. **`scraper/job_validator.py` / `scraper/validate_jobs.py`** — update `DEFAULT_EXPIRED_KEYWORDS` for the new site if needed

---

## 7. CI configuration

### 7.1 Verify the critical CI ordering

These two ordering rules are NOT optional — both came from production CI failures:

1. **`Sync with remote` step MUST run BEFORE `Install dependencies`**. `pip install` modifies `requirements.txt`, which breaks the subsequent rebase.
2. **`Sync with remote` step MUST have `if: github.event_name != 'pull_request'`**. PR runs lack git identity, so the rebase aborts.

Verify with:

```bash
grep -B1 -A2 "Sync with remote" .github/workflows/*.yml
```

Expected output for each workflow:
```yaml
- name: Sync with remote
  if: github.event_name != 'pull_request'
  run: git pull origin main --rebase -X theirs
- name: Install dependencies
  run: |
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
```

---

## 8. GitHub repo settings

```bash
# Topics (required by consistency tests)
gh repo edit peviitor-scrapers/<slug>-python-scraper \
  --add-topic job-seeker-ro-spider \
  --add-topic peviitor-ro

# Homepage URL (set after Pages is enabled)
gh repo edit peviitor-scrapers/<slug>-python-scraper \
  --homepage "https://peviitor-scrapers.github.io/<slug>-python-scraper/"

# Enable GitHub Pages from /docs on main
gh api -X POST repos/peviitor-scrapers/<slug>-python-scraper/pages \
  -f source[branch]=main \
  -f source[path]=/docs
```

**No secrets needed.** The Peviitor API is public, no auth.

---

## 9. Verify locally before pushing

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest tests/unit tests/consistency   # Must pass before push
python3 -m pytest tests/e2e                      # live scrape probe
```

Probe your scraping logic against the real site to confirm at least one job is parsed correctly.

---

## 10. Commit, push, trigger CI

```bash
git add -A
git commit -m "feat: convert template into <COMPANY> scraper

Derived from peviitor-scrapers/electrogrup-sa-python-scraper."
git push

# Trigger CI to verify
gh workflow run job-seeker-ro-spider.yml --repo peviitor-scrapers/<slug>-python-scraper
```

**Watch for typical failures**:
- "Sync with remote" failing → CI workflow ordering wrong (see Section 7.1)
- "Run Integration Tests" → likely sed mangling (see Pitfall #1)
- "Run E2E Tests" timeout → bump timeout
- "Consistency tests" → Pages not deployed yet OR homepage URL not set

---

## 11. Update template's "Derived Scrapers" table

After CI is green, add the new repo to the Python template's README:

```markdown
| [<slug>-python-scraper](https://github.com/peviitor-scrapers/<slug>-python-scraper) | <Legal Name> | <CIF> | <Method, e.g. HTML/BeautifulSoup> | ✅ Live |
```

---

## 12. Pitfalls (read before each derivation)

### Pitfall #1 — Bulk sed creates mangled identifiers

Use word-boundary patterns: `sed -i 's/\bELECTROGRUP\b/newbrand/g'`. After every bulk sed, run:

```bash
grep -rnE '\b[a-z]+\.[a-z]+\b' --include="*.py" .
python3 -c "import ast; ast.parse(open('scraper/index.py').read())"  # syntax check
python3 -m pytest tests/unit   # full validation
```

### Pitfall #2 — ANAF returns multiple matches

If you search ANAF by brand name and assert the first result is your company, you're wrong. Always find by CIF (deterministic).

### Pitfall #3 — SOLR may uppercase brand on store

Always use `.lower()` on both sides of brand comparisons in integration tests.

### Pitfall #4 — `lastScraped` format inconsistency

Make test regex permissive: `r"^\d{4}-\d{2}-\d{2}(T.*)?$"`.

### Pitfall #5 — E2E timeout from Azure runners

Romania-hosted sites are often slow from GH Actions Azure runners. Use generous timeouts.

### Pitfall #6 — CIF length varies

Romanian CIFs are NOT always 8 digits (older companies have 7, 6, even 4 digits). **Never zero-pad a CIF** — use it exactly as it appears in `company.json`.

### Pitfall #7 — Stale ANAF cache from template

The template ships `scraper/anaf_cache.json` containing ELECTROGRUP's ANAF data. The caching logic reads this first and skips ANAF for the derived company. **Always `rm -f scraper/anaf_cache.json` early in derivation.**

### Pitfall #8 — "Generated from" badge requires template feature

The ONLY way to add the badge retroactively is to delete and recreate via the template.

### Pitfall #9 — Forgot to update the template's "Derived Scrapers" list

This is the last manual step and easy to miss.

### Pitfall #10 — Stale `docs/jobs.md` from template gets sed-mangled into fake URLs

Bulk sed rewrites brand strings but keeps job paths/IDs, producing plausible-looking but fake URLs. Delete `docs/jobs.md` early (see Section 4.3).

### Pitfall #11 — ANOFM jobs are silently lost

The ANOFM public API (`/api/entity/vw_public_job_posting`) accepts a POST with `employer_tax_code` filter (the company's CIF). Each result includes `occupation` (title), `address_locality_name` (location in "County > City > Locality" format), and `id` (job URL `https://mediere.anofm.ro/app/module/mediere/job/{id}`). Always call `search_anofm` and merge results to avoid data loss.

---

## 13. Issue tracking rule

**File a GitHub issue for every fix you apply that isn't a typo.** When the fix is template-wide, file in the Python template. When company-specific, file in the derived scraper.

---

## 14. Reference: past derivations as worked examples

| Repo | Method | CIF | Notable |
|------|--------|-----|---------|
| [electrogrup-sa-python-scraper](https://github.com/peviitor-scrapers/electrogrup-sa-python-scraper) | HTML/BeautifulSoup (applytojob) | 9256208 | Template (this repo) |

---

## 15. Source issues feeding this guide

This guide is synthesized from the EPAM Node.js template's `ai/AI-DERIVATION-GUIDE.md` (issues #34–#38, Continental #1–#9, RAPEL #1–#2), adapted for Python.

---

**End of guide.** If you encounter a NEW class of pitfall not covered here, file an issue and update this guide.
