import os
import re
import socket
import argparse
from http import HTTPStatus
from urllib.parse import parse_qs


def get_open_port():
    with socket.socket() as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def get_status(value):
    try:
        status = HTTPStatus(int(value))
        result = f"{status.value} {status.name}"
    except ValueError:

        result = "200 OK"
    return result


def create_response(text, method, status, remote_address, query_params=None):
    body = f"Request Method: {method}\n" \
           f"Request Source: {remote_address}\n" \
           f"Response Status: {get_status(status)}\n"

    # Add query parameters to the response if they exist
    if query_params:
        body += "Query Parameters:\n"
        for key, values in query_params.items():
            for value in values:
                body += f"  {key}: {value}\n"

    for line in text.splitlines()[1:]:
        body += line.strip()  # .split(":")[0]
        body += f"\n"

    status_line = f"HTTP/1.1 {get_status(status)}"
    headers = "\r\n".join([
        status_line
    ])
    resp = "\r\n\r\n".join([
        headers,
        body
    ])
    return resp


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Start an echo HTTP server')
    parser.add_argument('--port', type=int, default=None, help='Port to listen on (default: auto-select)')
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = args.port if args.port is not None else get_open_port()
        srv_addr = ('', port)
        print(f"Started on {srv_addr}, pid: {os.getpid()}")

        s.bind(srv_addr)
        s.listen(1)

        while True:
            print(f"Waiting for a connection on {srv_addr}")
            conn, raddr = s.accept()
            print("Connection from", raddr)
            while True:
                data = conn.recv(1024)
                if data:
                    text = data.decode("utf-8")

                    # Extract the HTTP method and path with query string
                    request_line_match = re.search(r"(.*?)\s+(.*?)\s+HTTP", text)
                    if request_line_match:
                        method = request_line_match.group(1)
                        full_path = request_line_match.group(2)

                        # Parse query parameters if they exist
                        query_params = {}
                        if '?' in full_path:
                            path, query_string = full_path.split('?', 1)
                            query_params = parse_qs(query_string)

                        # Get status from query parameters or use default
                        status = "200"
                        if 'status' in query_params and query_params['status']:
                            status = query_params['status'][0]

                        response = create_response(text, method, status, raddr, query_params)
                    else:
                        # Fallback to the previous implementation if regex fails
                        method = re.search(r"(.*)\s/", text).group(1)
                        try:
                            status = re.search(r".*?status=(\d{1,3})", text).group(1)
                            response = create_response(text, method, status, raddr)
                        except AttributeError:
                            response = create_response(text, method, status="200", remote_address=raddr)

                    conn.send(response.encode("utf-8"))
                break
            conn.close()


if __name__ == '__main__':
    main()
