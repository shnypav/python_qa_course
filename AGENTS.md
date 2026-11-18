# Python QA Course

This repository contains independent Python QA course assignments. Keep changes scoped to the relevant homework directory; do not reorganize unrelated assignments.

## Environment

- Use Python with the dependencies in `requirements.txt`.
- Some homework directories have their own dependencies or test configuration. Check the local `requirements.txt`, `pytest.ini`, and scripts before running tests.
- Do not commit credentials, environment files, generated logs, browser profiles, or test artifacts.

## Testing

- Run the narrowest relevant `pytest` target first.
- API and Selenium tests may need network access, a browser driver, or external services. Do not treat environmental failures as product failures.
- Preserve existing fixtures and page objects. Prefer the established abstractions over one-off HTTP calls or raw Selenium selectors.

## Code Style

- Follow the surrounding code style and keep changes small.
- Add or update tests for observable behavior changes.
- Test names must state the behavior being verified.
- Do not hide failures with broad exception handling, sleeps, skips, or soft assertions.

## Git

- The working tree may contain unrelated user changes. Do not revert, format, or modify files outside the requested scope.
- Keep commit and pull-request descriptions short, factual, and free of generated-by attribution.

## Cursor Cloud specific instructions

- Install `python3-venv`, create `.venv`, then install the root `requirements.txt` and `flask`. `hw_08_ps_aux/app.py` imports Flask.
- Run tests with `.venv/bin/python -m pytest`. Geometry tests are `hw_02_figures/tests`.
- Echo server: `hw_10_echo_server/server.py --port 8080`, then `pytest tests/test_server_running.py --port=8080` from that directory.
- System report UI, from the repo root: `.venv/bin/python -m hw_08_ps_aux.app` at http://127.0.0.1:5000. Submitting the form runs `ps` and renders the report.
- Google Chrome is already installed. Selenium tests in `hw_05_06_07_selenium` open https://demo.opencart.com. Use the root `requirements.txt` for the shared environment; that homework directory has its own older pins.
- `hw_08_ps_aux/test_ps_aux_parser.py` and `hw_08_ps_aux/tests/test_ps_aux_parser.py` share a module name, so collecting both files together errors. `test_app.py::test_index_post_success` and several parser tests fail against the current assignment code.
- Leave `.venv`, logs, `*-scan.csv`, and `*-scan.txt` uncommitted.
