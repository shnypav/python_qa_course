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
