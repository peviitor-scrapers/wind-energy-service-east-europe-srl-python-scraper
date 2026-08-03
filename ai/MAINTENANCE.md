# MAINTENANCE

## Routine

- The scheduled `job-seeker-ro-spider.yml` workflow scrapes daily.
- If the scrape fails, check: board reachability, ANAF API status, API response.
- Validate job URLs periodically:

```bash
python3 -m scraper.validate_jobs 9256208 --mode content --dry-run
python3 -m scraper.validate_jobs 9256208 --mode content --delete
```

## Board structure changes

If `parse_api_jobs` returns 0 or few jobs, inspect the applytojob page:

```bash
curl -s "https://electrogrup.applytojob.com/apply/jobs/?department=ELECTROGRUP"
```

Update the parser selectors in `scraper/index.py` (`a.job_title_link`,
`tr/td`) and the expected count in `tests/e2e/test_scraper.py`.

## Company data changes

Edit `scraper/config/company.json` only. Run the scraper to regenerate
`docs/company.json`.

## ANAF outages

`get_company_from_anaf` falls back demoanaf.ro → cuiscan.ro → cache
(`scraper/anaf_cache.json`). If all fail, the scraper errors clearly.
