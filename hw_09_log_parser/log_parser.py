import argparse
import datetime
import json
import os
import re
from collections import defaultdict

parser = argparse.ArgumentParser(description="Script to parce access.log file(s)")
parser.add_argument("-p", "--path", dest="path", action="store", help="Provide path to log file or to folder with logs")
args = parser.parse_args()


def read_file(file):
    request_count = 0
    requests_by_method = {
        "POST": 0,
        "GET": 0,
        "PUT": 0,
        "DELETE": 0,
        "HEAD": 0,
        "CONNECT": 0,
        "OPTIONS": 0,
        "TRACE": 0
    }
    requests_other = 0
    requests_by_ip = defaultdict(int)
    requests_by_time = dict()

    with open(file) as file:
        for line in file:
            request = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\S\s\S.*HTTP.*\"\s(.*)", line)
            if request:
                ip = request.group(1)
                requests_by_ip[ip] += 1
                if len(requests_by_time) < 3:
                    requests_by_time[line] = int(request.group(2))
                else:
                    min_time_key = min(requests_by_time, key=requests_by_time.get)
                    if int(request.group(2)) >= requests_by_time[min_time_key]:
                        del requests_by_time[min_time_key]
                        requests_by_time[line] = int(request.group(2))

                method = re.search(r"] \"(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE)", line)
                if method:
                    requests_by_method[method.group(1)] += 1
                else:
                    requests_other += 1
                request_count += 1

    return requests_other, request_count, requests_by_time, requests_by_method, requests_by_ip


# get info for longest requests and try to use regex more
def get_data_from_longest_request(requests_by_time):
    longest_requests = dict()
    idx = 1
    data_sorted = {k: v for k, v in sorted(requests_by_time.items(), key=lambda x: x[1])}
    for i in data_sorted:
        ip_duration = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\S\s\S.*HTTP.*\"\s(.*)", i)
        ip = ip_duration.group(1)
        duration = ip_duration.group(2)
        method = re.search(r"] \"(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE)", i).group(1)
        url = re.search(rf"] \"{method}\s(\S+)", i).group(1)
        date_time = re.search(r"\S\s\S\s\S(\S+)", i).group(1).replace(":", " ", 1)
        longest_requests[f"ID {idx}"] = {"Method": method, "URL": url, "ip": ip, "Duration": duration,
                                         "Date and Time": date_time}
        idx += 1

    return longest_requests


def main(file):
    other_requests, count, r_by_time, r_by_method, r_by_ip = read_file(file)
    longest = get_data_from_longest_request(r_by_time)
    sorted_ips = {k: v for k, v in sorted(r_by_ip.items(), key=lambda x: x[1], reverse=True)[:3]}

    all_together = {
        "Log file": file,
        "Total requests": count,
        "By methods": r_by_method,
        "Other requests": other_requests,
        "Top 3 IP": sorted_ips,
        "Longest": longest
    }

    data_json = json.dumps(all_together, indent=4)

    print(data_json)

    with open(f"{datetime.datetime.now()}.json", mode="w", encoding="UTF8") as f:
        f.write(data_json)


if os.path.isdir(args.path):
    if not args.path.endswith("/"):
        args.path += "/"
    for file in os.listdir(args.path):
        if file.endswith(".log"):
            main(f"{args.path}{file}")
else:
    main(args.path)
