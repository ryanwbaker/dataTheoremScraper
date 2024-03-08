"""All tests for entire application here, adapted from Falcon WSGI Tutorial (https://falcon.readthedocs.io/en/3.1.3/user/tutorial.html)."""
"""All unit tests could eventually be organized into seperate files, but given the small amount of tests with just one endpoint, all tests were left here."""

import falcon
from falcon import testing
import pytest
import dataTheoremScraper.scraper as scraper
from dataTheoremScraper.app import app
import json
from datetime import date

@pytest.fixture
def client():
    return testing.TestClient(app)


# Global test vars
url = "https://instagram.en.aptoide.com/app"
test_obj = scraper.AptoideApp(url)

# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_api(client):
    """Tests if api returns same object as expected from scraper"""
    doc = {
        'app_name': test_obj.app_name,
        'app_version': test_obj.app_version,
        'app_downloads': test_obj.downloads,
        'release_date': test_obj.release_date,
        'description': test_obj.description,
    }

    response = client.simulate_get(f'/api?url={url}')
    result_doc = json.loads(response.text)
    print(f"Response Content Type: {type(result_doc)}")

    assert result_doc == doc
    assert response.status == falcon.HTTP_OK

def test_bad_app(client):
    """Tests a bad URL ending with aptoide.com/app returns HTTP 405 status"""
    bad_url = "https://this_app_does_not_exist.en.aptoide.com/app"
    response = client.simulate_get(f'/api?url={bad_url}')
    assert response.status == falcon.HTTP_405

def test_bad_url(client):
    """Tests a bad URL that is not even from aptoide.com"""
    bad_url = "https://www.google.com"
    response = client.simulate_get(f'/api?url={bad_url}')
    assert response.status == falcon.HTTP_405

def test_missing_url(client):
    """Tests a bad request with a missing URL returns HTTPS 405 status"""
    response = client.simulate_get(f'/api')
    assert response.status == falcon.HTTP_405

def test_scraped_name():
    """Tests the scraped name of the test object"""
    assert test_obj.app_name == "Instagram"

def test_scraped_version():
    """Tests the scraped version of the test object"""
    assert type(test_obj.app_version) == str
    version_array = test_obj.app_version.split(".")
    assert len(version_array) == 5 # versioning e.g. "323.0.0.0.0"
    assert int(version_array[0]) >= 323 # ver. 323.0.0.0.0 as of Mar 8 2024

def test_scraped_downloads():
    """Tests the scraped downloads of the test object"""
    assert type(test_obj.downloads) == str
    assert len(test_obj.downloads) == 5
    assert test_obj.downloads.endswith("M+")

def test_scraped_release_date():
    """Tests the scraped release date of the test object"""
    parsed_date = test_obj.release_date.split("-")
    parsed_date = [int(el) for el in parsed_date]
    date_obj = date(parsed_date[2], parsed_date[1], parsed_date[0])
    assert len(parsed_date) == 3
    assert parsed_date[2] >= 2024
    assert date_obj >= date(2024, 3, 7) # Latest update as of Mar 8, 2024 was Mar 7, 2024

def test_scraped_description():
    """Tests the scraped description of the test object"""
    assert type(test_obj.description) == str
    assert len(test_obj.description) > 200 # Most app descriptions were very long


