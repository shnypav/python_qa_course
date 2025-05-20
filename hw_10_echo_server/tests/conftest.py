import pytest
import requests
import psutil


def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption("--port", action="store", default=None, help="Port number for the server")


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
            found_port = 60383
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
