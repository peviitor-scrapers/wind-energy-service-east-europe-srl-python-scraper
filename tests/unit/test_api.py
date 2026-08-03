import tests.conftest  # noqa: F401  (sys.path setup)
import unittest.mock as mock

import pytest

import scraper.api as api


def test_query_solr_returns_docs(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"success": True, "total": 2, "data": [{"url": "u1"}]}
    result = api.query_solr("9256208")
    assert result["numFound"] == 2
    assert result["docs"] == [{"url": "u1"}]


def test_query_solr_throws_on_http_error(mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.text = "boom"
    with pytest.raises(RuntimeError, match="500"):
        api.query_solr("9256208")


def test_query_solr_missing_data_returns_empty(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"success": False}
    result = api.query_solr("9256208")
    assert result["numFound"] == 0
    assert result["docs"] == []


def test_upsert_jobs_keeps_cif(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True, "count": 1}
    api.upsert_jobs([{"url": "u", "cif": "9256208"}])
    sent = mock_post.call_args.kwargs["json"]
    assert sent[0]["cif"] == "9256208"


def test_upsert_jobs_throws_on_http_error(mock_post):
    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "boom"
    with pytest.raises(RuntimeError, match="500"):
        api.upsert_jobs([{"url": "u", "cif": "9256208"}])


def test_delete_job_by_url(mock_delete):
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {"success": True}
    api.delete_job_by_url("https://example.com/job")
    assert mock_delete.call_args.kwargs["json"] == {"url": "https://example.com/job"}


def test_delete_job_by_url_404_is_silent(mock_delete):
    mock_delete.return_value.status_code = 404
    api.delete_job_by_url("https://example.com/job")


def test_delete_job_by_url_throws_on_http_error(mock_delete):
    mock_delete.return_value.status_code = 500
    mock_delete.return_value.text = "boom"
    with pytest.raises(RuntimeError, match="500"):
        api.delete_job_by_url("https://example.com/job")


def test_upsert_company_keeps_id(mock_put):
    mock_put.return_value.status_code = 200
    mock_put.return_value.json.return_value = {"success": True}
    api.upsert_company({"id": "9256208", "company": "ELECTROGRUP SA"})
    sent = mock_put.call_args.kwargs["json"]
    assert sent["id"] == "9256208"


def test_upsert_company_throws_on_http_error(mock_put):
    mock_put.return_value.status_code = 500
    mock_put.return_value.text = "boom"
    with pytest.raises(RuntimeError, match="500"):
        api.upsert_company({"id": "9256208", "company": "ELECTROGRUP SA"})


def test_check_url_head(mock_head):
    mock_head.return_value.ok = True
    mock_head.return_value.status_code = 200
    result = api.check_url("https://example.com")
    assert result["valid"] is True


def test_check_url_failure(mock_head):
    mock_head.return_value.ok = False
    mock_head.return_value.status_code = 404
    result = api.check_url("https://example.com")
    assert result["valid"] is False


def test_check_url_redirect_invalid(mock_head):
    mock_head.return_value.ok = True
    mock_head.return_value.status_code = 302
    result = api.check_url("https://example.com")
    assert result["valid"] is False
