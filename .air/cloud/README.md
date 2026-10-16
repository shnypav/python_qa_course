# Air cloud test environment

Air automatically runs `startup.sh` after checkout and on every resume. It prepares a Linux x86-64 Ubuntu/Debian workspace with passwordless sudo; x86-64 is required by the Linux NASM example. The script installs dependencies and starts supporting services. It does not run the test suite during startup.

See [Air's cloud startup script documentation](https://www.jetbrains.com/help/air/startup-commands.html#cloud_startup_script). Air's default timeout is 600 seconds. For the first installation of all toolchains and browsers, allow 1800 seconds in the environment's **Startup Script → Execution timeout, sec** setting. Later launches reuse installed packages, Python environments, and browser downloads.

## What is installed

| Homework | Test prerequisites |
| --- | --- |
| `hw_02_figures` | pytest; no external service |
| `hw_04_api_testing` | requests, Cerberus, pytest; access to the public APIs |
| `hw_05_06_07_selenium` | A separate Python 3.10 environment with the exact homework requirements, Chrome + matching ChromeDriver, Firefox + GeckoDriver, Xvfb, fonts and shared libraries, Allure pytest plugin |
| `hw_08_ps_aux` | Flask, psutil, pytest, `ps`; Flask uses its test client, so no web server needs to be started |
| `hw_10_echo_server` | requests, psutil, pytest; a running copy of the homework echo server, plus process/port tools used by its launchers |
| `hw_11_hello_worlds` | Python, Node.js, a JDK, C/C++ build tools, Mono C# compiler/runtime, Go, Rust, PHP CLI, Ruby, NASM and binutils |

`hw_03_books_users` and `hw_09_log_parser` have no pytest tests. Their input data is not needed by the automated suites. No database or Selenium Grid container is required for the default local browser tests. Choosing the existing remote `--executor` option still requires supplying your own Selenium/Selenoid service.

The main Python environment installs the root requirements, including Flask, which is imported by the process-report application. Selenium's older package pins are installed separately so they do not downgrade the main environment. `uv` supplies Python 3.10 if the image does not already have it. The OS Python is preserved.

## Run the tests

From the repository root:

```sh
bash .air/cloud/run-tests.sh all -q
```

Or run one suite:

```sh
bash .air/cloud/run-tests.sh hello -q
bash .air/cloud/run-tests.sh figures -q
bash .air/cloud/run-tests.sh echo -q
bash .air/cloud/run-tests.sh selenium --browser=firefox -q
```

Extra arguments are passed to pytest. Use a single suite when passing homework-specific options such as `--url` or `--browser`. The default Selenium target remains the public OpenCart demo; pass `--url` to use another compatible deployment.

The runner executes each homework in its own pytest process, including both process-parser test modules. This avoids the API/Selenium `--url` option collision and the duplicate process-parser test filenames. It continues through the suites and exits nonzero if any suite fails. It does not deselect tests to hide missing tools or failures.

To perform setup manually, use `bash .air/cloud/startup.sh`. To use the main environment in an already-open Bash terminal after setup, source `~/.local/share/air/python-qa-course/env.sh`. Open a new Fish terminal, or run `exec fish`, to load the generated Fish configuration.

## Resume behavior and configuration

Setup stores tool downloads, virtual environments, requirement hashes, and service logs outside the checkout, under `~/.local/share/air/python-qa-course` (or beneath `XDG_DATA_HOME` if set). On resume it checks installed system packages, verifies Python dependencies, reuses browser downloads, and restarts Xvfb/the echo server if they are not responding. Successful markers are written only after installation succeeds.

Air does not preserve exports from the startup process. The script therefore writes an environment file and adds an idempotent source line to Bash startup files, before any noninteractive early return or Fish handoff. It also writes a Fish `conf.d` file. Existing shell configuration is preserved. The generated environment includes the main Python on `PATH`, browser/driver paths, `DISPLAY`, and localhost proxy exclusions.

Optional Air environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `AIR_QA_STATE_DIR` | `~/.local/share/air/python-qa-course` | Absolute directory for installations, environments, and logs |
| `AIR_QA_DISPLAY` | `:99` | Local Xvfb display |
| `AIR_QA_ECHO_PORT` | `8080` | Echo server port; the test runner passes it explicitly |

The Selenium fixture accepts `CHROME_BIN`, `CHROMEDRIVER_PATH`, `FIREFOX_BIN`, and `GECKODRIVER_PATH` from setup, avoiding webdriver-manager downloads during tests. Without those settings it keeps its existing driver-manager behavior. `AIR_QA_CONTAINER_BROWSER=1` enables Chrome's container options; graphical tests run against Xvfb.

## Network access and remaining test limitations

Provisioning needs access to the configured Ubuntu/Debian package mirrors, PyPI (`pypi.org`, `files.pythonhosted.org`, or your configured pip mirror), GitHub and its API/raw/release download hosts (uv, Python 3.10, and GeckoDriver), Chrome for Testing downloads (`storage.googleapis.com`), and Mozilla's Firefox download hosts (`download.mozilla.org` and its CDN redirects). Configure these in the Air environment's network policy before launching a fresh task. The script retains TLS verification and fails with the download error if a required host is blocked. Check Air's startup logs: Air can still start the task after a startup-script failure.

The API suites require `dog.ceo`, `api.openbrewerydb.org`, `jsonplaceholder.typicode.com`, and the URL selected by the command-line API test (default `ya.ru`). Selenium requires the OpenCart URL you select. Those services can reject requests, change data, or be unavailable; installing tools cannot guarantee their tests pass. The browser tests use the existing application's accounts and registration flows; setup does not manufacture credentials or replace the public demo.

There are also existing test/code inconsistencies in `hw_08_ps_aux`, including a call to the undefined `get_application_name` and mismatched statistics expectations. The Python Hello World example prints additional lines after its greeting, which fails its runner test. The new setup does not mask these failures. Selenium already contains marked skipped/xfail admin cases; setup leaves those markers as they are. A complete test run may therefore report failures or existing skips even with every dependency installed.
