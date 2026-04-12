# Week 1 API Foundation

This repository currently implements Week 1 of the roadmap: a clean API automation foundation built with `pytest`, `requests`, and environment-based configuration.

## What Is Included

- `conftest.py`: session-scoped fixtures for settings, API client, and authenticated login
- `core/api_client.py`: one shared API helper so requests are not scattered through test files
- `tests/api/`: login and cart tests written with `pytest.mark.parametrize`
- `pytest.ini`: central pytest configuration and test markers
- `requirements.txt`: pinned starter dependencies for reproducible setup

## Project Structure

```text
.
├── core/
│   └── api_client.py
├── tests/
│   └── api/
│       ├── test_auth.py
│       └── test_carts.py
├── .env.example
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in real test credentials.

## Environment Variables

```env
BASE_URL=https://dummyjson.com
TEST_USERNAME=your_api_username
TEST_PASSWORD=your_api_password
```

## Run Tests

Run the whole API suite:

```bash
pytest tests/api -v
```

Run only smoke checks:

```bash
pytest tests/api -v -m smoke
```

Run only regression checks:

```bash
pytest tests/api -v -m regression
```

## Note on Web UI Tests

SauceDemo does not expose session tokens or cookies that can be injected to bypass the login UI. The login flow is therefore automated through the Page Object rather than skipped via state injection. In a real project where the target application supports cookie or local storage pre-seeding, the preferred approach would be to inject authenticated state directly into the browser context.

## Allure

Week 1 includes the dependency for Allure so the report can be added as the next step in the workflow.

Example command:

```bash
pytest tests/api -v --alluredir=reports/allure-results
```
