import csv
from collections import defaultdict
from datetime import datetime
from unittest import mock

import pytest

from hw_08_ps_aux.ps_aux_parser import write_output_to_csv, calculate_statistics as cs, \
    create_report, get_total_memory_in_mb, get_application_name, write_report_to_file, main


@pytest.fixture
def mock_ps_aux_output():
    return """USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 225114  8468 ?        Ss   Mar29   0:09 /sbin/init
user       5003  25.4 10.2 431564 99080 ?       Rl   Apr12   9:33 /usr/bin/python3 script.py
mysql      2401  0.1  0.3 874372 12900 ?       Sl   Mar28   2:11 /usr/sbin/mysqld
www-data   4242  0.0  0.1 341276  8756 ?        S    Apr12   0:22 nginx: worker process
nobody     1219  0.2  0.4 225342 33417 ?       Sl   Apr11   4:56 /bin/nobody_cmd
fleet      2424  1.0  5.0 800000 50000 ?       Sl   Apr11   2:00 /usr/bin/fleet
"""


@pytest.fixture
def mock_csv_file(tmpdir):
    file = tmpdir.join("mock_results.csv")
    with open(file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["USER", "PID", "CPU", "MEM", "VSZ", "RSS", "TTY", "STAT", "START", "TIME", "COMMAND"])
        writer.writerow(["root", "1", "0.0", "0.1", "225114", "8468", "?", "Ss", "Mar29", "0:09", "/sbin/init"])
        writer.writerow(["user", "5003", "25.4", "10.2", "431564 99080", "99080", "?", "Rl", "Apr12", "9:33",
                         "/usr/bin/python3 script.py"])
        writer.writerow(
            ["fleet", "2424", "1.0", "5.0", "800000", "50000", "?", "Sl", "Apr11", "2:00", "/usr/bin/fleet"])
    return file


def test_get_total_memory_in_mb():
    with mock.patch('psutil.virtual_memory') as mock_virtual_memory:
        mock_virtual_memory.return_value.total = 8000 * 1024 * 1024  # Mock exactly 8000 MB of RAM in bytes
        total_memory_mb = get_total_memory_in_mb()
        assert total_memory_mb == 8000  # 8000 MB


def test_get_application_name():
    command_path = "/usr/bin/fleet"
    app_name = get_application_name(command_path)
    assert app_name == "fleet"


def test_calculate_statistics(mock_csv_file):
    mock_path = mock_csv_file.strpath.replace(".csv", "")  # Remove .csv extension if present
    total_cpu, total_memory, process_counter, max_cpu_process_name, max_cpu, max_mem_process_name, max_mem, users, processes_by_user, max_application_name, max_application_mem, fleet_memory_usage = cs(
        mock_path)  # Pass the path without .csv extension

    assert process_counter == 3  # Process count based on mock data structure
    assert isinstance(total_cpu, float)  # Verify types
    assert isinstance(total_memory, float)
    assert isinstance(max_cpu, float)
    assert isinstance(max_mem, float)
    assert len(users) == 3  # Based on mock data
    assert "root" in users
    assert "user" in users
    assert "fleet" in users
    assert processes_by_user["root"] == 1
    assert processes_by_user["user"] == 1
    assert processes_by_user["fleet"] == 1
    assert fleet_memory_usage > 0


def test_create_report():
    total_cpu = 0.4
    total_memory = 1.3
    process_counter = 2
    max_cpu_name = "/usr/bin/python3"
    max_cpu = 0.4
    max_mem_name = "/usr/bin/python3"
    max_mem = 1.2
    users = ["root", "user"]
    processes_by_user = defaultdict(int, {"root": 1, "user": 1})
    max_application_name = "python3"
    max_application_mem = 100.0
    fleet_memory_usage = 50.0

    report = create_report(total_cpu, total_memory, process_counter, max_cpu_name, max_cpu, max_mem_name, max_mem,
                           users, processes_by_user, max_application_name, max_application_mem, fleet_memory_usage)

    assert "System report:" in report
    assert "System users:" in report
    assert "Processes running:" in report
    assert "User processes:" in report
    assert "Total memory used:" in report
    assert "Total CPU used:" in report
    assert "Most memory used by process:" in report
    assert "Most CPU used by process:" in report
    assert "Application with most memory usage:" in report
    assert "Fleet application memory usage:" in report


def test_write_output_to_csv(mock_ps_aux_output, tmpdir):
    result_file = tmpdir.join("result")  # Omitting the extension '.csv'
    write_output_to_csv(mock_ps_aux_output, result_file.strpath)

    with open(result_file.strpath + ".csv", mode="r") as f:  # Adding '.csv' during file read
        reader = csv.reader(f)
        lines = list(reader)
        assert len(lines) > 1  # Ensure header and at least one data row
        assert lines[0] == ["USER", "PID", "CPU", "MEM", "VSZ", "RSS", "TTY", "STAT", "START", "TIME", "COMMAND"]


def test_write_report_to_file(tmpdir):
    report = "Test Report\nSystem users: root, user\nProcesses running: 2\nFleet application memory usage: 50.0 MB\n"
    result_file = tmpdir.join("result.txt")

    write_report_to_file(report, result_file.strpath)

    with open(f"{result_file.strpath}.txt", mode="r") as f:  # Opening the correct path with '.txt'
        content = f.read()
        assert report in content


def test_main_integration(mock_ps_aux_output, tmpdir):
    with mock.patch('hw_08_ps_aux.ps_aux_parser.get_ps_aux_output', return_value=mock_ps_aux_output):
        with mock.patch('hw_08_ps_aux.ps_aux_parser.datetime') as datetime_mock:
            mock_now = datetime(2023, 5, 1, 12, 0, 0)
            datetime_mock.now.return_value = mock_now
            datetime_mock.strftime = mock_now.strftime

            # Set the current working directory to pytest's `tmpdir` fixture
            tmpdir.chdir()

            main()  # Call the main function without arguments

            result_file_csv = tmpdir.join("01-05-2023-12:00-scan.csv")
            result_file_txt = tmpdir.join("01-05-2023-12:00-scan.txt")

            # Check if CSV and TXT files are created
            assert result_file_csv.check()
            assert result_file_txt.check()

            # Validate CSV Content
            with open(result_file_csv.strpath, mode="r") as f:
                reader = csv.reader(f)
                lines = list(reader)
                assert len(lines) > 1  # At least header and one row

            # Validate Report Content in the TXT file
            with open(result_file_txt.strpath, mode="r") as f:
                content = f.read()
                assert "System report:" in content
                assert "Processes running:" in content
                assert "Fleet application memory usage:" in content
