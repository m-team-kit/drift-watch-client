"""Test example module."""

import pytest


@pytest.mark.usefixtures("with_context")
def test_running_drift(patch_requests, mock_server):
    """Test the POST request to create a drift run was sent to server."""
    assert patch_requests.post.call_count == 1
    assert mock_server.request == "POST"
    assert mock_server.url == "http://localhost:5000/drift"
    assert mock_server.json["status"] == "Running"


@pytest.mark.usefixtures("with_context")
def test_completed_drift(patch_requests, mock_server):
    """Test the PUT request to complete a drift run was sent to server."""
    assert patch_requests.put.call_count == 1
    assert mock_server.request == "PUT"
    assert mock_server.json["status"] == "Completed"


@pytest.mark.usefixtures("with_context")
def test_failed_drift(patch_requests, mock_server):
    """Test the PUT request to fail a drift run was sent to server."""
    assert patch_requests.put.call_count == 1
    assert mock_server.request == "PUT"
    assert mock_server.json["status"] == "Failed"
