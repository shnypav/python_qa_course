import os
import re
import socket
from http import HTTPStatus


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


def create_response(text, method, status, remote_address):
    body = f"Request Method: {method}\n" \
           f"Request Source: {remote_address}\n" \
           f"Response Status: {get_status(status)}\n"

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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        srv_addr = ('', get_open_port())
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
                    method = re.search(r"(.*)\s/", text).group(1)
                    try:
                        status = re.search(r".*?status=(\d{1,3})", text).group(1)
                        response = create_response(text, method, status, raddr)
                    except AttributeError:
                        response = create_response(text, method, status="200", remote_address=raddr)
                        pass
                    conn.send(response.encode("utf-8"))
                break
            conn.close()


if __name__ == '__main__':
    main()
