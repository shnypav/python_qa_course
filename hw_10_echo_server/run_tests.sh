#!/bin/bash

# Start the server with a specific port
PORT=8080
echo "Starting the server on port $PORT..."
python3 server.py --port $PORT &

# Store the server process ID
SERVER_PID=$!

# Wait a moment for the server to start
sleep 2

# Run the tests with the specified port
echo "Running tests on port $PORT..."
python3 -m pytest tests/test_server_running.py --port=$PORT -v

# Clean up: kill the server process
echo "Stopping the server..."
kill $SERVER_PID