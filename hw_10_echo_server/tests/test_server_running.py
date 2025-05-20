import pytest
import requests
import socket
import subprocess
import time
import psutil


@pytest.fixture(scope="module")
def server_url(request):
    """
    Returns the URL of the running server.
    This fixture attempts to find the port of the already running server.
    The server should be started manually before running these tests.

    Can be overridden by passing --port=<port_number> to pytest.
    """
    # Check if port was provided as a command-line parameter
    port_param = request.config.getoption("--port")
    if port_param:
        found_port = int(port_param)
        print(f"Using port {found_port} from command-line parameter")
    else:
        # Find the port by looking for Python processes with 'server.py' in their command line
        found_port = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python' or proc.info['name'] == 'python3':
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'server.py' in cmdline:
                        # Now we need to find which port this process is listening on
                        connections = psutil.Process(proc.info['pid']).net_connections()
                        for conn in connections:
                            if conn.status == 'LISTEN':
                                found_port = conn.laddr.port
                                break
                        if found_port:
                            break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # If we can't find the port automatically, fall back to the default
        if not found_port:
            # Using the default port
            found_port = 8080
            print(f"Warning: Could not auto-detect server port, using default port {found_port}")
        else:
            print(f"Found server running on port {found_port}")

    # Verify the server is actually responding
    try:
        requests.get(f"http://localhost:{found_port}", timeout=1)
        print(f"Server at http://localhost:{found_port} is responding")
    except requests.RequestException:
        pytest.skip(f"No server responding at port {found_port}. Please start the server before running tests.")

    return f"http://localhost:{found_port}"


def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption("--port", action="store", default=None, help="Port number for the server")


class TestBasicConnectivity:
    """Tests for verifying basic server connectivity"""

    def test_server_responds(self, server_url):
        """Test that the server responds to a basic GET request"""
        response = requests.get(server_url)
        assert response.status_code == 200
        assert "Response Status: 200 OK" in response.text

    def test_response_contains_expected_fields(self, server_url):
        """Test that the response contains all expected fields"""
        response = requests.get(server_url)
        assert "Request Method:" in response.text
        assert "Request Source:" in response.text
        assert "Response Status:" in response.text


class TestHttpMethods:
    """Tests for different HTTP methods"""

    @pytest.mark.parametrize("method", ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
    def test_http_method_handling(self, server_url, method):
        """Test that the server properly handles different HTTP methods"""
        response = requests.request(method, server_url)
        assert response.status_code == 200
        if method != "HEAD":  # HEAD responses don't have a body
            assert f"Request Method: {method}" in response.text


class TestStatusCodes:
    """Tests for handling of different status codes"""

    @pytest.mark.parametrize("status_code,expected_status", [
        ("200", "200 OK"),
        ("201", "201 CREATED"),
        ("400", "400 BAD_REQUEST"),
        ("404", "404 NOT_FOUND"),
        ("500", "500 INTERNAL_SERVER_ERROR")
    ])
    def test_status_code_handling(self, server_url, status_code, expected_status):
        """Test that the server handles different status codes correctly"""
        response = requests.get(f"{server_url}?status={status_code}")
        assert f"Response Status: {expected_status}" in response.text

    def test_invalid_status_code(self, server_url):
        """Test that the server handles invalid status codes gracefully"""
        response = requests.get(f"{server_url}?status=999")
        # Server should default to 200 OK for invalid status codes
        assert "Response Status: 200 OK" in response.text


class TestSequentialRequests:
    """Tests for sequential request handling"""

    def test_multiple_sequential_requests(self, server_url):
        """Test that the server can handle multiple sequential requests"""
        for i in range(5):
            response = requests.get(f"{server_url}?seq={i}")
            assert response.status_code == 200
            assert "Query Parameters:" in response.text
            assert f"  seq: {i}" in response.text

    def test_different_methods_sequentially(self, server_url):
        """Test a sequence of different HTTP methods"""
        methods = ["GET", "POST", "PUT", "DELETE"]
        for method in methods:
            response = requests.request(method, server_url)
            assert response.status_code == 200
            assert f"Request Method: {method}" in response.text
