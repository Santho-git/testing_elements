## The goal of this project is to automate testing for slider component

### Overview
The goal of this project is a componnt level UI test automation on emphasis of test design, edge cases to validate the behavior of slider component present in Material UI website using Python, Selenium Webdriver and Pytest

### Test target
The slider taken for example is taken from Material UI website and this is intented for learning purposes only

### Manual test cases for checking a slider with tooltip
1. Verify if the required slider is present in the given page
2. Verify the total number of sliders present in the section
3. Verify header of each of the sliders present
4. Verify the default position of the slider when a user open the page newly
5. Verify slider can be moved to the minimum value and the tooltip displays the correct value
6. Verify slider can be moved to the maximum value and the tooltip displays the correct value
7. Verify slider can be moved to any intermediate value and the tooltip dispalys the correct value
8. Verify the tooltip appears on the slider handle while dragging
9. Verify the value of the tooltip changes dynamically when the tooltip is being dragged
10. verify the tooltip remains or disappears after releasing the slider handle
11. Verify the tooltip remains correctly alinged above the slider handle at positions
12. Verify tooltip does not go outside or it does not overlap with the other UI elements present on the screen
13. Verify the tooltip does not move below the minimum range
14. Verify the tooltip does not move above the maximum range

### Tech stack
* Language: Python
* Automation web tool: Selenium web driver
* Test framework: Pytest
* Browser: Google chrome

### Design highlights
* Reusable PyTest fixture for browser setup and tear down
* Explicit waits instead of hard coded sleeps
* Functions and class to reduce duplication

### How to run tests
#### Prerequisites
* Python 3.x
* Google chrome
* Chrome driver
#### Install dependencies
pip install selenium pytest
#### Run tests
pytest

### Future scope
This test script is written for testing only one slider component. This will be extended to other three siblings and HTML report generation and screenshot capture will be done as future updations.
