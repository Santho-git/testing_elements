## Automate testing for the accordion componenent

## Test Target
The accordion taken for example is taken from Material UI website and this is intented for learning purposes only

### Overview
The goal of this project is a componnt level UI test automation on emphasis of test design, edge cases to validate the behavior of accordion component present in Material UI website using Python, Selenium Webdriver and Pytest

### Objectives
* Validate the functionality of the accordion component from a user's perspective
* Cover edge cases related to expanding, collapsing and visibility of the sections present in the accordion
* Aviod assumptions about UI validation that the application does not provide

### Structure of accordion
1. The accordion taken for example is, Expanded by deafult accordion
2. This accordion has two sections in it
3. At first, the accordion will have one section expanded
4. When clicked on the header, the section will expand
5. It is an example for multi opening accordion
6. When clicked on the header, the accordion will expand or collapse
7. There is an icon in the side, which when clicked will change direction (v-^)

### Manual test cases for accordion component
1. Verify there are two sections present in the accordion
2. Verify there are headers present in each section
3. Verify there are icons present the side of each section for expanding or collapsing
4. Verify if accordion is collapsed by default except section 1
5. Verify clicking on the accordion header expands the section
6. Verify clicking on the expanded header collapses to original state when clicked again
7. Verify clicking on the header opens and closes
8. Verify clicking on the icon present at the side, expands and collapses the section
9. Verify that the icon becomes inverted (from 'v' to '^') when clicked on
10. Verify clicking on outside the accordion component does not change or affect the state of the accordion
11. Verify the content is fully visible when expanded
12. Verify the content is fully hidden when collapsed

  ### Tech stack
  * Language: Python
  * Automation web tool: Selenium web driver
  * Test framework: Pytest
  * Browser: Google chrome
  * Test target: Expanded by deafault accordion

  ### Design highlights
  * Reusable PyTest fixture for browser setup and tear down
  * Explicit waits instead of hard coded sleeps
  * Functions to reduce duplication
  * Parameterized tests for better coverage
  * Assertions aligned with actual Ui behavior
 
  ### How to run tests
  #### Prerequisites
  * Python 3.x
  * Google chrome
  * Chrome driver
 
  #### Install dependencies
    pip install selenium pytest

  #### Run tests
    pytest







