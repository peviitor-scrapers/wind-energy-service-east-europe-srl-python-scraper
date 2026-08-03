# Issues

## Reporting

Open an issue in
[peviitor-scrapers/electrogrup-sa-python-scraper/issues](https://github.com/peviitor-scrapers/electrogrup-sa-python-scraper/issues).

## Common issues

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `0` jobs parsed | Board HTML changed | Update selectors in `scraper/index.py` |
| Company INACTIVE | ANAF status change | Do not scrape; jobs get deleted |
| API 401/403 | Token/endpoint change | Check `scraper/api.py` |
| Tests fail offline | Network-dependent test | Ensure `pytest.skip` on unreachable hosts |

## Escalation

For peviitor API problems, contact the peviitor maintainers with the CIF
`9256208` and the failing endpoint.
