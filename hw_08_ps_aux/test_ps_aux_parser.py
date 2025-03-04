# test_ps_aux_parser.py
from datetime import datetime

import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from ps_aux_parser import (
    get_ps_aux_output,
    write_output_to_csv,
    calculate_statistics,
    extract_application_name,
    get_total_memory_in_mb,
)

# Mock data for 'ps aux' output
MOCK_PS_AUX_OUTPUT = """USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
user1     1234  5.0  1.0  100000  5000 ?        S    10:00   0:01 /usr/bin/python3 script.py
user2     5678 10.0  2.0  200000 10000 ?        S    10:01   0:02 /usr/bin/java -jar app.jar
"""

# Mock data for CSV content
MOCK_CSV_CONTENT = [
    {"USER": "user1", "PID": "1234", "%CPU": "5.0", "%MEM": "1.0", "VSZ": "100000", "RSS": "5000",
     "COMMAND": "/usr/bin/python3 script.py"},
    {"USER": "user2", "PID": "5678", "%CPU": "10.0", "%MEM": "2.0", "VSZ": "200000", "RSS": "10000",
     "COMMAND": "/usr/bin/java -jar app.jar"},
]


@pytest.fixture
def mock_csv_file(tmp_path):
    """Fixture to create a temporary CSV file."""
    csv_file = tmp_path / "test.csv"
    with open(csv_file, "w") as f:
        f.write("USER,PID,%CPU,%MEM,VSZ,RSS,COMMAND\n")
        for row in MOCK_CSV_CONTENT:
            f.write(",".join(row.values()) + "\n")
    return csv_file


@patch("subprocess.run")
def test_get_ps_aux_output(mock_subprocess_run):
    """Test fetching 'ps aux' output."""
    mock_subprocess_run.return_value.stdout = MOCK_PS_AUX_OUTPUT
    output = get_ps_aux_output()
    assert output == MOCK_PS_AUX_OUTPUT
    mock_subprocess_run.assert_called_once_with(["ps", "aux"], stdout=-1, text=True, check=True)


@patch("builtins.open", new_callable=mock_open)
def test_write_output_to_csv(mock_open_file):
    """Test writing 'ps aux' output to a CSV file."""
    result_file = Path("test_output")
    write_output_to_csv(MOCK_PS_AUX_OUTPUT, result_file)
    mock_open_file.assert_called_once_with("test_output.csv", "w", encoding="UTF8")
    handle = mock_open_file()
    handle.write.assert_called()


def test_calculate_statistics(mock_csv_file):
    """Test calculating statistics from a CSV file."""
    stats = calculate_statistics(mock_csv_file.with_suffix(""))

    # Unpack only the relevant values and ignore the rest
    (
        total_cpu,
        total_memory_mb,
        unique_users_count,
        max_cpu_process,
        max_cpu_usage,
        max_memory_process,
        max_memory_usage_mb,
        *_  # Ignore the remaining values
    ) = stats

    assert total_cpu == 15.0  # Total CPU
    assert total_memory_mb == pytest.approx(15.0,
                                            rel=1e-1), f"Expected ~15.0, got {total_memory_mb}"  # Total memory in MB
    assert unique_users_count == 2  # Number of unique users
    assert max_cpu_process == "/usr/bin/java -jar app.jar"  # Max CPU process
    assert max_cpu_usage == 10.0  # Max CPU usage
    assert max_memory_process == "/usr/bin/java -jar app.jar"  # Max memory process
    assert max_memory_usage_mb == pytest.approx(10.0,
                                                rel=1e-1), f"Expected ~10.0, got {max_memory_usage_mb}"  # Max memory usage in MB


def test_extract_application_name():
    """Test extracting application name from a command."""
    command = "/usr/bin/python3 script.py"
    today = datetime.utcnow().date()
    app_name = extract_application_name(command)
    assert app_name == "python3"


@patch("psutil.virtual_memory")
def test_get_total_memory_in_mb(mock_virtual_memory):
    """Test getting total memory in MB."""
    mock_virtual_memory.return_value.total = 8 * 1024 * 1024 * 1024  # 8 GB
    total_memory = get_total_memory_in_mb()
    assert total_memory == 8192.0
