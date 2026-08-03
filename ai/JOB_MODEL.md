# Job Model

Standardized job document published to peviitor SOLR.

## Fields

| Field           | Required | Description                                                        |
|-----------------|----------|--------------------------------------------------------------------|
| `url`           | yes      | Canonical job URL                                                   |
| `title`         | yes      | Job title                                                           |
| `company`       | no       | Company name (UPPERCASE, diacritics allowed)                        |
| `cif`           | no       | Company CIF, as-is (no zero-padding)                                |
| `location`      | no       | Array of Romanian cities                                            |
| `tags`          | no       | Lowercase keywords, no diacritics                                   |
| `workmode`      | no       | `remote` / `on-site` / `hybrid`                                     |
| `date`          | no       | ISO 8601 (`YYYY-MM-DDThh:mm:ssZ`)                                   |
| `status`        | no       | `scraped`                                                           |
| `vdate`         | no       | Verification date (ISO)                                             |
| `expirationdate`| no       | Expiration date (ISO)                                               |
| `salary`        | no       | Optional salary info                                                 |

## Location rules

- Only Romanian cities accepted; anything else falls back to `["România"]`.
- `"Romania"` (ASCII) is normalized to `"România"`.
- Cities come from `extract_location` (first token of `"City, County, Romania"`).

## Workmode rules

`_normalize_workmode` maps:

- contains `remote` → `remote`
- contains `office` / `on-site` / `site` → `on-site`
- otherwise → `hybrid` (or omitted when unknown)

## Example

```json
{
  "url": "https://electrogrup.applytojob.com/apply/jobs/details/bClwIJnZdv",
  "title": "Inginer Ofertare Energetic",
  "company": "ELECTROGRUP SA",
  "cif": "09256208",
  "location": ["Bucuresti"],
  "workmode": "on-site",
  "date": "2026-08-03T00:00:00Z",
  "status": "scraped"
}
```
