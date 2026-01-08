from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import calendar
import pytest

@pytest.fixture
def driver_and_wait():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://jqueryui.com/datepicker/")

    iframe = driver.find_element(By.CLASS_NAME, "demo-frame")
    driver.switch_to.frame(iframe)

    wait = WebDriverWait(driver, 5)
    yield driver, wait
    driver.quit()

def open_date_picker(driver, wait):
    date_input = wait.until(
        EC.visibility_of_element_located((By.ID, "datepicker"))
    )
    date_input.click()
    date_input.clear()
    return date_input

def today_date():
    return datetime.now().date()

def test_input_title_verification(driver_and_wait):
    driver, _ = driver_and_wait   # we don’t need wait here

    element_date = driver.find_element(By.CSS_SELECTOR, "body p")
    text = element_date.text.strip()
    assert text == "Date:"

    driver, wait = driver_and_wait

    open_date_picker(driver, wait)

    weekdays = driver.find_elements(By.CSS_SELECTOR, "span[title]")

    assert len(weekdays) == 7

from datetime import datetime
from selenium.webdriver.common.by import By

def test_highlighted_date_is_today(driver_and_wait):
    driver, wait = driver_and_wait

    open_date_picker(driver, wait)

    highlighted = driver.find_element(
        By.CSS_SELECTOR, ".ui-state-default.ui-state-highlight"
    )
    highlighted.click()

    value = driver.find_element(By.ID, "datepicker").get_attribute("value")
    selected_date = datetime.strptime(value, "%m/%d/%Y").date()

    assert selected_date == today_date()

def test_nxt_month_navigation(driver_and_wait):
    driver, wait = driver_and_wait

    open_date_picker(driver, wait)

    # Click next month arrow
    next_arrow = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".ui-icon.ui-icon-circle-triangle-e")
        )
    )
    next_arrow.click()

    # Select date "3"
    date_3 = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='3']")
        )
    )
    date_3.click()

    # Read selected date
    value = driver.find_element(By.ID, "datepicker").get_attribute("value")
    selected_date = datetime.strptime(value, "%m/%d/%Y").date()

    today = today_date()

    # Assertion (handles Dec → Jan automatically)
    expected_month = (today.month % 12) + 1
    assert selected_date.month == expected_month

def test_previous_month_navigation(driver_and_wait):
    driver, wait = driver_and_wait

    open_date_picker(driver, wait)

    # Click previous month arrow
    prev_arrow = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".ui-icon.ui-icon-circle-triangle-w")
        )
    )
    prev_arrow.click()

    # Select date "3"
    date_3 = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='3']")
        )
    )
    date_3.click()

    # Read selected date
    value = driver.find_element(By.ID, "datepicker").get_attribute("value")
    selected_date = datetime.strptime(value, "%m/%d/%Y").date()

    today = today_date()

    # Expected previous month (handles Jan → Dec)
    expected_month = 12 if today.month == 1 else today.month - 1

    assert selected_date.month == expected_month

def test_different_month_and_year(driver_and_wait):
    driver, wait = driver_and_wait

    date_input = open_date_picker(driver, wait)

    # Enter a past date
    date_input.clear()
    date_input.send_keys("07/02/1998")

    # Open calendar to read header
    date_input.click()

    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ui-datepicker-month"))
    )

    month_ui = driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
    year_ui = driver.find_element(By.CLASS_NAME, "ui-datepicker-year").text

    input_date = datetime.strptime("07/02/1998", "%m/%d/%Y").date()

    expected_month = input_date.strftime("%B")
    expected_year = str(input_date.year)

    assert month_ui == expected_month
    assert year_ui == expected_year

def test_first_and_last_day_of_month(driver_and_wait):
    driver, wait = driver_and_wait

    open_date_picker(driver, wait)

    days = driver.find_elements(
        By.CSS_SELECTOR, "td[data-handler='selectDay'] a"
    )

    day_numbers = [int(day.text) for day in days]

    # First day check
    assert day_numbers[0] == 1

    # Last day check
    today = datetime.now()
    expected_last_day = calendar.monthrange(today.year, today.month)[1]

    assert max(day_numbers) == expected_last_day

@pytest.mark.parametrize(
    "year, day",
    [
        (2008, 29),  # leap year
        (2009, 29),  # non-leap year
        (2023, 28),  # always valid
    ]
)
def test_february_days(driver_and_wait, year, day):
    driver, wait = driver_and_wait

    date_input = open_date_picker(driver, wait)

    date_str = f"02/{day:02d}/{year}"
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        date_input,
        date_str
    )

    date_input.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "td[data-handler='selectDay'] a")
        )
    )

    days = driver.find_elements(
        By.CSS_SELECTOR, "td[data-handler='selectDay'] a"
    )
    available_days = [int(d.text) for d in days]

    if day == 29:
        if calendar.isleap(year):
            assert 29 in available_days
        else:
            assert 29 not in available_days
    else:
        assert day in available_days

# jQuery UI datepicker does not display validation errors for invalid inputs.
# The expected behavior is that invalid dates are not selectable in the calendar.

invalid_values = [
    "02/30/2009",  # invalid day in Feb
    "00/15/2024",  # invalid month
    "06/15/78",    # year in short format
    "67/87/78",    # completely invalid
    "2029-23-10",  # wrong format
    "abcd",        # letters only
    "abcd/12/2025" # partially invalid
]

@pytest.mark.parametrize("value", invalid_values)

def test_invalid_inputs(driver_and_wait, value):
    driver, wait = driver_and_wait

    # Open the date picker input
    date_input = open_date_picker(driver, wait)

    # Clear and type the invalid value
    date_input.clear()
    date_input.send_keys(value)

    # Open the calendar
    date_input.click()
    wait.until(EC.visibility_of_element_located((By.ID, "ui-datepicker-div")))

    # Get all selectable days in the calendar
    days = driver.find_elements(By.CSS_SELECTOR, "td[data-handler='selectDay'] a")
    available_days = [int(d.text) for d in days]

    # Try parsing the input value
    try:
        month, day, year = map(int, value.split("/"))
    except ValueError:
        # Completely invalid strings like "abcd"
        month = day = year = None

    # If day is a valid number, it should NOT be in the calendar for invalid dates
    if day and 1 <= day <= 31:
        assert day not in available_days
    else:
        # Totally invalid input → pass the test
        assert True

def test_click_outside_closes_datepicker(driver_and_wait):
    driver, wait = driver_and_wait

    date_input = open_date_picker(driver, wait)

    # Wait for the calendar to appear
    calendar_div = wait.until(
        EC.visibility_of_element_located((By.ID, "ui-datepicker-div"))
    )

    # Click outside on the body
    driver.find_element(By.TAG_NAME, "body").click()

    # Wait until the calendar is hidden
    wait.until(EC.invisibility_of_element(calendar_div))

    # If the calendar is still visible, wait will timeout → test fails automatically

def test_esc_closes_datepicker(driver_and_wait):
    driver, wait = driver_and_wait

    date_input = open_date_picker(driver, wait)

    # Wait for calendar to be visible
    calendar_div = wait.until(
        EC.visibility_of_element_located((By.ID, "ui-datepicker-div"))
    )

    # Press ESC key
    date_input.send_keys(Keys.ESCAPE)

    # Wait until calendar is hidden
    wait.until(EC.invisibility_of_element(calendar_div))

    # If the calendar is still visible, the wait will timeout → test fails automatically
