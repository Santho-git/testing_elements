## QA Automation Project – UI Component Testing

### Project Overview
This project demonstrates automation testing of web UI components using Selenium with Python. The goal is to create reusable, maintainable test scripts to verify component functionality, behavior, and UI interactions.

### Currently, the project covers:
* Slider (Material UI)
* Accordion (Material UI)
* Date Picker (jQuery UI)

This project highlights component-level testing, backend validation (if needed), and scalable automation practices suitable for real-world QA workflows.

### Tools & Technologies Used
* Programming Language: Python
* Automation Framework: Selenium WebDriver, PyTest
* Web Components: Material UI, jQuery UI
* Version Control: Git
* Others: ChromeDriver (for browser automation)

### Features & Functionality Tested
#### Slider (Material UI)
* Verify the slider is visible and enabled
* Validate min, max, and step values
* Test drag-and-drop functionality and value change
* Verify correct behavior for boundary values

#### Accordion (Material UI)
* Verify expand/collapse behavior
* Validate multiple accordion items open/close independently
* Ensure content visibility matches user interaction

#### Date Picker (jQuery UI)
* Verify date picker is visible and clickable
* Validate selection of specific dates
* Test navigation across months and years
* Confirm input field updates correctly upon selection

### How to Run the Tests
#### Clone the repository:
     git clone <repository-url>

#### Navigate to the project folder:
     cd testing_elements

#### Install dependencies:
    pip install -r requirements.txt

#### Run tests using PyTest:
    pytest tests/

### Key Learning / Achievements
* Implemented component-level UI automation using Selenium and Python.
* Practiced Pytest for reusable and maintainable automation scripts.
* Enhanced understanding of web element interactions.
* Built test scripts suitable for integration into larger automation frameworks.

### Future Improvements
* Add additional Material UI components for broader coverage.
* Implement data-driven testing for dynamic input scenarios.
* Generate HTML reports for test execution results.


