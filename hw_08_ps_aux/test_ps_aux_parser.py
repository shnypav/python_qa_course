import unittest.mock
from ps_aux_parser import write_output_to_csv, calculate_statistics, \
    create_report, write_report_to_file

ps_aux_output_data = """
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 225448  9460 ?        Ss   Jan03   3:42 /sbin/init
root         2  0.0  0.0      0     0 ?        S    Jan03   0:01 [kthreadd]
"""

calculated_statistics = (0.0, 0.1, 2, "/sbin/init", 0.0, "/sbin/init", 0.1, ["root", "root"], {"root": 2})

report = """
System report:
System users: root
Processes running: 2
User processes:
root: 2
Total memory used: 0.10
Total CPU used: 0.00
Most memory used by: /sbin/init uses 0.1
Most CPU used by: /sbin/init uses 0.0
"""


def test_write_output_to_csv():
    with unittest.mock.patch("builtins.open", new=unittest.mock.mock_open()) as mock_file:
        write_output_to_csv(ps_aux_output_data, "result")
        mock_file.assert_called_once_with("result.csv", mode="w", encoding="UTF8")


def test_calculate_statistics():
    with unittest.mock.patch("builtins.open", new=unittest.mock.mock_open(read_data=ps_aux_output_data)) as mock_file:
        result = calculate_statistics("result")
        mock_file.assert_called_once_with("result.csv", mode="r")
        assert result == calculated_statistics


def test_create_report():
    assert create_report(*calculated_statistics) == report


def test_write_report_to_file():
    with unittest.mock.patch("builtins.open", new=unittest.mock.mock_open()) as mock_file:
        write_report_to_file(report, "result")
        mock_file.assert_called_once_with("result.txt", mode="w", encoding="UTF8")
