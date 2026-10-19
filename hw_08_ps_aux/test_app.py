# test_app.py
import pytest
from unittest.mock import patch
from hw_08_ps_aux.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


@patch('hw_08_ps_aux.app.generate_report')
@patch('hw_08_ps_aux.app.calculate_statistics')
def test_index_get(mock_calculate_statistics, mock_generate_report, client):
    # Test GET request
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'report' in rv.data  # Check if 'report' placeholder is in the response data
    mock_generate_report.assert_not_called()
    mock_calculate_statistics.assert_not_called()


@patch('hw_08_ps_aux.app.generate_report')
@patch('hw_08_ps_aux.app.calculate_statistics')
def test_index_post_success(mock_calculate_statistics, mock_generate_report, client, tmp_path, monkeypatch):
    # Set up the mock objects
    monkeypatch.chdir(tmp_path)
    result_file_base = '2023-05-01_12-00-system-scan'
    mock_generate_report.side_effect = lambda: (tmp_path / f'{result_file_base}.csv').touch()
    mock_calculate_statistics.return_value = (
        10.0, 100.0, 2, 'proc1', 5.0, 'proc2', 10.0,
        ['user1', 'user2'], {'user1': 5, 'user2': 3},
        'app1', 50.0, 5.0, 2, 3
    )

    rv = client.post('/')
    assert rv.status_code == 200
    assert b'System report' in rv.data  # Checking one part of the report
    assert b'System users' in rv.data
    assert b'100.00 MB' in rv.data
    mock_generate_report.assert_called_once_with()
    mock_calculate_statistics.assert_called_once_with(result_file_base)


@patch('hw_08_ps_aux.app.generate_report')
@patch('hw_08_ps_aux.app.calculate_statistics')
def test_index_post_failure(mock_calculate_statistics, mock_generate_report, client):
    # Set up the mock objects to raise an exception
    mock_generate_report.side_effect = Exception("Test Exception")

    rv = client.post('/')
    assert rv.status_code == 200
    assert b"An error occurred: Test Exception" in rv.data  # Check for the full error message
    mock_calculate_statistics.assert_not_called()
