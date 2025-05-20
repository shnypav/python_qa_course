# test_app.py
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


@patch('app.generate_report')
@patch('app.calculate_statistics')
def test_index_get(mock_calculate_statistics, mock_generate_report, client):
    print(mock_calculate_statistics)
    # Test GET request
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'report' in rv.data  # Check if 'report' placeholder is in the response data


@patch('app.generate_report')
@patch('app.calculate_statistics')
def test_index_post_success(mock_calculate_statistics, mock_generate_report, client):
    # Set up the mock objects
    mock_generate_report.return_value = None
    mock_calculate_statistics.return_value = (
        10.0, 100.0, 5, 'proc1', 5.0, 'proc2', 10.0,
        ['user1', 'user2'], {'user1': 5, 'user2': 3},
        'app1', 50.0, 5.0, 2, 3
    )

    rv = client.post('/')
    assert rv.status_code == 200
    assert b'System report' in rv.data  # Checking one part of the report
    assert b'System users' in rv.data


@patch('app.generate_report')
@patch('app.calculate_statistics')
def test_index_post_failure(mock_calculate_statistics, mock_generate_report, client):
    # Set up the mock objects to raise an exception
    mock_generate_report.side_effect = Exception("Test Exception")

    rv = client.post('/')
    assert rv.status_code == 200
    assert b"An error occurred: Test Exception" in rv.data  # Check for the full error message
