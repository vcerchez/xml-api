from django.test import TestCase
import pytest
from rest_framework.test import APIClient
from xml_api_app.models import Doc


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_upload_valid_xml(api_client):
    with open("xml_api_app/tests/test_case.xml", "rb") as file:
        response = api_client.post("/api/upload/", {"file": file})
    assert response.status_code == 201  # Check for successful creation
    assert Doc.objects.count() == 1  # Check if data saved


@pytest.mark.django_db
def test_upload_no_file(api_client):
    response = api_client.post("/api/upload/", {"file": ""})
    assert response.status_code == 400  # Check for bad request
    assert b"No file provided" in response.content  # Check for error hint


@pytest.mark.django_db
def test_upload_invalid_schema_xml_file(api_client):
    with open("xml_api_app/tests/test_case_bad_schema.xml", "rb") as file:
        response = api_client.post("/api/upload/", {"file": file})
    assert response.status_code == 422  # Check for bad request
    assert (
        b"Check that the schema of the uploaded file corresponds to the schema expected by the API."
        in response.content
    )  # Check for error hint
