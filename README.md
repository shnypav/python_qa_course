# Python QA

### The project is to store everything related to the Python QA course

Each `hw_*` folder is a separate homework assignment with its own code and tests. Some homeworks also have their own dependencies and pytest options.

## Project structure

| Folder | Contents | Tests |
| --- | --- | --- |
| [hw_02_figures](hw_02_figures) | Geometric figure classes | `tests/` |
| [hw_03_books_users](hw_03_books_users) | Script that shares books among users | None |
| [hw_04_api_testing](hw_04_api_testing) | REST API tests | `test_rest_*.py` |
| [hw_05_06_07_selenium](hw_05_06_07_selenium) | Selenium UI tests for the OpenCart demo shop | `tests/` |
| [hw_08_ps_aux](hw_08_ps_aux) | `ps aux` system report and a Flask page that shows it | `test_*.py`, `tests/` |
| [hw_09_log_parser](hw_09_log_parser) | Access log parser | None |
| [hw_10_echo_server](hw_10_echo_server) | HTTP echo server | `tests/` |
| [hw_11_hello_worlds](hw_11_hello_worlds) | Hello World programs in 16 languages | `tests/` |
| [logs](logs) | Log files written by tests and scripts; only `.gitkeep` is committed | — |
| [.air](.air) | JetBrains Air cloud setup, test runner, review prompt and plans | — |
| [.fleet](.fleet) | JetBrains Fleet run configurations and settings | — |

## Homework folders

### hw_02_figures — geometric figures

Each figure class checks its constructor arguments and calculates `area` and `perimeter`. `add_area()` returns the sum of two figures' areas.

- `src/Figure.py` — base class. It can't be instantiated directly.
- `src/Circle.py`, `src/Annulus.py`, `src/Ellipse.py`, `src/Rectangle.py`, `src/Square.py`, `src/Rhombus.py`, `src/Trapezoid.py`, `src/Triangle.py` — the figures. `Square` extends `Rectangle`.
- `src/logging_config.py` — the shared `hw_02_figures` logger.
- `tests/conftest.py` — figure fixtures and test logging.
- `tests/test_<figure>.py` — tests for each figure.
- `tests/test_add_area.py`, `tests/test_basic.py`, `tests/test_figure_contracts.py`, `tests/test_additional_contracts.py` — tests for `add_area()`, the base class and rules shared by all figures.

Each test run writes a log to `logs/` and appends a pass/fail summary to `hw_02_figures/test_run.log`.

### hw_03_books_users — books and users

- `script.py` — reads users from `users.json` and books from `books.csv`, hands the books out to the users in turn and writes the result to `result.json`. It keeps only the name, gender, address and age of each user.
- `result.json` — output of the script.

`users.json` and `books.csv` aren't in the repository. Put them in this folder, then run `python3 hw_03_books_users/script.py`. The script logs to the console and to `logs/`. There are no automated tests.

### hw_04_api_testing — REST API tests

Tests for public REST APIs, written with `requests`. Some tests check response schemas with Cerberus.

- `test_rest_01_dogs.py`, `test_rest_08_dogs_extended.py` — Dog CEO API.
- `test_rest_02_breweries.py`, `test_rest_07_openbrewery_extended.py` — Open Brewery DB.
- `test_rest_03_jsonplaceholder.py`, `test_rest_06_jsonplaceholder_extended.py` — JSONPlaceholder.
- `test_rest_05_contracts.py` — error responses and required fields across all three APIs.
- `test_rest_04_command_line.py` — checks that the URL passed with `--url` (default `https://ya.ru`) returns the status passed with `--status_code` (default `200`).
- `conftest.py` — the command-line options, request logging to `logs/`, and a 15-second timeout for requests that don't set one.

### hw_05_06_07_selenium — Selenium UI tests

UI tests for the OpenCart demo shop (`https://demo.opencart.com` by default), built with page objects. Results are saved for Allure reports.

- `page_objects/` — `BasePage.py` holds the shared waits and actions. `MainPage.py`, `CatalogPage.py`, `ItemPage.py`, `AdminPage.py` and `RegistrationPage.py` describe the shop pages.
- `tests/` — main page, catalog, product page, admin login and user registration tests.
- `conftest.py` — the browser fixture and options: `--browser` (`chrome` or `firefox`), `--url`, `--log_level`, `--executor` (`local` or a remote Selenium/Selenoid host) and `--browser_ver` for remote runs. If a test fails, a screenshot is attached to the Allure report.
- `env.py` — the admin password for your own OpenCart instance.
- `pytest.ini` — writes Allure results to `../allure-results`.
- `requirements.txt` — pinned, older dependency versions for this homework only.
- `Dockerfile` — image that installs the requirements and runs `pytest`.

Install this folder's `requirements.txt` into a separate virtual environment, because its pinned versions would downgrade the shared one. The Air cloud setup uses Python 3.10 for it.

### hw_08_ps_aux — system process report

- `ps_aux_parser.py` — runs `ps aux` and saves the output to `<date>_<time>-system-scan.csv`. It then writes a report to a `.txt` file with the same name: users, number of processes, total CPU and memory, the process and application using the most resources, and memory used by Fleet.
- `app.py` and `templates/index.html` — Flask page with a button that generates the report and shows it as a table.
- `test_ps_aux_parser.py`, `tests/test_ps_aux_parser.py` — parser tests. The two modules have the same file name.
- `test_app.py` — tests for the Flask page. They use the Flask test client and mock the report.

Run both tools from this folder, because generated files are ignored by Git only here:

```sh
cd hw_08_ps_aux
python3 ps_aux_parser.py
PYTHONPATH=.. python3 app.py
```

The Flask page opens at http://127.0.0.1:5000.

### hw_09_log_parser — access log parser

- `log_parser.py` — parses an access log, or every `*.log` file in a folder. It prints JSON with the total number of requests, the counts by HTTP method, the top 3 IP addresses and the 3 longest requests. It also saves the JSON to a file named after the current date and time.
- [README.md](hw_09_log_parser/README.md) — options and an example.

Run `python3 hw_09_log_parser/log_parser.py --path <file or folder>`. There are no automated tests.

### hw_10_echo_server — HTTP echo server

- `server.py` — HTTP server built on sockets. It replies with the request method, the client address, the response status and the request headers. The `status` query parameter sets the response status, for example `/?status=404`. `--port` sets the port; without it, the server picks a free one.
- `run_tests.sh` — starts the server on port 8080, runs the tests and stops the server.
- `run_server_and_tests.sh`, `run_server_and_tests.py` — start the server on a free port, find which port it uses and run the tests.
- `tests/test_server_running.py` — tests for responses, HTTP methods, status codes and repeated requests.
- `tests/conftest.py` — the `--port` option. Without it, the tests look for a running `server.py`. The tests are skipped if no server responds.

### hw_11_hello_worlds — Hello World in 16 languages

Programs that ask for your name and greet you, in Python, JavaScript, Java, C, C++, C#, Go, Rust, PHP, Ruby, Bash, Perl, Lua, Tcl, AWK and x86-64 assembly (NASM).

- `hello_world.*`, `HelloWorld.java`, `HelloWorld.cs` — the programs. `hello_world.asm` targets Linux and `hello_world_macos.asm` targets macOS.
- `run.sh` — builds and runs one program and offers to install a missing toolchain.
- `tests/test_hello_world_programs.py` — runs every program and checks its prompt and greeting.
- [README.md](hw_11_hello_worlds/README.md) — build and run commands for each language.

## Files in the repository root

- `requirements.txt` — shared Python dependencies.
- `AGENTS.md` — instructions for AI coding agents working in this repository.
- `.gitignore` — Git ignore rules for caches, logs, Allure results and homework data files.
- `.air/` — JetBrains Air settings. `cloud/` holds the cloud environment setup script and test runner, `review/review-prompt.md` holds the code review prompt, and `plans/` holds implementation plans.
- `.fleet/` — JetBrains Fleet run configurations and settings.
- `.mcp.json` — MCP servers for YouTrack and TeamCity. Their tokens come from the `YOUTRACK_MCP_TOKEN` and `TC_TOKEN` environment variables.
- `.envrc` — direnv configuration that loads `.env`.
- `country_capital.py` — asks for a country and prints its capital, using the REST Countries API.
- `hello_world.py`, `newname.py`, `temptemp.py`, `aaa.md`, `temp` — scratch files that aren't part of any homework.

## Running the tests

Install the shared dependencies:

```sh
python3 -m pip install -r requirements.txt
```

The homeworks define their own pytest options (the API and Selenium suites both define `--url`), so run each suite on its own. Run the commands from the repository root:

| Homework | Command | Requires |
| --- | --- | --- |
| hw_02_figures | `python3 -m pytest hw_02_figures/tests` | — |
| hw_04_api_testing | `python3 -m pytest hw_04_api_testing` | Internet access |
| hw_05_06_07_selenium | `cd hw_05_06_07_selenium && python3 -m pytest tests` | The homework's own requirements, Chrome or Firefox, internet access |
| hw_08_ps_aux | `PYTHONPATH=.:hw_08_ps_aux python3 -m pytest --import-mode=importlib hw_08_ps_aux` | `ps` |
| hw_10_echo_server | `cd hw_10_echo_server && bash run_tests.sh` | Free port 8080 |
| hw_11_hello_worlds | `python3 -m pytest hw_11_hello_worlds/tests` | Runtimes and compilers for all 16 languages |

- Run the Selenium tests from their folder, so `pytest.ini` puts the Allure results in the repository's `allure-results/`.
- `--import-mode=importlib` lets pytest collect both `test_ps_aux_parser.py` modules. `PYTHONPATH` lets the tests import `ps_aux_parser`, `app` and `hw_08_ps_aux.ps_aux_parser`.
- `hw_03_books_users` and `hw_09_log_parser` have no tests.

In the JetBrains Air cloud environment, `bash .air/cloud/run-tests.sh all` runs every suite. Its [README](.air/cloud/README.md) also lists the network requirements and the tests that currently fail or are skipped.

## Other README files

- [hw_09_log_parser/README.md](hw_09_log_parser/README.md) — log parser options and an example.
- [hw_11_hello_worlds/README.md](hw_11_hello_worlds/README.md) — how to build and run each Hello World program, the `run.sh` launcher and the tests.
- [.air/cloud/README.md](.air/cloud/README.md) — what the Air cloud setup installs, how to run all suites, network requirements and known test failures.
