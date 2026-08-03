# AGENTS.md

Instructions for AI agents working in this repository.

## Project

Python scraper that reads job listings from the ELECTROGRUP SA applytojob
board and publishes them to peviitor.ro through the **v1 API**
(`https://api.peviitor.ro/v1`). It is a Python port of the Node.js EPAM
template and must follow the same API contract.

## Commandments

1. **Never** call Solr directly — use the peviitor v1 API only.
2. Company CIFs are used **as-is** — never zero-pad or transform them.
3. Use `User-Agent: job_seeker_ro_spider`.
4. Edit `scraper/config/company.json` — it is the single source of truth.
5. Run `python3 -m pytest tests/unit tests/consistency` before pushing.
6. Do not add comments unless they explain *why*.
7. Do not commit secrets, `jobs.json`, or the ANAF cache.

## Quick commands

```bash
python3 -m pytest tests/unit tests/consistency   # fast tests (no network)
python3 -m pytest tests/e2e                      # real board scrape
python3 -m scraper.index                         # full scrape + publish
python3 -m scraper.validate_jobs 9256208 --head  # validate job URLs
```

## Key files

- `scraper/index.py` — entry point and orchestration.
- `scraper/api.py` — peviitor v1 client.
- `scraper/anaf.py` — ANAF + CUIScan company validation.
- `scraper/config/company.json` — company identity/config.
