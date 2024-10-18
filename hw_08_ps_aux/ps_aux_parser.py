import csv
from collections import defaultdict
from subprocess import run, PIPE
import os
from datetime import datetime
import psutil


def get_ps_aux_output():
    ps_aux = run(["ps", "aux"], stderr=PIPE, stdout=PIPE)
    return ps_aux.stdout.decode("utf-8")


def write_output_to_csv(ps_aux_output, result_file):
    header = ps_aux_output.splitlines()[0].replace("%", "").split()

    with open(f"{result_file}.csv", mode="w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for line in ps_aux_output.splitlines()[1:]:
            line = line.replace(",", ".")
            line.replace("%", "")
            line = line.split(None, 10)
            writer.writerow(line)


def get_total_memory_in_mb():
    total_memory_bytes = psutil.virtual_memory().total
    total_memory_mb = total_memory_bytes / (1024 * 1024)
    return total_memory_mb


def get_application_name(command):
    """Extracts the application name from a command which might be a full path."""
    return os.path.basename(command.split()[0])


def calculate_statistics(result_file):
    total_cpu = total_memory = process_counter = 0
    max_cpu_process_name = max_mem_process_name = ""
    max_cpu = max_mem = 0
    users = []
    processes_by_user = defaultdict(int)
    processes_by_application = defaultdict(float)  # Application and their total memory usage
    fleet_memory_usage = 0.0

    total_memory_mb = get_total_memory_in_mb()

    with open(f"{result_file}.csv", mode="r") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            total_cpu += float(row["CPU"])
            mem_usage_pct = float(row["MEM"])
            mem_usage_mb = (mem_usage_pct / 100) * total_memory_mb
            total_memory += mem_usage_mb
            process_counter += 1
            users.append(row["USER"])
            processes_by_user[row["USER"]] += 1

            application_name = get_application_name(row["COMMAND"])
            if "fleet" in application_name.lower():
                fleet_memory_usage += mem_usage_mb

            processes_by_application[application_name] += mem_usage_mb

            if float(row["CPU"]) >= max_cpu:
                max_cpu = float(row["CPU"])
                max_cpu_process_name = row["COMMAND"]
            if mem_usage_mb >= max_mem:
                max_mem = mem_usage_mb
                max_mem_process_name = row["COMMAND"]

    # Find the application with the maximum memory usage
    max_application_name = max(processes_by_application, key=processes_by_application.get)
    max_application_mem = processes_by_application[max_application_name]

    return total_cpu, total_memory, process_counter, max_cpu_process_name, max_cpu, max_mem_process_name, max_mem, users, processes_by_user, max_application_name, max_application_mem, fleet_memory_usage


def create_report(total_cpu, total_memory, process_counter, max_cpu_name, max_cpu, max_mem_name, max_mem, users,
                  processes_by_user, max_application_name, max_application_mem, fleet_memory_usage):
    by_user_formatted = ""

    for user, amount in sorted(processes_by_user.items(), key=lambda kv: kv[1], reverse=True):
        by_user_formatted += f"{user}: {amount}\n"

    report = f"System report:\n" \
             f"System users: {', '.join(x for x in set(users))}\n" \
             f"Processes running: {process_counter}\n" \
             f"User processes:\n" \
             f"{by_user_formatted}" \
             f"Total memory used: {'{:.2f}'.format(total_memory)} MB\n" \
             f"Total CPU used: {'{:.2f}'.format(total_cpu)}\n" \
             f"Most memory used by process: {max_mem_name[:20]} uses {max_mem:.2f} MB\n" \
             f"Most CPU used by process: {max_cpu_name[:20]} uses {max_cpu}\n" \
             f"Application with most memory usage: {max_application_name[:20]} uses {max_application_mem:.2f} MB\n" \
             f"Fleet application memory usage: {fleet_memory_usage:.2f} MB"

    return report


def write_report_to_file(report, result_file):
    with open(f"{result_file}.txt", mode="w", encoding="UTF8") as f:
        print(report, file=f)
        f.write(result_file)


def parse_custom_report(output):
    lines = output.strip().split('\n')
    report = []
    for line in lines:
        if line.strip():  # Skip empty lines if any
            parts = line.split(':')
            if len(parts) >= 2:  # Ensure there are key and values
                report.append({'Category': parts[0].strip(), 'Detail': ':'.join(parts[1:]).strip()})
    return report


def main():
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%H:%M")
    current_time = datetime.now()
    result_file = f"{current_time.strftime('%d-%m-%Y-%H:%M')}-scan"

    ps_aux_output = get_ps_aux_output()
    write_output_to_csv(ps_aux_output, result_file)

    statistics = calculate_statistics(result_file)
    report = create_report(*statistics)
    print(report)
    write_report_to_file(report, result_file)


if __name__ == '__main__':
    main()
