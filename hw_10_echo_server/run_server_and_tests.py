#!/usr/bin/env python3
import subprocess
import time
import psutil
import os
import sys
import signal


def find_server_port(pid):
    """Find the port that the server with the given PID is listening on."""
    try:
        process = psutil.Process(pid)
        connections = process.connections()
        for conn in connections:
            if conn.status == 'LISTEN':
                return conn.laddr.port
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return None


# Start the server
print("Starting the server...")
server_process = subprocess.Popen(
    [sys.executable, "server.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for the server to start
time.sleep(2)

# Try to get the port from the server output
server_port = None
for line in server_process.stdout.readline().splitlines():
    if "Started on" in line:
        # Extract port from line like "Started on ('', 12345), pid: 1234"
        try:
            port_part = line.split("(")[1].split(")")[0]
            server_port = int(port_part.split(",")[1].strip())
            break
        except (IndexError, ValueError):
            pass

# If we couldn't get the port from output, try to find it using psutil
if not server_port:
    server_port = find_server_port(server_process.pid)

# Run the tests
try:
    if server_port:
        print(f"Server is running on port {server_port}")
        test_command = [sys.executable, "-m", "pytest", "tests/test_server_running.py", f"--port={server_port}", "-v"]
    else:
        print("Could not determine server port, using default port detection in tests")
        test_command = [sys.executable, "-m", "pytest", "tests/test_server_running.py", "-v"]

    test_process = subprocess.run(test_command, check=True)
    print("Tests completed successfully")

finally:
    # Clean up: kill the server process
    print("Stopping the server...")
    os.kill(server_process.pid, signal.SIGTERM)
    server_process.wait()
