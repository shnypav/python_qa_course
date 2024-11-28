import os
from collections import defaultdict
from datetime import datetime
from subprocess import run, PIPE
from typing import Dict, List, Tuple

import psutil


def get_ps_aux_output() -> str:
    """Get the output of the 'ps aux' command."""
    ps_aux = run(["ps", "aux"], stderr=PIPE, stdout=PIPE)
    return ps_aux.stdout.decode("utf-8")


import csv


def write_output_to_csv(ps_aux_output: str, result_file: str) -> None:
    lines = ps_aux_output.splitlines()
    header, *data = [line.replace(",", ".").replace("%", "").split() for line in lines]

    with open(f"{result_file}.csv", "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def get_total_memory_in_mb() -> float:
    """Get total memory in MB."""
    total_memory_bytes = psutil.virtual_memory().total
    return total_memory_bytes / (1024 * 1024)


def get_application_name(command: str) -> str:
    """Extract the application name from a command which might be a full path."""
    return os.path.basename(command.split()[0])


def calculate_statistics(result_file: str) -> Tuple:
    """Calculate and return various statistics from the CSV file."""
    total_cpu = total_memory = process_counter = 0
    max_cpu = max_mem = 0
    max_cpu_process_name = max_mem_process_name = ""
    users = []
    processes_by_user = defaultdict(int)
    processes_by_application = defaultdict(float)
    fleet_memory_usage = 0.0

    total_memory_mb = get_total_memory_in_mb()

    with open(f"{result_file}.csv", mode="r") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            cpu_usage = float(row["CPU"])
            mem_usage_pct = float(row["MEM"])
            mem_usage_mb = (mem_usage_pct / 100) * total_memory_mb

            total_cpu += cpu_usage
            total_memory += mem_usage_mb
            process_counter += 1
            users.append(row["USER"])
            processes_by_user[row["USER"]] += 1

            application_name = get_application_name(row["COMMAND"])
            if "fleet" in application_name.lower():
                fleet_memory_usage += mem_usage_mb

            processes_by_application[application_name] += mem_usage_mb

            if cpu_usage >= max_cpu:
                max_cpu = cpu_usage
                max_cpu_process_name = row["COMMAND"]
            if mem_usage_mb >= max_mem:
                max_mem = mem_usage_mb
                max_mem_process_name = row["COMMAND"]

    max_application_name, max_application_mem = max(processes_by_application.items(), key=lambda kv: kv[1])

    return (total_cpu, total_memory, process_counter, max_cpu_process_name, max_cpu, max_mem_process_name,
            max_mem, users, processes_by_user, max_application_name, max_application_mem, fleet_memory_usage)


def create_report(total_cpu: float, total_memory: float, process_counter: int, max_cpu_name: str,
                  max_cpu: float, max_mem_name: str, max_mem: float, users: List[str],
                  processes_by_user: Dict[str, int], max_application_name: str, max_application_mem: float,
                  fleet_memory_usage: float) -> str:
    """Create a formatted system report."""
    by_user_formatted = "\n".join(
        f"{user}: {amount}" for user, amount in sorted(processes_by_user.items(), key=lambda kv: kv[1], reverse=True))

    report = (
        f"System report:\n"
        f"System users: {', '.join(set(users))}\n"
        f"Processes running: {process_counter}\n"
        f"User processes:\n{by_user_formatted}\n"
        f"Total memory used: {total_memory:.2f} MB\n"
        f"Total CPU used: {total_cpu:.2f}\n"
        f"Most memory used by process: {max_mem_name[:20]} uses {max_mem:.2f} MB\n"
        f"Most CPU used by process: {max_cpu_name[:20]} uses {max_cpu:.2f}\n"
        f"Application with most memory usage: {max_application_name[:20]} uses {max_application_mem:.2f} MB\n"
        f"Fleet application memory usage: {fleet_memory_usage:.2f} MB"
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
    """Main function to execute the script."""
    timestamp = datetime.now().strftime("%d-%m-%Y-%H:%M")
    result_file = f"{timestamp}-scan"

    ps_aux_output = get_ps_aux_output()
    write_output_to_csv(ps_aux_output, result_file)

    statistics = calculate_statistics(result_file)
    report = create_report(*statistics)
    print(report)
    write_report_to_file(report, result_file)


if __name__ == '__main__':
    main()
