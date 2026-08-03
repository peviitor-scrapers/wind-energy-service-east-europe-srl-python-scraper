# INSTRUCTIONS

## 1. Prerequisites

```bash
python3 -m pip install -r requirements.txt
```

## 2. Run the scraper

```bash
python3 -m scraper.index
```

This will:

1. Query existing jobs in peviitor SOLR for CIF `9256208`.
2. Validate the company via ANAF (fallback CUIScan).
3. Upsert the company core (with `scraperFile`).
4. Scrape the applytojob board filtered by `?department=ELECTROGRUP`.
5. Merge ANOFM jobs (unless `--test`).
6. Transform jobs (Romanian city filter, workmode normalization).
7. Write `scraper/jobs.json`, `docs/jobs.md`, `docs/company.json`.
8. Upsert jobs to SOLR via `/v1/scraper/jobs/upload/`.
9. Delete stale jobs via `/v1/scraper/jobs/delete/`.

## 3. Validate job URLs

```bash
python3 -m scraper.validate_jobs 9256208 --mode head      # dry check
python3 -m scraper.validate_jobs 9256208 --mode content   # content check
python3 -m scraper.validate_jobs 9256208 --delete         # delete invalid
```

## 4. Tests

```bash
python3 -m pytest tests/unit tests/consistency   # offline
python3 -m pytest tests/integration              # live APIs (skip-safe)
python3 -m pytest tests/e2e                      # real board (skip-safe)
python3 -m pytest                                # everything
```

## 5. GitHub Actions

- `job-seeker-ro-spider.yml` — scheduled scrape (cron) + dispatch.
- `automation-testing.yml` — runs unit/consistency tests on every push.
- `job-deep-validate.yml` — validates job URLs on demand.
- `job-recovery-from-disaster.yml` — rebuild from backup on demand.
