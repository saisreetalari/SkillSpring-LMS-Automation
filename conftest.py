import os
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from config.config_reader import ConfigReader
from utilities.server_manager import ServerManager
from utilities.screenshot_helper import ScreenshotHelper
from utilities.logger import get_logger

logger = get_logger("Conftest")

def pytest_addoption(parser):
    """Register custom command-line options for pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default=ConfigReader.get_default_browser(),
        help="Target browser for tests: chrome or edge (default: chrome)"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run browser in headless mode: true or false (default: false)"
    )

@pytest.fixture(scope="session", autouse=True)
def skillspring_server():
    """Session fixture: starts mock server if testing locally; skips if targeting online practice portal."""
    base_url = ConfigReader.get_base_url()
    if "127.0.0.1" in base_url or "localhost" in base_url:
        logger.info("Initializing SkillSpring test server fixture...")
        ServerManager.start_server()
        yield
        logger.info("Test session completed. Cleaning up SkillSpring server state...")
        ServerManager.reset_state()
    else:
        logger.info(f"Targeting online LMS practice portal: {base_url}. Local server startup skipped.")
        yield

@pytest.fixture(scope="function")
def driver(request):
    """Function-level fixture initializing and closing the Selenium WebDriver instance."""
    browser_name = request.config.getoption("--browser").lower()
    headless_arg = request.config.getoption("--headless").lower() in ("true", "1", "yes")

    logger.info(f"Launching WebDriver session. Browser={browser_name}, Headless={headless_arg}")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless_arg:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_instance = webdriver.Chrome(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        if headless_arg:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_instance = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: '{browser_name}'. Choose 'chrome' or 'edge'.")

    # Favor explicit waits as required by syllabus
    driver_instance.implicitly_wait(0)

    # Attach driver to request node so pytest_runtest_makereport can access it on failure
    request.node.driver = driver_instance

    yield driver_instance

    logger.info("Tearing down WebDriver session...")
    driver_instance.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook executed after each test stage to capture screenshots upon failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when in ("call", "setup") and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            try:
                screenshot_path = ScreenshotHelper.capture_screenshot(
                    driver,
                    name_prefix=f"FAIL_{item.name}"
                )
                logger.error(f"Test failure captured screenshot at: {screenshot_path}")

                try:
                    import pytest_html
                    extras = getattr(report, "extras", None)
                    if extras is None:
                        extras = getattr(report, "extra", [])
                        extras.append(pytest_html.extras.image(screenshot_path))
                        report.extra = extras
                    else:
                        extras.append(pytest_html.extras.image(screenshot_path))
                        report.extras = extras
                except Exception:
                    pass
            except Exception as e:
                logger.warning(f"Could not take failure screenshot: {e}")

def pytest_html_report_title(report):
    report.title = "SkillSpring Learning Management Portal — Automation Test Report"

def pytest_configure(config):
    """Add metadata to pytest-html report."""
    if hasattr(config, "_metadata"):
        config._metadata["Project"] = "SkillSpring Automation (Project 3)"
        config._metadata["Framework"] = "Selenium 4 + Pytest + POM"
        config._metadata["Portal URL"] = ConfigReader.get_base_url()
        config._metadata["Author"] = "Student Automation Engineer"
