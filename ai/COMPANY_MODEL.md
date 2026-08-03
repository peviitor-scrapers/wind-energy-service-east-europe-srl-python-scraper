# Company Model

Company document published to the peviitor company core (`/v1/firme/company/`).

## Source of truth

`scraper/config/company.json` — never edit other copies; they are generated.

## Fields

| Field        | Type   | Description                                                        |
|--------------|--------|--------------------------------------------------------------------|
| `id`         | string | CIF (8 digits)                                                     |
| `company`    | string | Legal name (UPPERCASE)                                             |
| `brand`      | string | Public brand name                                                  |
| `status`     | string | `activ` / `inactiv`                                                |
| `location`   | array  | Headquarters city                                                  |
| `website`    | array  | Company website                                                   |
| `career`     | array  | Careers/board URL                                                  |
| `scraperFile`| string | GitHub Actions workflow URL                                        |

## Upsert behavior

`upsert_company` pads `id` to 8 digits and PUTs to
`/v1/firme/company/add/`. The live address/location from ANAF (CUIScan)
takes precedence over the static config when available.

## Example

```json
{
  "id": "9256208",
  "company": "ELECTROGRUP SA",
  "brand": "ELECTROGRUP",
  "status": "activ",
  "location": ["Cluj-Napoca"],
  "website": ["https://electrogrup.ro"],
  "career": ["https://electrogrup.applytojob.com/apply/jobs/"],
  "scraperFile": "https://github.com/peviitor-scrapers/electrogrup-sa-python-scraper/actions/workflows/job-seeker-ro-spider.yml"
}
```
