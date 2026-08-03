"""Unit tests for config loading and structure."""

import json


def test_company_config_shape(company_config):
    assert company_config["id"].isdigit()
    assert company_config["company"]
    assert company_config["brand"]
    assert company_config["status"] == "activ"
    assert isinstance(company_config["location"], list)
    assert isinstance(company_config["website"], list)
    assert isinstance(company_config["career"], list)
    assert company_config["career"][0]
    assert "peviitor-scrapers" in company_config["scraperFile"]
    assert "job-seeker-ro-spider.yml" in company_config["scraperFile"]


def test_company_config_id_is_numeric(company_config):
    assert company_config["id"].isdigit()


def test_scraper_config_shape(scraper_config):
    assert scraper_config["apiBase"] == "https://electrogrup.applytojob.com"
    assert scraper_config["apiPath"] == "/apply/jobs"
    assert scraper_config["department"]


def test_configs_are_json_files():
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[2]
    for name in ("company.json", "scraper.json"):
        p = root / "scraper" / "config" / name
        assert p.exists()
        json.loads(p.read_text(encoding="utf-8"))
