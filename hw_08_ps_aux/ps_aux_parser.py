# ps_aux_parser_revised.py
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess
from typing import Dict, List, Tuple

import psutil

CSV_EXTENSION = ".csv"
ENCODING = "utf-8"
TEXT_EXTENSION = ".txt"


def get_ps_aux_output() -> str:
    """Fetch the output of the 'ps aux' command."""
    result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, text=True, check=True)
    return result.stdout


def write_output_to_csv(ps_aux_output: str, result_file: Path) -> None:
    """Write the 'ps aux' command output to a CSV file."""
    lines = ps_aux_output.splitlines()
    # Standard ps aux headers: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
    header = ['USER', 'PID', '%CPU', '%MEM', 'VSZ', 'RSS', 'TTY', 'STAT', 'START', 'TIME', 'COMMAND']
    data = [line.split() for line in lines[1:]]

    with open(f"{result_file}.csv", "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def get_total_memory_in_mb() -> float:
    """Get the total memory in MB."""
    return psutil.virtual_memory().total / (1024 * 1024)


def extract_application_name(command: str) -> str:
    """Extract the application name from a command line."""
    return Path(command.split()[0]).name


def calculate_statistics(result_file: Path) -> Tuple:
    """Calculate and return various statistics from the CSV file."""
    total_cpu = total_memory = 0.0
    max_cpu, max_mem = 0.0, 0.0
    max_cpu_process, max_mem_process = "", ""
    users = set()  # Using set to avoid duplicate user entries
    processes_by_user = defaultdict(int)
    processes_by_application = defaultdict(lambda: {"memory": 0.0, "processes": 0})
    fleet_usage = 0.0
    fleet_process_count = 0  # Track the number of Fleet processes

    csv_file = f"{result_file}.csv"
    with open(csv_file, "r", encoding=ENCODING) as f:
        csv_reader = csv.DictReader(f)
        # Store all rows in memory to avoid file closure issues
        rows = list(csv_reader)
        for row in rows:
            try:
                cpu_usage = float(row["%CPU"])
                mem_usage_mb = float(row["RSS"]) / 1024  # RSS is in KB, convert to MB

                total_cpu += cpu_usage
                total_memory += mem_usage_mb
                processes_by_user[row["USER"]] += 1
                users.add(row["USER"])

                application_name = extract_application_name(row["COMMAND"])
                if "fleet" in application_name.lower():
                    fleet_usage += mem_usage_mb
                    fleet_process_count += 1  # Increment Fleet process count

                processes_by_application[application_name]["memory"] += mem_usage_mb
                processes_by_application[application_name]["processes"] += 1

                if cpu_usage > max_cpu:
                    max_cpu = cpu_usage
                    max_cpu_process = row["COMMAND"]

                if mem_usage_mb > max_mem:
                    max_mem = mem_usage_mb
                    max_mem_process = row["COMMAND"]
            except (KeyError, ValueError) as e:
                print(f"Error processing row: {row}. Error: {e}")
                continue

    # Find application with highest memory usage
    max_app_name, max_app_stats = max(
        processes_by_application.items(),
        key=lambda item: item[1]["memory"],
        default=("", {"memory": 0.0, "processes": 0}),
    )

    return (
        total_cpu,
        total_memory,
        len(users),
        max_cpu_process,
        max_cpu,
        max_mem_process,
        max_mem,
        users,
        processes_by_user,
        max_app_name,
        max_app_stats["memory"],
        fleet_usage,
        max_app_stats["processes"],
        fleet_process_count,  # Use the correct Fleet process count
    )


def create_report(
    total_cpu: float,
    total_memory: float,
    user_count: int,
    max_cpu_name: str,
    max_cpu: float,
    max_mem_name: str,
    max_mem: float,
    users: set,
    processes_by_user: Dict[str, int],
    max_app_name: str,
    max_app_mem: float,
    fleet_usage: float,
    max_app_processes: int,
    fleet_processes: int,
) -> str:
    """Create a formatted system report."""
    processes_summary = "\n".join(
        f"{user}: {count}"
        for user, count in sorted(processes_by_user.items(), key=lambda item: item[1], reverse=True)
    )

    report = (
        f"System report:\n"
        f"Total unique users: {user_count}\n"
        f"System users: {', '.join(users)}\n"
        f"\nProcesses running: {sum(processes_by_user.values())}\n"
        f"User processes:\n{processes_summary}\n"
        f"\nTotal memory used: {total_memory:.2f} MB\n"
        f"Total CPU used: {total_cpu:.2f}%\n"
        f"\nMost memory used by process:\n  {max_mem_name[:50]} -> {max_mem:.2f} MB\n"
        f"Most CPU used by process:\n  {max_cpu_name[:50]} -> {max_cpu:.2f}%\n"
        f"  (This is the single process using the most memory.)\n"
        f"\nApplication with highest memory usage:\n  {max_app_name[:20]} -> {max_app_mem:.2f} MB "
        f"(across {max_app_processes} processes)\n"
        f"Fleet memory usage:\n  {fleet_usage:.2f} MB "
        f"(across {fleet_processes} processes)\n"
    )
    return report


def write_report_to_file(report: str, result_file: str) -> None:
    """Write the report to a text file."""
    with open(f"{result_file}.txt", mode="w", encoding="UTF8") as f:
        f.write(report)


def parse_custom_report(output: str) -> List[Dict[str, str]]:
    """Parse the custom report output."""
    return [{'Category': parts[0].strip(), 'Detail': ':'.join(parts[1:]).strip()} for line in output.strip().split('\n')
            if (parts := line.split(':', 1)) and len(parts) >= 2]


def main() -> None:
    """Main function for the script."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    result_file = Path(f"{timestamp}-system-scan")

    ps_aux_output = get_ps_aux_output()
    write_output_to_csv(ps_aux_output, result_file)

    stats = calculate_statistics(result_file)
    report = create_report(*stats)
    print(report)
    write_report_to_file(report, str(result_file))


if __name__ == "__main__":
    main()
