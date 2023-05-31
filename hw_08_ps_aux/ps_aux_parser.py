import csv
from collections import defaultdict
from datetime import datetime
from subprocess import run, PIPE

current_time = datetime.now()
result_file = f"{current_time.strftime('%d-%m-%Y-%H:%M')}-scan"

users = []
process_counter = 0
total_cpu = 0
total_memory = 0
processes_by_user = defaultdict(int)
max_cpu_name = ""
max_cpu = 0
max_mem_name = ""
max_mem = 0
by_user_formatted = ""

ps_aux = run(["ps", "aux"], stderr=PIPE, stdout=PIPE)
ps_aux_output = ps_aux.stdout.decode("utf-8")

header = ps_aux_output.splitlines()[0].replace("%", "").split()

with open(f"{result_file}.csv", mode="w", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for line in ps_aux_output.splitlines()[1:]:
        line = line.replace(",", ".")
        line = line.split(None, 10)
        writer.writerow(line)

with open(f"{result_file}.csv", mode="r") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        total_cpu += float(row["CPU"])
        total_memory += float(row["MEM"])
        process_counter += 1
        users.append(row["USER"])
        processes_by_user[row["USER"]] += 1
        if float(row["CPU"]) >= max_cpu:
            max_cpu = float(row["CPU"])
            max_cpu_name = row["COMMAND"]
        if float(row["MEM"]) >= max_mem:
            max_mem = float(row["MEM"])
            max_mem_name = row["COMMAND"]

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

print(report)

with open(f"{result_file}.txt", mode="w", encoding="UTF8") as f:
    f.write(report)
    