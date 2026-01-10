from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://mui.com/material-ui/react-accordion/")
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 5)

@pytest.fixture
def accordion(driver):
    navi = driver.find_element(
        By.XPATH, "(//span[contains(text(),'Expanded by default')])[2]"
    )
    navi.click()

    accordion = driver.find_element(
        By.XPATH, "(//div[starts-with(@id, 'demo-_R_')])[3]"
    )
    return accordion
#---------------------------Verify the expanded by default accordion is present--------------------------
def test_expanded_by_default_accordion_is_present(accordion):
    assert accordion.is_displayed()

#--------------------------------Verify there are two sections inside the accordion---------------------------------
def test_accordion_has_two_sections(accordion):
    sections = accordion.find_elements(
        By.XPATH, ".//button[starts-with(@id,'panel')]"
    )
    assert len(sections) == 2

#--------------------------Verify there are headers present in each section-------------------------------------

def test_verify_headers(accordion):
    text_find = accordion.find_elements(By.XPATH, ".//span[contains(@class,'MuiTypography-root')]")
    all_texts = [span.text.strip() for span in text_find]
    expected_texts= ["Expanded by default", "Header"]
    assert all_texts == expected_texts, f"Expected {expected_texts}, got {all_texts}"

#----------------------------A Helper Function--------------------------------
def assert_section_state(wait, section_button, should_be_expanded):
    xpath = ".//*[contains(@class,'Mui-expanded')]"

    if should_be_expanded:
        wait.until(
            lambda d: len(section_button.find_elements(By.XPATH, xpath)) > 0
        )
    else:
        wait.until(
            lambda d: len(section_button.find_elements(By.XPATH, xpath)) == 0
        )

#-------------------------------------Verify by default, the section 1 is expanded---------------------------------
def test_first_section_is_expanded_by_default(accordion, wait):
    section_button = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[1]")
    assert_section_state(wait, section_button, should_be_expanded=True)

#----------------------------------Verify by default, the section 2 is not expanded-------------------------------
def test_section_2_collapsed_by_default(accordion, wait):
    collapsed_element = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[2]")
    assert_section_state(wait, collapsed_element, should_be_expanded=False)

#-----------------------Verify clicking on the accordion header expands/closes the section----------------------------
def test_clicking_header_expands_and_collapses_sections(accordion, wait):

    # -------- Section 1 --------
    sect1 = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[1]")

    # initially expanded → click → collapse
    sect1.click()
    assert_section_state(wait, sect1, should_be_expanded=False)

    # click again → expand
    sect1.click()
    assert_section_state(wait, sect1, should_be_expanded=True)

    # -------- Section 2 --------
    sect2 = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[2]")

    # initially collapsed → click → expand
    sect2.click()
    assert_section_state(wait, sect2, should_be_expanded=True)

    # click again → collapse
    sect2.click()
    assert_section_state(wait, sect2, should_be_expanded=False)

def test_multiple_sections_can_be_expanded(accordion, wait):
    section = accordion.find_elements(By.XPATH, ".//button[starts-with(@id,'panel')]")
    section2 = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[2]")
    section2.click()
    expanded_sections = []
    for ele in section:
        expanded_sections.append(ele)
        for expanded in expanded_sections:
            assert_section_state(wait, expanded, should_be_expanded=True)

#-------------Verify clicking on the icon present at the side, expands and collapses the section----------------------

def test_icon_click_expands_and_collapses_section(accordion, wait):
    section2_click = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[2]")
    section2_click.click()
    icon_id = accordion.find_elements(By.XPATH, ".//span[contains(@class,'MuiAccordionSummary-expandIconWrapper')]")

    for icon in icon_id:
        # find the parent section button of this icon
        section_button = icon.find_element(By.XPATH, "./ancestor::button")

        # click → should close
        icon.click()
        assert_section_state(wait, section_button, should_be_expanded=False)

        assert "Mui-expanded" not in icon.get_attribute("class")

        transform_before = icon.value_of_css_property("transform")

        # click again → should open
        icon.click()
        assert_section_state(wait, section_button, should_be_expanded=True)

        assert "Mui-expanded" in icon.get_attribute("class"), "Icon is inverted unexpectedly"

        transform_after = icon.value_of_css_property("transform")

        # -----------------Verify that the icon becomes inverted (from 'v' to '^') when clicked on------------------
        assert transform_before != transform_after
        # at this point, both the sections in accordion is expected to be in open

#-----------------Verify the content is fully visible when expanded------------------------------
# start from the button, climb up to its accordion, then search inside it for the content

def assert_content_visible(wait, section_button, should_be_visible):

    content = section_button.find_element(
        By.XPATH,
        "./ancestor::h3"
        "/following-sibling::div[contains(@class,'MuiCollapse-root')]"
        "//div[contains(@class,'MuiAccordionDetails-root')]"
    )

    if should_be_visible:
        wait.until(lambda d: content.is_displayed())
        assert content.is_displayed(), "Accordion content is not visible"
        assert content.size["height"] > 0, "Accordion content is not fully expanded"
    else:
        wait.until(lambda d: not content.is_displayed())
        assert not content.is_displayed(), "Accordion content is visible"


def test_accordion_content_visibility(accordion, wait):

    content_section1 = accordion.find_element(
        By.XPATH, "(.//button[starts-with(@id,'panel')])[1]"
    )
    content_section2 = accordion.find_element(
        By.XPATH, "(.//button[starts-with(@id,'panel')])[2]"
    )

    # Section 1 expanded by default
    assert_section_state(wait, content_section1, should_be_expanded=True)
    assert_content_visible(wait, content_section1, should_be_visible=True)

    # Expand section 2
    content_section2.click()
    assert_section_state(wait, content_section2, should_be_expanded=True)
    assert_content_visible(wait, content_section2, should_be_visible=True)

    # Collapse section 1
    content_section1.click()
    assert_section_state(wait, content_section1, should_be_expanded=False)
    assert_content_visible(wait, content_section1, should_be_visible=False)

    # Collapse section 2
    content_section2.click()
    assert_section_state(wait, content_section2, should_be_expanded=False)
    assert_content_visible(wait, content_section2, should_be_visible=False)
