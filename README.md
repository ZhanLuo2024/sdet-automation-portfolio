# 🚀 Cross-Platform Test Automation Strategy (API & UI)

A robust, enterprise-grade E2E test automation framework built with Python. Designed for scalability, maintainability, and zero-hardcoding. This repository serves as a showcase of modern Quality Engineering practices, spanning across API integration and Web automation.

## 🎯 Design Philosophy
Coming from a strong Native Mobile Development background (7+ years of iOS), this framework is designed with architectural discipline in mind:
*   **Dependency Injection over Setup/Teardown:** Utilizing Pytest's `conftest.py` and `yield` fixtures to manage test lifecycles (Setup/Teardown) efficiently without polluting test scripts.
*   **Zero Hardcoding:** Test data and environmental variables (like `BASE_URL`, `auth_token`) are decoupled and injected dynamically.
*   **Data-Driven Framework:** Leveraging `@pytest.mark.parametrize` to avoid brittle `for-loops` inside test execution, isolating test outputs perfectly.
*   **Agnostic Locators:** Utilizing Playwright's `get_by_placeholder` and CSS assertions (similar to XCUITest Accessibility ID mapping) for resilient frontend testing.

## 🛠 Tech Stack
*   **Core:** Python 3
*   **Test Runner:** Pytest (via `conftest` architecture)
*   **API Automation:** `Requests`
*   **Web Automation (UI):** Microsoft Playwright (`pytest-playwright`)

## 📁 Repository Structure

    ├── conftest.py           # Global Fixtures, Test Lifecycles, Auth Managers
    ├── tests/
    │   ├── api/
    │   │   ├── test_dummy.py     # API infrastructure verification
    │   │   └── test_products.py  # Token injection & Data-driven validations
    │   └── web/
    │       └── test_playwright_demo.py # Playwright UI tests with Smart Assertions
    ├── .gitignore
    └── README.md

## 🚀 Getting Started

### 1. Environment Setup
Clone the repository and set up a clean Python virtual environment:

    # Clone the repo
    git clone https://github.com/YourUsername/sdet-automation-portfolio.git
    cd sdet-automation-portfolio
    
    # Initialize Virtual Environment
    python3 -m venv venv
    source venv/bin/activate

### 2. Install Dependencies
Install all required libraries including the Playwright browser binaries:

    # Install core packages
    pip install pytest requests pytest-playwright
    
    # Install headless browser binaries for Playwright
    playwright install

## 🧪 Execution

### API Automation Tests
Run tests without UI, utilizing session-scoped authentication fixtures:

    pytest tests/api/ -v -s

### Web UI Automation Tests
Run the Playwright test suite in **Headed Mode** with an artificial delay (for visual demonstration purposes):

    pytest tests/web/ -v -s --headed --slowmo=500

*(Remove `--headed` to run the suite in the background as it would in a CI/CD pipeline).*

## ⏭️ Upcoming Features (Roadmap)
- [ ] **Mobile Automation:** Extend the framework using **Appium 2.0** (XCUITest & UiAutomator2).
- [ ] **Game Automation:** Integrate **Airtest / PocoSDK** for Unity-engine Object Hierarchy inspection.
- [ ] **CI/CD Integration:** Auto-trigger executions via **GitHub Actions**.
