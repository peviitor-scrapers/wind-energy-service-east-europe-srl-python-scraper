# Contributing

## Getting started

```bash
git clone git@github.com:peviitor-scrapers/electrogrup-sa-python-scraper.git
cd electrogrup-sa-python-scraper
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Code style

- Python 3.9+.
- No comments unless they explain *why* (mirrors repo conventions).
- Module-level docstrings; short function docstrings.
- Run tests before pushing:

```bash
python3 -m pytest tests/unit tests/consistency
```

## Adding a test

Add to the appropriate directory under `tests/`:

- `unit/` — mocked HTTP, no network.
- `integration/` — live APIs, `pytest.skip` when unreachable.
- `e2e/` — real board scrape, `pytest.skip` when unreachable.
- `consistency/` — repo identity and template conventions.

## Updating company data

Only edit `scraper/config/company.json` (single source of truth). After a
scrape, `docs/company.json` is regenerated automatically.
