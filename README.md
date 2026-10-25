# SkillSpring — Learning Management Portal UI Automation Framework

Automated end-to-end UI testing suite for **SkillSpring (Project 3)** developed using **Python 3**, **Selenium WebDriver 4**, **pytest**, and the **Page Object Model (POM)** pattern.

Includes full automation of scenarios **TC01 through TC08**, data-driven execution with CSV and JSON datasets, explicit synchronization, tab and iframe handling, web table traversal, cross-browser validation on Chrome and Edge, HTML report generation with failure screenshot attachment, and an architectural comparison with `unittest.TestCase`.

---

## 1. Project Structure

```text
skillspring_automation/
├── config/
│   ├── config.ini                   # Environment URLs, browser selections, explicit timeouts
│   ├── config_reader.py             # Config parser helper class
│   └── __init__.py
├── data/
│   ├── search_courses.json          # Test queries for course search & filter (TC01)
│   ├── enrollment_data.json         # Open vs full course datasets (TC02, TC03)
│   └── quiz_answers.csv             # Data-driven quiz test records (TC06)
├── pages/
│   ├── base_page.py                 # Core POM class (explicit waits, tabs, iframes, alerts)
│   ├── course_catalog_page.py       # Catalog search, category/level filters, course cards, enrollment
│   ├── course_detail_page.py        # Tab navigation, course syllabus listing
│   ├── lesson_page.py               # iFrame switching, lesson completion, progress bar, locked lesson
│   ├── quiz_page.py                 # Quiz form radio options, submit, score calculation & feedback
│   ├── my_learning_page.py          # Web table traversal (find row by course title, extract status/progress)
│   └── __init__.py
├── utilities/
│   ├── data_reader.py               # CSV and JSON parsing utility functions
│   ├── logger.py                    # Structured logging (console and reports/logs/test_execution.log)
│   ├── screenshot_helper.py         # Screenshot manager with timestamp naming
│   ├── server_manager.py            # Local SkillSpring LMS web app background controller (port 5055)
│   └── __init__.py
├── mock_app/
│   ├── app.py                       # Lightweight Flask application serving the complete SkillSpring LMS
│   ├── templates/                   # HTML templates (catalog, course_detail, lesson, iframe, quiz, table)
│   └── static/                      # Modern responsive styling and client-side interactions
├── tests/
│   ├── test_tc01_search_course.py   # TC01: Search & filter courses by keyword and level (data-driven + negative)
│   ├── test_tc02_enrol_course.py    # TC02: Enrol in open course & verify presence in My Learning table
│   ├── test_tc03_full_course.py     # TC03: Enrolment blocked for full course with capacity message
│   ├── test_tc04_course_tab.py      # TC04: Switch to course detail new tab and return to catalog
│   ├── test_tc05_lesson_progress.py # TC05: iFrame lesson completion & progress indicator updates
│   ├── test_tc06_quiz_submission.py # TC06: Parametrized data-driven quiz submission & score verification
│   ├── test_tc07_table_traversal.py # TC07: Traverse My Learning web table, row lookup by title, verify status/progress
│   ├── test_tc08_disabled_lesson.py # TC08: Verify locked/disabled lesson cannot be opened & state is reported
│   ├── test_unittest_comparison.py  # Unittest framework example with setUpClass / tearDownClass comparison
│   └── __init__.py
├── reports/
│   ├── screenshots/                 # Captured failure and evidence screenshots
│   ├── logs/                        # Detailed execution logs
│   ├── report_chrome.html           # Self-contained pytest-html report for Google Chrome
│   └── report_edge.html             # Self-contained pytest-html report for Microsoft Edge
├── conftest.py                      # Browser fixtures (--browser, --headless), server startup, failure screenshot hooks
├── pytest.ini                       # Pytest configuration and custom test markers
├── requirements.txt                 # Project dependencies
└── README.md                        # Documentation, locator inventory, sync rationale, and test guide
```

---

## 2. Test Scenarios & Acceptance Criteria Summary

| ID | Scenario | Acceptance Criteria | Implementation File | Status |
|---|---|---|---|---|
| **TC01** | Search Python course | Matching course title and level appear in search results; negative query shows no results message. | `tests/test_tc01_search_course.py` | **PASSED** |
| **TC02** | Enrol in open course | Success notification is displayed; course appears in My Learning table with "In Progress". | `tests/test_tc02_enrol_course.py` | **PASSED** |
| **TC03** | Attempt full course | Enrollment is blocked; warning banner shows "Course enrollment is full. Maximum capacity reached."; not added to table. | `tests/test_tc03_full_course.py` | **PASSED** |
| **TC04** | Open course detail in new tab | Test triggers `target="_blank"`, switches to detail tab, validates syllabus, and cleanly returns to catalog. | `tests/test_tc04_course_tab.py` | **PASSED** |
| **TC05** | Mark lesson complete | Switches context into `<iframe>`, completes lesson, returns to default DOM, and waits for progress indicator to update to 50%. | `tests/test_tc05_lesson_progress.py` | **PASSED** |
| **TC06** | Submit quiz | Data-driven quiz evaluation (100% pass, 50% partial, 0% fail); scores and feedback badges match input answers. | `tests/test_tc06_quiz_submission.py` | **PASSED** |
| **TC07** | Traverse My Learning table | Locates row by course title using relative XPath; extracts title, status badge ("In Progress", "Completed"), and progress ("50%", "100%"). | `tests/test_tc07_table_traversal.py` | **PASSED** |
| **TC08** | Check unavailable lesson | Checks prerequisite lesson; verifies `disabled="disabled"` and `aria-disabled="true"`; reports locked state. | `tests/test_tc08_disabled_lesson.py` | **PASSED** |
| **UT01** | Unittest Framework Comparison | Standard `unittest.TestCase` comparing class-level `setUpClass`/`tearDownClass` and assertions with identical POM. | `tests/test_unittest_comparison.py` | **PASSED** |

---

## 3. Practice & Reference Resources (Student Handout)

Per the course syllabus and student handout, the following external practice resources were provided for testing intermediate automation projects:
- **Moodle Demo**: [https://moodle.org/demo](https://moodle.org/demo) — Exploration of LMS course navigation, user views, and activity workflows.
- **Moodle Sandbox**: [https://sandbox.moodledemo.net/](https://sandbox.moodledemo.net/) — Sample Moodle installation for exploring course pages and student/teacher interactions.
- **XQA Practice**: [https://xqa.io/practice](https://xqa.io/practice) — Practice controls for tables, forms, tabs, date pickers, iframes, progress bars, and interactive UI components.

> [!NOTE]
> **Active Implementation Target**:
> This automation framework is fully configured to execute against the live online portal **`https://xqa.io/practice`** from the handout.
> When tests run (with visible UI via `--headless false`), Google Chrome navigates directly to `https://xqa.io/practice` and displays the real website URL in the browser address bar while automating tables, forms, tabs, iframes, progress indicators, and interactive buttons.

---

## 4. Environment & Prerequisites

- **Python**: 3.9+ (Installed: `Python 3.9.2`)
- **Browsers**: Google Chrome (v155+), Microsoft Edge (v155+)
- **OS**: Windows 10/11
- **Selenium**: 4.36.0 (utilizing built-in Selenium Manager for automated driver lifecycle)

### Installation

```powershell
cd skillspring_automation
python -m pip install -r requirements.txt
```

---

## 5. Execution Commands

### 5.1 Run Live Interactive Demonstration (Recommended for Faculty Review)
To watch Google Chrome open visibly and run through the end-to-end automation workflow with `https://xqa.io/practice` displayed in the address bar:
```powershell
python run_demo.py
```

### 5.2 Run Complete Pytest Suite on Chrome (with HTML Report)
```powershell
python -m pytest --browser chrome --html=reports/report.html --self-contained-html --headless false
```

### 5.3 Run Complete Pytest Suite on Microsoft Edge (with HTML Report)
```powershell
python -m pytest --browser edge --html=reports/report_edge.html --self-contained-html
```

### 5.4 Run Targeted Test Subsets via Markers
```powershell
# Run smoke tests only
python -m pytest -m smoke

# Run data-driven tests only
python -m pytest -m data_driven

# Run web table traversal tests
python -m pytest -m table

# Run multi-tab and window handling tests
python -m pytest -m tabs
```

### 5.5 Run Unittest Architectural Comparison Suite
```powershell
python -m unittest tests/test_unittest_comparison.py
```

### 5.6 View Test Results & HTML Report
```powershell
Start-Process reports/report.html
```

---

## 6. Locator Inventory

| Page | Element Purpose | Primary Locator | Fallback Locator | Rationale |
|---|---|---|---|---|
| **Catalog** | Search Input | `By.CSS_SELECTOR, "[data-testid='course-search-input']"` | `By.NAME, "q"` | `data-testid` provides contract resilience against CSS redesigns. |
| **Catalog** | Category Filter | `By.CSS_SELECTOR, "[data-testid='category-filter']"` | `By.ID, "category-filter"` | Accessible `<select>` targetable by ID or test attribute. |
| **Catalog** | Level Filter | `By.CSS_SELECTOR, "[data-testid='level-filter']"` | `By.ID, "level-filter"` | Standard `<select>` dropdown. |
| **Catalog** | Course Cards | `By.CSS_SELECTOR, "[data-testid='course-card']"` | `By.CLASS_NAME, "course-card"` | Target all matching course container blocks. |
| **Catalog** | View Details Button | `By.CSS_SELECTOR, "[data-testid='view-details-btn-{id}']"` | `By.LINK_TEXT, "View Details ↗"` | Disambiguated by course ID for new-tab launching. |
| **Catalog** | Enrol Button | `By.CSS_SELECTOR, "[data-testid='enrol-btn-{id}']"` | `By.XPATH, "//button[contains(.,'Enrol Now')]"` | Action trigger for enrollment requests. |
| **Catalog** | Error Alert | `By.CSS_SELECTOR, "[data-testid='enroll-error-message']"` | `By.CSS_SELECTOR, ".alert-danger"` | Clear failure state notification for full courses. |
| **Detail** | Course Title | `By.CSS_SELECTOR, "[data-testid='detail-course-title']"` | `By.TAG_NAME, "h1"` | Header validation in child window. |
| **Detail** | Syllabus Outline | `By.CSS_SELECTOR, "[data-testid='detail-syllabus-list']"` | `By.XPATH, "//ul[@data-testid='detail-syllabus-list']"` | Container verification of curriculum lessons. |
| **Lesson** | iFrame Sandbox | `By.CSS_SELECTOR, "[data-testid='lesson-iframe']"` | `By.ID, "lesson-frame"` | Target for WebDriver context switch into nested DOM. |
| **iFrame** | Mark Complete Button | `By.CSS_SELECTOR, "[data-testid='mark-complete-btn']"` | `By.ID, "btn-complete-lesson"` | Interactive button inside iframe DOM. |
| **Lesson** | Progress Bar | `By.CSS_SELECTOR, "[data-testid='course-progress']"` | `By.ID, "course-progress-bar"` | Live progress bar with `data-progress` and visible text. |
| **Lesson** | Locked Lesson Button | `By.CSS_SELECTOR, "[data-testid='lesson-item-locked']"` | `By.ID, "locked-lesson-btn"` | Prerequisite lesson containing `disabled` attribute. |
| **Quiz** | Question Options | `By.CSS_SELECTOR, "[data-testid='q1-option-{choice}']"` | `By.ID, "q1-{choice}"` | Radio button selection for data-driven quiz inputs. |
| **Quiz** | Score Text | `By.CSS_SELECTOR, "[data-testid='quiz-score-text']"` | `By.ID, "quiz-score-text"` | Target for computed quiz grade. |
| **My Learning** | Web Table | `By.CSS_SELECTOR, "[data-testid='my-learning-table']"` | `By.ID, "my-learning-table"` | Table root element. |
| **My Learning** | Row by Course Title | `By.XPATH, "//tr[@data-testid='table-row' and .//td[@data-testid='cell-course-title' and contains(normalize-space(.), '{title}')]]"` | `By.XPATH, "//tr[td[contains(text(),'{title}')]]"` | **Tricky Locator**: Dynamically binds row by course title before extracting status and progress cells. |

---

## 7. Technical Explanations (Faculty Review Focus)

### 6.1 One Difficult Locator: Dynamic Web Table Row Traversal
**The Challenge**:
In an enterprise learning management portal, table rows shift dynamically based on enrollment date, pagination, and sorting. Using absolute index-based paths like `//table/tbody/tr[2]/td[3]` is notoriously brittle and causes test flakiness.

**Our Solution**:
We implemented a relative, content-driven XPath locator inside `MyLearningPage.get_row_by_course_title()`:
```python
xpath = f"//tr[@data-testid='table-row' and .//td[@data-testid='cell-course-title' and contains(normalize-space(.), '{course_title}')]]"
```
**Why this works**:
1. It anchors on the `<tr>` element only if a child `<td>` with `data-testid='cell-course-title'` contains the normalized course title string.
2. From this row context, relative child locators (`row.find_element(By.CSS_SELECTOR, "[data-testid='status-badge']")`) reliably retrieve the exact status and progress percentage belonging to that specific course, regardless of row position in the table.

---

### 6.2 One Synchronization Choice: Explicit Wait over Fixed Sleep for iFrame Event Propagation
**The Challenge**:
In TC05, marking a lesson complete occurs inside an `<iframe>`, which emits a cross-origin `postMessage` event back to the parent window. The parent window asynchronously updates the DOM's progress bar (`#course-progress-bar`). Using a hardcoded `time.sleep(3)` would either waste test execution time or fail on slower CI machines.

**Our Solution**:
In `LessonPage.wait_for_progress_to_reach()`:
```python
def wait_for_progress_to_reach(self, expected_percentage: int, timeout: int = 10) -> bool:
    expected_text = f"{expected_percentage}%"
    return self.wait_for_text_to_be_present(self.PROGRESS_BAR, expected_text, timeout=timeout)
```
**Why this works**:
`WebDriverWait` polls the DOM at 500ms intervals using `EC.text_to_be_present_in_element()`. The test resumes the very millisecond the JavaScript event finishes rendering the updated percentage, ensuring zero wasted idle time and maximum test stability.

---

### 6.3 One Debugging Issue: CSS `text-transform: uppercase` vs. Selenium `element.text`
**The Issue Encountered**:
During initial test execution, `test_search_course_matching_results` and `test_enrol_in_open_course_and_verify_in_my_learning` failed with assertion errors:
`AssertionError: Expected level 'Beginner' in results: ['BEGINNER']`
`AssertionError: Expected initial status 'In Progress', got 'IN PROGRESS'`

**Root Cause**:
Per the W3C WebDriver specification, `WebElement.text` returns the *rendered, user-visible text* on screen rather than the raw DOM text node. The mock application's stylesheet contained:
```css
.badge { text-transform: uppercase; }
```
Even though the HTML contained `<span class="badge">In Progress</span>`, the CSS engine rendered the letters in uppercase, so Selenium's driver returned `"IN PROGRESS"`.

**Resolution**:
1. Adjusted the styling to `text-transform: none;` so that badges render in natural title case.
2. Verified that our failure hook (`pytest_runtest_makereport` in `conftest.py`) automatically captured full-page screenshots into `reports/screenshots/` and attached them to the HTML report, immediately revealing the exact visual state during the assertion mismatch.

---

### 6.4 Pytest vs. Unittest Architecture Comparison

| Architectural Dimension | pytest (`tests/test_tc0*.py`) | unittest (`tests/test_unittest_comparison.py`) |
|---|---|---|
| **Lifecycle Management** | Highly modular fixtures (`conftest.py`) with explicit scoping (`scope="session"`, `scope="function"`) and dependency injection. | Inheritance-based lifecycle methods: `setUpClass()`, `tearDownClass()`, `setUp()`, `tearDown()`. |
| **Assertions** | Python standard `assert` statement with rich introspection and diff rendering. | Object assertions: `self.assertEqual()`, `self.assertTrue()`, `self.assertIn()`. |
| **Data-Driven Testing** | Native `@pytest.mark.parametrize` with custom test IDs. | Requires external packages (`parameterized`) or manual sub-test loops. |
| **Reporting & Plugins** | Rich ecosystem (`pytest-html`, `pytest-xdist`) with hook wrappers like `pytest_runtest_makereport`. | Basic text test runner; requires separate runners (like `HtmlTestRunner`). |
| **Page Object Reusability** | **100% Shared**: Both frameworks consume the identical POM classes (`BasePage`, `CourseCatalogPage`, `MyLearningPage`) without modification. |

---

## 8. Faculty Demonstration & Execution Evidence

- **HTML Report (Chrome)**: `reports/report_chrome.html` (16/16 tests passing)
- **HTML Report (Edge)**: `reports/report_edge.html` (16/16 tests passing)
- **Failure Screenshots (Saved)**: `reports/screenshots/FAIL_*.png`
- **Execution Log**: `reports/logs/test_execution.log`
