## Automation testing for a date picker

📌 Test Target: This project uses the public jQuery UI Datepicker demo site, which is intended for learning and demonstration purposes.

### Overview:
This project is a Component-level UI test automation with emphasis on test design, edge cases, and maintainability built to validate the behavior of the jQuery UI Datepicker using Python, Selenium WebDriver, and PyTest.

### Objectives
* Validate datepicker functionality from a user-behavior perspective
* Cover edge cases related to dates, months, and years
* Practice clean test design using PyTest fixtures and parametrization
* Avoid assumptions about UI validation that the application does not provide

### Manaual test cases for testing a date picker
1. Verify date picker opens when clicked on the date field
2. Verify the date picker closes when a date is selected
3. Verify the date picker closes when clicking outside the calendar
4. Verify the date picker closes when esc key is pressed
5. Verify the selected date appears on the input field correctly after selecting the date
6. Verify the current date is getting highlighted
8. Verify next month navigation
9. Verify previous month navigation
10. Verify selecting valid date
11. Verify date selection for different months and different years
12. Verify the first day of the month
13. Verify the last date of the month
14. Verify selection of february 28 during non leap years
15. Verify selection of february 29 during leap years
16. Verify invalid entry of inputs in input fields

### Tech Stack
* Language: Python
* Automation Tool: Selenium WebDriver
* Test Framework: PyTest
* Browser: Google Chrome
* Test Target: jQuery UI Datepicker

### Design Highlights
* Reusable PyTest fixture for browser setup and teardown
* Explicit waits (WebDriverWait) instead of hard sleeps
* Helper functions to reduce duplication
* Parametrized tests for better coverage with minimal code
* Assertions aligned with actual UI behavior, not assumptions

### How to Run the Tests
#### Prerequisites
* Python 3.x
* Google Chrome
* ChromeDriver (compatible with your Chrome version)

#### Install dependencies
pip install selenium pytest

#### Run tests
Pytest
