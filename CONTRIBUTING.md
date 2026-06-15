# Contributing to Ecotracker

Thank you for your interest in contributing to the Ecotracker Home Assistant integration.

## Getting started

1. Fork the repository.
2. Create a feature branch from `main`.
3. Make your changes.
4. Run the test suite and formatter.
5. Open a pull request with a clear description.

## Development setup

Install the project dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run formatting and linting:

```bash
pre-commit run --all-files
```

Run tests:

```bash
pytest tests/unit/ -v
```

## Code style

This repository uses `ruff` and `pre-commit` for formatting and linting.

## Pull request process

- Use clear branch names.
- Keep PRs small and focused.
- Include tests for bug fixes and new features.
- Use the provided PR template.
