import csv
import logging

import pytest

from hw_08_ps_aux.ps_aux_parser import (
    calculate_statistics,
    parse_custom_report,
    write_output_to_csv,
)


@pytest.fixture
def write_process_rows(tmp_path):
    def write_rows(rows):
        result_file = tmp_path / "processes"
        with result_file.with_suffix(".csv").open("w", newline="", encoding="UTF8") as file:
            writer = csv.writer(file)
            writer.writerow(["USER", "%CPU", "RSS", "COMMAND"])
            writer.writerows(rows)
        return result_file

    return write_rows


def test_statistics_aggregate_applications_and_fleet_across_users(write_process_rows):
    result_file = write_process_rows([
        ["alice", "2.5", "4096", "/usr/bin/python3 first.py"],
        ["bob", "3.5", "4096", "/opt/bin/python3 second.py"],
        ["alice", "9", "6144", "/usr/bin/java -jar app.jar"],
        ["bob", "1", "1024", "/opt/Fleet --worker"],
        ["bob", "0.5", "2048", "/usr/bin/fleet-helper"],
    ])

    assert calculate_statistics(result_file) == (
        16.5, 17.0, 2,
        "/usr/bin/java -jar app.jar", 9.0,
        "/usr/bin/java -jar app.jar", 6.0,
        {"alice", "bob"}, {"alice": 2, "bob": 3},
        "python3", 8.0, 3.0, 2, 2,
    )


@pytest.mark.parametrize("cpu,rss", [
    ("invalid", "1024"),
    ("100", "invalid"),
    ("", "1024"),
    ("100", ""),
])
def test_statistics_skip_invalid_numeric_rows_and_continue(
    write_process_rows, caplog, cpu, rss
):
    result_file = write_process_rows([
        ["alice", "1", "1024", "/usr/bin/python3 first.py"],
        ["invalid-user", cpu, rss, "/opt/Fleet"],
        ["alice", "2", "2048", "/usr/bin/python3 second.py"],
    ])

    with caplog.at_level(logging.WARNING):
        stats = calculate_statistics(result_file)

    assert stats == (
        3.0, 3.0, 1,
        "/usr/bin/python3 second.py", 2.0,
        "/usr/bin/python3 second.py", 2.0,
        {"alice"}, {"alice": 2}, "python3", 3.0, 0.0, 2, 0,
    )
    assert "Error processing row" in caplog.text
    assert "invalid-user" in caplog.text


def test_statistics_return_zero_totals_for_header_only_csv(write_process_rows):
    assert calculate_statistics(write_process_rows([])) == (
        0.0, 0.0, 0, "", 0.0, "", 0.0, set(), {}, "", 0.0, 0.0, 0, 0,
    )


def test_statistics_raise_for_missing_csv(tmp_path):
    with pytest.raises(FileNotFoundError):
        calculate_statistics(tmp_path / "missing")


def test_csv_round_trip_preserves_command_arguments_and_numeric_columns(tmp_path):
    command = '/usr/bin/python3 -c "print(1, 2)"'
    output = (
        "USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND\n"
        f"alice 123 2.5 1.0 8192 2048 ? S 10:00 0:01 {command}\n"
    )
    result_file = tmp_path / "scan"

    write_output_to_csv(output, result_file)

    with result_file.with_suffix(".csv").open(newline="", encoding="UTF8") as file:
        assert list(csv.DictReader(file)) == [{
            "USER": "alice", "PID": "123", "%CPU": "2.5", "%MEM": "1.0",
            "VSZ": "8192", "RSS": "2048", "TTY": "?", "STAT": "S",
            "START": "10:00", "TIME": "0:01", "COMMAND": command,
        }]
    stats = calculate_statistics(result_file)
    assert stats[:7] == (2.5, 2.0, 1, command, 2.5, command, 2.0)


def test_custom_report_preserves_colons_and_ignores_non_field_lines():
    output = (
        "\n Heading without a separator\n"
        "  Started at : 10:30:45  \n\n"
        "System report:\n"
        " User : alice \n"
        " User : bob \n"
    )

    assert parse_custom_report(output) == [
        {"Category": "Started at", "Detail": "10:30:45"},
        {"Category": "System report", "Detail": ""},
        {"Category": "User", "Detail": "alice"},
        {"Category": "User", "Detail": "bob"},
    ]


@pytest.mark.parametrize("output", ["", " \n\t", "No report fields\nAnother heading"])
def test_custom_report_returns_no_fields_for_empty_or_unstructured_input(output):
    assert parse_custom_report(output) == []
