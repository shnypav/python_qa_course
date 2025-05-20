#!/bin/bash

# Start the server in the background
echo "Starting the server..."
python3 server.py &

# Store the server process ID
SERVER_PID=$!

# Wait a moment for the server to start
sleep 2

# Get the port the server is listening on
PORT=$(netstat -tuln | grep -E "^tcp.*LISTEN" | grep "$SERVER_PID" | awk '{print $4}' | awk -F: '{print $NF}')

# If we couldn't get the port from netstat, try lsof
if [ -z "$PORT" ]; then
    PORT=$(lsof -p $SERVER_PID -a -i -n | grep LISTEN | awk '{print $9}' | awk -F: '{print $NF}')
fi

# If we still couldn't get the port, try ss
if [ -z "$PORT" ]; then
    PORT=$(ss -tlnp | grep "$SERVER_PID" | awk '{print $4}' | awk -F: '{print $NF}')
fi

# If we still couldn't get the port, try to get it from the server output
if [ -z "$PORT" ]; then
    # Wait a bit more for the server to print its port
    sleep 3
    # Look for the port in the server output (assuming it prints something like "Started on ('', 12345)")
    PORT=$(ps -p $SERVER_PID -o args= | grep -o "Started on.*" | grep -o "[0-9]\+")
fi

# If we still couldn't get the port, use a default
if [ -z "$PORT" ]; then
    echo "Could not determine server port, using default port detection in tests"
    # Run the tests without specifying a port
    python3 -m pytest tests/test_server_running.py -v
else
    echo "Server is running on port $PORT"
    # Run the tests with the detected port
    python3 -m pytest tests/test_server_running.py --port=$PORT -v
fi

# Clean up: kill the server process
echo "Stopping the server..."
kill $SERVER_PID