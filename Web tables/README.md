## Web Tables

### Overview
The goal of this project is to create an automation test script using Selenium Python for component level testing with emphasis on test design, edge cases, and maintainability built to validate the behavior of the web table.

### Test target
The test target for this project is a web table taken from Material UI website which is intented for learning purposes only

### Objectives
* Validate the functionality of the web table
* Practice clean test design using PyTest fixtures and parametrization
* Avoid assumptions about UI validation that the application does not provide
* Cover test cases related to functionality, UI and edge case scenarios

### Structure of web table:
* The web table component is a dynamic one
* The table has 6 columns
* First one has check box, next first name, last name, age, full name and then an empty column
* It has pagination for moving forward and backward
* It has an option to display rows according to the condition required by the user (For example, it can displays, 5, 10 or 15 records at a time).
* We can not edit or add or delete the rows or columns.
* There is no filter. But we can click on the check boxes.
* When clicked on check boxes, the number of checked rows will be displayed in the bottom.

### Manual test cases for testing the web table:
1. Verify the table loads correctly on page load.
2. Verify all 6 columns are displayed with correct headers: checkbox, first name, last name, age, full name, and empty column.
3. Verify the number of rows matches the expected dataset for the selected row count (5, 10, or 15).
4. Verify the table width fits properly within the page layout.
5. Verify the table handles empty datasets properly 
6. Verify rows display correct data under each column.
7. Verify each row checkbox can be selected individually.
8. Verify each row checkbox can be deselected individually.
9. Verify the total number of selected rows updates correctly at the bottom when checkboxes are clicked.
10. Verify selecting all checkboxes updates the total selected count correctly.
11. Verify checkboxes maintain their state when navigating between pages.
12. Verify pagination controls navigate to the next page correctly.
13. Verify pagination controls navigate to the previous page correctly.
14. Verify the table displays the correct rows per page when navigating.
15. Verify the table handles the last page correctly with fewer than the maximum rows.
16. Verify changing the “rows per page” option (5, 10, 15) displays the correct number of rows.
17. Verify changing rows per page retains the correct page data and selection states.
18. Verify navigation through pages does not break the table layout or functionality.
19. Verify text in each column is fully visible or properly truncated if needed.
20. Verify the total selected rows display at the bottom is always visible and updated.

### Tech Stack
* Language: Python
* Automation Tool: Selenium WebDriver
* Test Framework: PyTest
* Browser: Google Chrome
* Test Target: Web table

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

