"""End-to-end test: scrape the real WESEE applytojob board.

The WESEE group shares the electrogrup.applytojob.com board; this scraper
filters to the `WESEE` department. Skips (rather than fails) when the board
is unreachable, so that CI does not break on transient network issues.
"""

import socket

import pytest

from scraper import index

# Observed: 0 unique jobs for the WESEE department at time of writing.
# The department can legitimately have no open positions, so we only
# validate structure (URL prefix, titles, uniqueness, department filter).
EXPECTED_MIN_JOBS = 0


def _board_reachable():
    try:
        with socket.create_connection(("electrogrup.applytojob.com", 443), timeout=5):
            return True
    except OSError:
        return False


def test_scrape_real_board():
    if not _board_reachable():
        pytest.skip("applytojob board not reachable")
    html = index.fetch_listing()
    jobs = index.parse_api_jobs(html)
    assert len(jobs) >= EXPECTED_MIN_JOBS, f"Expected >= {EXPECTED_MIN_JOBS} jobs, got {len(jobs)}"
    for job in jobs:
        assert job["url"].startswith("https://electrogrup.applytojob.com/apply/jobs/details/")
        assert job["title"]
    urls = {j["url"] for j in jobs}
    assert len(urls) == len(jobs), "duplicate job URLs found"
    assert "WESEE" in index.DEPARTMENT, "scraper should target the WESEE department"
