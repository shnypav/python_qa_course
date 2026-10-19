import csv
from collections import defaultdict
from datetime import datetime
from unittest import mock

import pytest

from hw_08_ps_aux.ps_aux_parser import write_output_to_csv, calculate_statistics as cs, \
    create_report, extract_application_name, get_total_memory_in_mb, write_report_to_file, main


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
        writer.writerow(["USER", "PID", "%CPU", "%MEM", "VSZ", "RSS", "TTY", "STAT", "START", "TIME", "COMMAND"])
        writer.writerow(["root", "1", "0.0", "0.1", "225114", "8468", "?", "Ss", "Mar29", "0:09", "/sbin/init"])
        writer.writerow(["user", "5003", "25.4", "10.2", "431564", "99080", "?", "Rl", "Apr12", "9:33",
                         "/usr/bin/python3 script.py"])
        writer.writerow(["user", "5004", "0.5", "0.1", "10000", "1024", "?", "S", "Apr12", "0:01",
                         "/usr/bin/python3 worker.py"])
        writer.writerow(
            ["fleet", "2424", "1.0", "5.0", "800000", "50000", "?", "Sl", "Apr11", "2:00", "/usr/bin/fleet"])
    return file


def test_get_total_memory_in_mb():
    with mock.patch('psutil.virtual_memory') as mock_virtual_memory:
        mock_virtual_memory.return_value.total = 8000 * 1024 * 1024  # Mock exactly 8000 MB of RAM in bytes
        total_memory_mb = get_total_memory_in_mb()
        assert total_memory_mb == 8000  # 8000 MB


def test_extract_application_name_from_command():
    command_path = "/usr/bin/fleet"
    app_name = extract_application_name(command_path)
    assert app_name == "fleet"


def test_calculate_statistics_aggregates_processes_by_user_and_application(mock_csv_file):
    mock_path = mock_csv_file.strpath.removesuffix(".csv")
    (
        total_cpu,
        total_memory,
        user_count,
        max_cpu_process_name,
        max_cpu,
        max_mem_process_name,
        max_mem,
        users,
        processes_by_user,
        max_application_name,
        max_application_mem,
        fleet_memory_usage,
        max_app_processes,
        fleet_processes,
    ) = cs(mock_path)

    assert total_cpu == pytest.approx(26.9)
    assert total_memory == pytest.approx((8468 + 99080 + 1024 + 50000) / 1024)
    assert user_count == 3
    assert users == {"root", "user", "fleet"}
    assert dict(processes_by_user) == {"root": 1, "user": 2, "fleet": 1}
    assert max_cpu_process_name == "/usr/bin/python3 script.py"
    assert max_cpu == 25.4
    assert max_mem_process_name == "/usr/bin/python3 script.py"
    assert max_mem == pytest.approx(99080 / 1024)
    assert max_application_name == "python3"
    assert max_application_mem == pytest.approx((99080 + 1024) / 1024)
    assert max_app_processes == 2
    assert fleet_memory_usage == pytest.approx(50000 / 1024)
    assert fleet_processes == 1


def test_create_report_includes_user_and_process_counts():
    total_cpu = 0.4
    total_memory = 1.3
    user_count = 2
    max_cpu_name = "/usr/bin/python3"
    max_cpu = 0.4
    max_mem_name = "/usr/bin/python3"
    max_mem = 1.2
    users = {"root", "user"}
    processes_by_user = defaultdict(int, {"root": 1, "user": 2})
    max_application_name = "python3"
    max_application_mem = 100.0
    fleet_memory_usage = 50.0
    max_app_processes = 2
    fleet_processes = 1

    report = create_report(total_cpu, total_memory, user_count, max_cpu_name, max_cpu, max_mem_name, max_mem,
                           users, processes_by_user, max_application_name, max_application_mem, fleet_memory_usage,
                           max_app_processes, fleet_processes)

    assert "System report:" in report
    assert "System users:" in report
    assert "Total unique users: 2" in report
    assert "Processes running: 3" in report
    assert "User processes:" in report
    assert "Total memory used:" in report
    assert "Total CPU used:" in report
    assert "Most memory used by process:" in report
    assert "Most CPU used by process:" in report
    assert "Application with highest memory usage:" in report
    assert "python3 -> 100.00 MB (across 2 processes)" in report
    assert "Fleet memory usage:" in report
    assert "50.00 MB (across 1 processes)" in report


def test_write_output_to_csv(mock_ps_aux_output, tmpdir):
    result_file = tmpdir.join("result")  # Omitting the extension '.csv'
    write_output_to_csv(mock_ps_aux_output, result_file.strpath)

    with open(result_file.strpath + ".csv", mode="r") as f:  # Adding '.csv' during file read
        reader = csv.reader(f)
        lines = list(reader)
        assert len(lines) == 7
        assert lines[0] == ["USER", "PID", "%CPU", "%MEM", "VSZ", "RSS", "TTY", "STAT", "START", "TIME", "COMMAND"]
        assert lines[2][-1] == "/usr/bin/python3 script.py"


def test_write_report_to_file(tmpdir):
    report = "Test Report\nSystem users: root, user\nProcesses running: 2\nFleet application memory usage: 50.0 MB\n"
    result_file = tmpdir.join("result")

    write_report_to_file(report, result_file.strpath)

    with open(f"{result_file.strpath}.txt", mode="r") as f:
        content = f.read()
        assert content == report


def test_main_writes_timestamped_csv_and_report(mock_ps_aux_output, tmpdir, monkeypatch):
    with mock.patch('hw_08_ps_aux.ps_aux_parser.get_ps_aux_output', return_value=mock_ps_aux_output):
        with mock.patch('hw_08_ps_aux.ps_aux_parser.datetime') as datetime_mock:
            mock_now = datetime(2023, 5, 1, 12, 0, 0)
            datetime_mock.now.return_value = mock_now
            monkeypatch.chdir(tmpdir)

            main()  # Call the main function without arguments

            result_file_csv = tmpdir.join("2023-05-01_12-00-system-scan.csv")
            result_file_txt = tmpdir.join("2023-05-01_12-00-system-scan.txt")

            # Check if CSV and TXT files are created
            assert result_file_csv.check()
            assert result_file_txt.check()

            # Validate CSV Content
            with open(result_file_csv.strpath, mode="r") as f:
                reader = csv.reader(f)
                lines = list(reader)
                assert len(lines) == 7

            # Validate Report Content in the TXT file
            with open(result_file_txt.strpath, mode="r") as f:
                content = f.read()
                assert "System report:" in content
                assert "Total unique users: 6" in content
                assert "Processes running: 6" in content
                assert "Total memory used: 207.64 MB" in content
                assert "Total CPU used: 26.70%" in content
                assert "Fleet memory usage:" in content
