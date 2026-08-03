# VERIFY

How to verify the scraper works.

## Offline

```bash
python3 -m pytest tests/unit tests/consistency
```

Expect: all green, no network needed.

## Live — company

```bash
python3 -c "from scraper.anaf import get_company_from_anaf; print(get_company_from_anaf('9256208'))"
```

Expect: `denumire == "ELECTROGRUP SA"`, `cif == "9256208"`.

## Live — board

```bash
python3 -m pytest tests/e2e
```

Expect: `>= 40` jobs scraped, unique URLs, titles present.

## Live — peviitor SOLR

```bash
curl "https://api.peviitor.ro/v1/scraper/jobs/?cif=09256208&rows=500"
```

Expect: `success: true` and `data` matching the scraped job count.

## Full pipeline

```bash
python3 -m scraper.index
```

Then check:

- `scraper/jobs.json` exists and has jobs.
- `docs/jobs.md` regenerated with the job list.
- `docs/company.json` mirrors `scraper/config/company.json`.
- SOLR count matches scraped count (minus filtered locations).
