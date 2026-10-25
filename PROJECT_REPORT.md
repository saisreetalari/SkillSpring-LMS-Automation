# Project 3: SkillSpring — Learning Management Portal UI Automation
## Comprehensive Project Submission Report

**Student Name:** Talari Sai Sree  
**Class / Branch:** 3rd BCA Data Science  
**Subject:** Advanced UI Test Automation (Python & Selenium WebDriver)  
**Date of Submission:** October 24, 2026  
**Technology Stack:** Python 3.9, Selenium WebDriver 4, pytest, Page Object Model (POM), pytest-html  
**Target Portals:** `https://xqa.io/practice` (with SkillSpring LMS Integration) & Standalone LMS Mock (`mock_app/`)  

---

## 1. Executive Summary

For Project 3 (SkillSpring), I developed an end-to-end automated UI testing framework using **Python 3**, **Selenium WebDriver 4**, and **pytest**, structured around the **Page Object Model (POM)** pattern.

The purpose of this framework is to automate and validate the critical learning workflows of an enterprise learning management portal, including:
- Course catalog searching and real-time filtering
- Student enrollment form handling and constraint validation
- Switching contexts across browser tabs (`target="_blank"`)
- Context switching into and out of nested `<iframe>` sandbox elements
- Dynamic evaluation tracking using progress bar updates
- Web table traversal and relative XPath row data extraction
- Verification of locked/disabled curriculum states and interactive actions

The framework is verified cross-browser on Google Chrome and Microsoft Edge, executes 100% reliably with zero hardcoded sleeps (utilizing explicit synchronization via `WebDriverWait`), and generates a self-contained HTML test execution report with failure screenshot capture.

---

## 2. Test Scenarios & Acceptance Criteria

I designed and automated test cases covering all requirements from the project specification:

| Test ID | Scenario Description | Acceptance Criteria | Execution Status |
|:--- |:--- |:--- |:--- |
| **TC01** | Course Search & Filter | Matching course and level appear dynamically; negative query shows clear empty state. | **PASSED (4/4)** |
| **TC02** | Student Enrollment | Student registration form accepts valid details; enrollment status confirms success. | **PASSED** |
| **TC03** | Full Course Capacity | Enrollment is blocked with clear validation message when capacity or prerequisites fail. | **PASSED** |
| **TC04** | Course Detail New Tab | Test triggers `target="_blank"`, switches to child tab, validates syllabus, and returns. | **PASSED** |
| **TC05** | Lesson Progress in iFrame | Switches into `<iframe>`, completes lesson action, returns to default content, and verifies progress. | **PASSED** |
| **TC06** | Quiz & Progress Tracker | Dynamic progress indicator advances upon task initiation; percentage updates dynamically. | **PASSED** |
| **TC07** | Web Table Traversal | Locates specific row by course title using dynamic relative XPath; extracts title, status, and progress. | **PASSED** |
| **TC08** | Disabled Lesson Check | Verifies unavailable/prerequisite lesson cannot be clicked and reports correct disabled state. | **PASSED** |
| **TC09** | Learning Path Navigation | Navigates multi-tab curriculum paths and confirms restricted/disabled tab constraints. | **PASSED** |
| **TC10** | Certificate Action Verify | Performs action verification clicks and verifies dynamic confirmation feedback. | **PASSED** |
| **UT01** | Unittest Comparison Suite | Validates identical POM workflow within `unittest.TestCase` using `setUpClass` / `tearDownClass`. | **PASSED** |

---

## 3. Architecture & Project Layout

I organized the codebase following clean separation of concerns:

```text
skillspring_automation/
├── config/
│   ├── config.ini                   # Base URLs, default browser, timeouts, window dimensions
│   ├── config_reader.py             # ConfigParser wrapper for strongly-typed settings
│   └── __init__.py
├── data/
│   ├── search_courses.json          # Data-driven search keywords and expected results (TC01)
│   ├── enrollment_data.json         # Open vs full course enrollment test records (TC02, TC03)
│   └── quiz_answers.csv             # Data-driven quiz test records (TC06)
├── pages/
│   ├── base_page.py                 # Core POM helper (explicit waits, clicks, tabs, frames, alerts)
│   ├── course_catalog_page.py       # Catalog search, category/level filters, course cards
│   ├── student_enrollment_page.py   # Student registration form input and validation
│   ├── course_detail_page.py        # New-tab handling and syllabus verification
│   ├── lesson_page.py               # iFrame switching, progress tracking, locked lessons
│   ├── quiz_page.py                 # Progress tracking and evaluation polling
│   ├── my_learning_page.py          # Relative XPath row lookup and cell data extraction
│   ├── learning_path_page.py        # Tab switching and disabled tab assertion
│   ├── certificate_page.py          # Dynamic action click and verification message retrieval
│   └── __init__.py
├── utilities/
│   ├── data_reader.py               # JSON and CSV dataset parsing utilities
│   ├── logger.py                    # Structured dual logging (console + execution log file)
│   ├── screenshot_helper.py         # Timestamped failure screenshot capture utility
│   ├── server_manager.py            # Local mock app process controller
│   └── __init__.py
├── tests/
│   ├── test_tc01_search_course.py   # Parametrized course search tests
│   ├── test_tc02_enrol_course.py    # Form enrollment acceptance tests
│   ├── test_tc03_full_course.py     # Blocked enrollment constraint tests
│   ├── test_tc04_course_tab.py      # Multi-tab context switching tests
│   ├── test_tc05_lesson_progress.py # Nested iframe context switching tests
│   ├── test_tc06_quiz_submission.py # Dynamic progress bar tracking tests
│   ├── test_tc07_table_traversal.py # Multi-column web table extraction tests
│   ├── test_tc08_disabled_lesson.py # Locked/disabled element assertion tests
│   ├── test_tc09_learning_path.py   # Tab component navigation tests
│   ├── test_tc10_certificate_generation.py # Action verification tests
│   ├── test_unittest_comparison.py  # Unittest.TestCase architectural comparison
│   └── __init__.py
├── reports/
│   ├── report.html                  # Self-contained pytest HTML execution report
│   ├── screenshots/                 # Captured run evidence and failure screenshots
│   └── logs/test_execution.log      # Complete runtime execution log
├── conftest.py                      # Browser fixtures (--browser, --headless), failure screenshot hooks
├── pytest.ini                       # Test discovery and custom marker definitions
├── run_demo.py                      # Standalone visual demonstration runner script
├── SkillSpring_Project_Report.docx  # Formal Word project submission report
└── README.md                        # Framework setup, locator inventory, and execution guide
```

---

## 4. Dual Environment Testing Strategy

To ensure comprehensive test coverage, I automated and validated the test suite across two environments:

1. **Live Online Practice Portal (`https://xqa.io/practice`)**:
   I automated the live online exercises from the course handout to validate real-world elements on an external server:
   - Web Tables (`/web-tables`): For course/record search, sorting, and row extraction.
   - Practice Form (`/practice-form`): For student registration, email validation, and required fields.
   - Browser Windows (`/browser-windows`): For `target="_blank"` tab switching.
   - Frames (`/frames`): For nested `<iframe>` sandbox manipulation.
   - Progress Bar (`/progress-bar`): For dynamic evaluation tracking.
   - Buttons (`/buttons`): For action verification.
   When running visible tests, Google Chrome directly navigates to `https://xqa.io/practice`.

2. **Dedicated SkillSpring Learning Management Portal (`mock_app/`)**:
   To test the complete end-to-end LMS student journey, I also built a dedicated SkillSpring web application. This allowed me to test specialized business workflows that public practice websites don't have:
   - Course catalog browsing with search and category filters (`Python for Beginners`, `Advanced Python & Selenium`).
   - Enforcing capacity constraints (blocking enrollment when a course is full).
   - Exploring course syllabi in child tabs.
   - Completing lessons inside sandboxed iframes with dynamic progress bar updates.
   - Data-driven quiz evaluation and score calculations.

---

## 5. Test Execution Evidence & Screenshots

The project report includes full visual run evidence across both environments:

### 5.1 Live Online Portal Evidence (`xqa.io/practice`)
- `reports/screenshots/EVIDENCE_TC01_Web_Tables_Search.png`: Course catalog web table search on xqa.io.
- `reports/screenshots/EVIDENCE_TC02_Student_Enrollment_Form.png`: Student registration form filled for Sai Sree.
- `reports/screenshots/EVIDENCE_TC06_Progress_Bar_Tracker.png`: Dynamic progress bar advancement tracking.
- `reports/screenshots/EVIDENCE_TC10_Button_Action_Verification.png`: Action verification confirmation.

### 5.2 SkillSpring LMS Portal Evidence (`mock_app/`)
- `reports/screenshots/EVIDENCE_MOCK_01_Catalog_Courses.png`: SkillSpring Course Catalog showing "Python for Beginners" and "Advanced Python & Selenium".
- `reports/screenshots/EVIDENCE_MOCK_02_Course_Detail_Syllabus.png`: Course Detail page showing syllabus lessons and curriculum tabs.
- `reports/screenshots/EVIDENCE_MOCK_03_Lesson_Progress.png`: Interactive lesson page with iframe sandbox and completion progress bar.
- `reports/screenshots/EVIDENCE_MOCK_04_My_Learning_Table.png`: My Learning web table showing enrolled courses, status badges, and progress percentages.

---

## 5. Locator Strategy & Inventory

| Page | Element Purpose | Primary Locator | Fallback Locator | Rationale |
|:--- |:--- |:--- |:--- |:--- |
| **Catalog** | Search Input | `By.ID, "searchBox"` | `By.CSS_SELECTOR, "#searchBox"` | Standard text input for real-time table filtering. |
| **Catalog** | Web Table Rows | `By.CSS_SELECTOR, "div[role='row']"` | `By.CLASS_NAME, "rt-tr-group"` | Targets all rendered record rows within the table. |
| **Enrollment** | First Name Input | `By.ID, "firstName"` | `By.CSS_SELECTOR, "#firstName"` | Direct unique ID locator for student first name. |
| **Enrollment** | Email Input | `By.ID, "userEmail"` | `By.CSS_SELECTOR, "#userEmail"` | Direct ID locator for student email. |
| **Enrollment** | Submit Button | `By.ID, "submit"` | `By.CSS_SELECTOR, "#submit"` | Action trigger button for form submission. |
| **Course Detail** | New Tab Button | `By.ID, "tabButton"` | `By.CSS_SELECTOR, "#tabButton"` | Button triggering window.open / child tab. |
| **Lesson iFrame** | Lesson Frame | `By.ID, "frame1"` | `By.CSS_SELECTOR, "#frame1"` | Target frame element for WebDriver context switch. |
| **Lesson Progress**| Disabled Element | `By.ID, "enableAfter"` | `By.CSS_SELECTOR, "#enableAfter"` | Verified for disabled attribute state. |
| **Quiz Tracker** | Start Button | `By.ID, "startStopButton"` | `By.CSS_SELECTOR, "#startStopButton"` | Interactive button initiating progress. |
| **Quiz Tracker** | Progress Indicator | `By.CSS_SELECTOR, "div[role='progressbar']"` | `By.CLASS_NAME, "progress-bar"` | React progress element updating width percentage. |
| **Action Verify** | Dynamic Click Button | `By.ID, "dynamicClickBtn"` | `By.XPATH, "//button[text()='Click Me']"` | Interactive button triggering dynamic event. |

---

## 6. Technical Implementation Highlights

### 6.1 Tricky Locator: Dynamic Relative XPath for Web Table Rows
- **The Problem:** In dynamic web tables, rows change position dynamically when searching, sorting, or filtering. Using an absolute index like `//div[@role='rowgroup']/div[2]` causes tests to fail when data order changes.
- **My Solution:** I implemented a content-driven relative XPath locator:
  ```python
  xpath = f"//div[@role='row' and .//div[contains(normalize-space(.), '{course_title}')]]"
  ```
- **Why this works:** It anchors on the row container only if a child cell contains the target text, regardless of row position. From that row reference, relative child queries extract the exact status and progress cells for that course.

### 6.2 Synchronization Strategy: Explicit Waits over Hardcoded Sleeps
- **The Problem:** Dynamic operations (like progress bars and iframe event updates) take varying amounts of time depending on machine speed and network latency. Using `time.sleep(5)` wastes time on fast machines and causes random failures on slow machines.
- **My Solution:** I used `WebDriverWait` with custom condition polling:
  ```python
  WebDriverWait(self.driver, 10).until(lambda d: self.get_progress_value() >= min_percentage)
  ```
- **Why this works:** The test proceeds the exact millisecond the condition is satisfied, guaranteeing 100% test reliability with minimum execution duration.

---

## 7. Testing Framework Comparison: Pytest vs Unittest

| Dimension | Pytest Framework | Unittest Framework |
|:--- |:--- |:--- |
| **Class Architecture** | Standard classes or standalone functions without inheritance. | Requires subclassing `unittest.TestCase`. |
| **Fixtures & Setup** | Modular `@pytest.fixture` with dependency injection. | Class-level `setUpClass`, `tearDownClass`, `setUp`, `tearDown`. |
| **Assertions** | Plain Python `assert` with detailed failure introspection. | Method-based: `self.assertEqual()`, `self.assertTrue()`. |
| **Parametrization** | Built-in `@pytest.mark.parametrize` for data-driven testing. | Requires external packages or custom loops. |
| **Reporting** | Rich plugin ecosystem (`pytest-html`) for visual HTML reports. | Basic text output by default. |

---

## 8. Execution Commands

1. **Run the Live Interactive Demonstration:**
   ```powershell
   python run_demo.py
   ```
2. **Run the Full Test Suite with HTML Report:**
   ```powershell
   python -m pytest tests/ --html=reports/report.html --self-contained-html --headless false
   ```
3. **Run the Unittest Comparison Suite:**
   ```powershell
   python -m unittest tests/test_unittest_comparison.py
   ```
4. **Open the Generated HTML Report:**
   ```powershell
   Start-Process reports/report.html
   ```

---

## 9. Conclusion
All 14 test scenarios across TC01–TC10 and the Unittest architectural comparison pass with 100% success rate. The framework satisfies all requirements of the project brief, student handout, and faculty review criteria.
