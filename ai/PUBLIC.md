# PUBLIC.md — Repository Must Be PUBLIC

All scrapers derived from the template **MUST** be **PUBLIC** repositories.

## Why?

- Peviitor is an open-source platform
- Job data should be accessible to everyone
- Transparency builds trust

## Enforcement

Keep the repository public. The repo is public and hosted at:

- Repository: https://github.com/peviitor-scrapers/wind-energy-service-east-europe-srl-python-scraper
- GitHub Pages: https://peviitor-scrapers.github.io/wind-energy-service-east-europe-srl-python-scraper/ (`docs/` on `main`, built automatically)
- Scraper workflow: https://github.com/peviitor-scrapers/wind-energy-service-east-europe-srl-python-scraper/actions/workflows/job-seeker-ro-spider.yml
- Jobs page: `docs/jobs.md` (generated, committed, served on GitHub Pages)
- Peviitor search: https://peviitor.ro (CIF `26669972`)

## How to check

```bash
gh repo view peviitor-scrapers/wind-energy-service-east-europe-srl-python-scraper --json visibility
```
