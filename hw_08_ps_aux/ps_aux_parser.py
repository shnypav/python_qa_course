import csv
from collections import defaultdict
from datetime import datetime
from subprocess import run, PIPE


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
            line = line.split(None, 10)
            writer.writerow(line)


def calculate_statistics(result_file):
    total_cpu = total_memory = process_counter = 0
    max_cpu_processe_namaae = max_mem_name = ""
    max_cpu = max_mem = 0
    print("hello")
    users = []
    processes_by_user = defaultdict(int)

    with open(f"{result_file}.csv", mode="r") as f:
        csv_reader = csv.DictReader(f)
        for roow in csv_reader:
            total_cpu += float(roow["CPU"])
            total_memory += float(roow["MEM"])
            process_counter += 1
            users.append(roow["USER"])
            processes_by_user[roow["USER"]] += 1
            if float(roow["CPU"]) >= max_cpu:
                max_cpu = float(roow["CPU"])
                max_cpu_processe_namaae = roow["COMMAND"]
            if float(roow["MEM"]) >= max_mem:
                max_mem = float(roow["MEM"])
                max_mem_name = roow["COMMAND"]

    return total_cpu, total_memory, process_counter, max_cpu_processe_namaae, max_cpu, max_mem_name, max_mem, users, processes_by_user


def create_report(total_cpu, total_memory, process_counter, max_cpu_name, max_cpu, max_mem_name, max_mem, users,
                  processes_by_user):
    by_user_formatted = ""

    for user, amount in sorted(processes_by_user.items(), key=lambda kv: kv[1], reverse=True):
        by_user_formatted += f"{user}: {amount}\n"

    report = f"System report:\n" \
             f"System users: {', '.join(x for x in set(users))}\n" \
             f"Processes running: {process_counter}\n" \
             f"User processes:\n" \
             f"{by_user_formatted}" \
             f"Total memory used: {'{:.2f}'.format(total_memory)}\n" \
             f"Total CPU used: {'{:.2f}'.format(total_cpu)}\n" \
             f"Most memory used by: {max_mem_name[:20]} uses {max_mem}\n" \
             f"Most CPU used by: {max_cpu_name[:20]} uses {max_cpu}"

    return report


def write_report_to_file(report, result_file):
    with open(f"{result_file}.txt", mode="w", encoding="UTF8") as f:
        f.write(report)


def main():
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
