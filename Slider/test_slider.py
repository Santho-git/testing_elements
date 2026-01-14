from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver import ActionChains
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://mui.com/material-ui/react-slider/")
    yield driver
    driver.quit()

@pytest.fixture
def customization_section(driver):
    wait = WebDriverWait(driver, 5)

    # Navigate to Customization
    navi = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Customization']")
    ))
    navi.click()

    # Verify Customization section
    customization = driver.find_element(
        By.XPATH,
        "//a[@class='title-link-to-anchor'][normalize-space()='Customization']"
    )
    assert customization.text == "Customization"

    # Return customization demo container
    custom = driver.find_element(
        By.XPATH,
        "//h2[normalize-space()='Customization']"
        "/following::div[starts-with(@id,'demo-')][1]"
    )

    return custom

#-------------------------------Verifying if there are four sections in the slider---------------------------------
def test_customization_has_four_sliders(customization_section):
    sliders = customization_section.find_elements(
        By.XPATH, ".//div[starts-with(@class, 'MuiBox-root')]"
    )

    assert len(sliders) == 4

#-----------------------------------testing if there are four sections are labelled correctly-------------------------
def test_slider_headings_present(customization_section):
    sliders = customization_section.find_elements(
        By.XPATH, ".//div[starts-with(@class, 'MuiBox-root')]"
    )

    headings = []
    for slider in sliders:
        texts = slider.find_elements(By.TAG_NAME, "p")
        for t in texts:
            if t.text:
                headings.append(t.text)

    expected_headers = ['iOS', 'pretto.fr', 'Tooltip value label', 'Airbnb']

    assert sorted(headings) == sorted(expected_headers)

#-----------------------------------Fixture for slider elements-------------------------------------------------
@pytest.fixture
def ios_slider_elements(customization_section):
    slider_root = customization_section.find_element(
        By.XPATH,
        ".//p[normalize-space()='iOS']"
        "/ancestor::div[contains(@class,'MuiBox-root')]"
        "//span[contains(@class,'MuiSlider-root')]"
    )

    slider_track = slider_root.find_element(
        By.XPATH, ".//span[contains(@class,'MuiSlider-track')]"
    )

    slider_thumb = slider_root.find_element(
        By.XPATH, ".//span[contains(@class,'MuiSlider-thumb')]"
    )

    return {
        "root": slider_root,
        "track": slider_track,
        "thumb": slider_thumb
    }

#----------------------------Verification of slider handler label---------------------------------------------------
def test_ios_slider_default_value(ios_slider_elements):
    slider_thumb = ios_slider_elements["thumb"]

    slider_label = slider_thumb.find_element(
        By.XPATH, ".//span[contains(@class,'MuiSlider-valueLabelLabel')]"
    )

    assert int(slider_label.text) == 60

#------------------------A helper function for calculating percentage-----------------------------------
def get_slider_percentage(slider_track):
    track_width_px = slider_track.value_of_css_property("width")
    parent = slider_track.find_element(By.XPATH, "..")
    parent_width_px = parent.value_of_css_property("width")

    track_width = int(track_width_px.replace("px", ""))
    parent_width = int(parent_width_px.replace("px", ""))

    if parent_width == 0:
        raise ValueError("Parent width is zero")

    percentage = int((track_width / parent_width) * 100)

    return percentage

#-------------------------------Calculating default percentage------------------------------------------
def test_ios_slider_default_percentage(ios_slider_elements):
    slider_track = ios_slider_elements["track"]

    percentage = get_slider_percentage(slider_track)

    assert percentage == 60

#----------------------------A helper function for calculating overlaps------------------------------
def is_overlapping(r1, r2):
    return not (
        r1['x'] + r1['width']  < r2['x'] or
        r2['x'] + r2['width']  < r1['x'] or
        r1['y'] + r1['height'] < r2['y'] or
        r2['y'] + r2['height'] < r1['y']
    )

#--------------------------Class for handling slider movements---------------------------------------------
class Slider:
    def __init__(self, driver, thumb, initial_value=60):
        self.driver = driver
        self.thumb = thumb
        self.current_value = initial_value

    def move_to(self, target_value):
        delta = target_value - self.current_value
        offset = delta * 3.2

        ActionChains(self.driver) \
            .click_and_hold(self.thumb) \
            .move_by_offset(offset, 0) \
            .release() \
            .perform()

        self.current_value = target_value

    def get_tooltip_value(self):
        label = self.thumb.find_element(
            By.XPATH,
            ".//span[contains(@class,'MuiSlider-valueLabelLabel')]"
        )
        return int(label.text)

@pytest.fixture
def ios_slider(driver, ios_slider_elements):
    return Slider(
        driver=driver,
        thumb=ios_slider_elements["thumb"],
        initial_value=60
    )

#--------------------------Verifying the default range is 60-------------------------------------------
def test_ios_slider_default(ios_slider):
    assert ios_slider.get_tooltip_value() == 60

#---------------------------Verifying if the slider handler is moving to zero------------------------------
def test_ios_slider_move_to_zero(ios_slider):
    ios_slider.move_to(0)
    assert ios_slider.get_tooltip_value() == 0

#-------------------------Verifying the maximum limit of the slider handler---------------------------
def test_ios_slider_move_to_max(ios_slider):
    ios_slider.move_to(100)
    assert ios_slider.get_tooltip_value() == 100

#------------------------Verifying if the slider handler moves for a random number-------------------------
def test_ios_slider_move_to_random(ios_slider):
    value = random.randint(1, 100)
    ios_slider.move_to(value)
    assert ios_slider.get_tooltip_value() == value

#-------------------------------Verifying if the slider moves far in front of the minimum limit---------------
def test_ios_slider_below_min_boundary(ios_slider):
    ios_slider.move_to(-50)
    assert ios_slider.get_tooltip_value() == 0

#--------------------------Verifying if the slider moves beyond the maximum limit--------------------
def test_ios_slider_above_max_boundary(ios_slider):
    ios_slider.move_to(150)
    assert ios_slider.get_tooltip_value() == 100

#-----------------Verifying if the tooltip is visible while dragging------------------------------------------
def test_ios_slider_tooltip_visible_while_dragging(driver, ios_slider_elements):
    slider_thumb = ios_slider_elements["thumb"]

    actions = ActionChains(driver)

    # Start drag
    actions.click_and_hold(slider_thumb).perform()

    tooltip = slider_thumb.find_element(
        By.XPATH, ".//span[contains(@class,'MuiSlider-valueLabel')]"
    )
    assert tooltip.is_displayed()

    # Move slightly
    actions.move_by_offset(10, 0).perform()
    assert tooltip.is_displayed()

    # Release drag
    actions.release().perform()

#-------------------------------Verifying if the tooltip overlaps with the text above-----------------------
def test_ios_slider_tooltip_not_overlap_label(driver, ios_slider_elements):
    slider_thumb = ios_slider_elements["thumb"]

    actions = ActionChains(driver)
    actions.click_and_hold(slider_thumb).perform()

    tooltip = slider_thumb.find_element(
        By.XPATH, ".//span[contains(@class,'MuiSlider-valueLabel')]"
    )

    ios_label = driver.find_element(By.XPATH, "//p[normalize-space()='iOS']")

    assert not is_overlapping(ios_label.rect, tooltip.rect), \
        "Tooltip overlaps with iOS label"

    actions.release().perform()


