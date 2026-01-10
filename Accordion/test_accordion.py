from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://mui.com/material-ui/react-accordion/")
wait = WebDriverWait(driver, 5)

# for navigating to the section expanded by default accordion for visualizing
navi = driver.find_element(By.XPATH, "(//span[contains(text(),'Expanded by default')])[2]")
navi.click()

#---------------------------Verify the expanded by default accordion is present--------------------------
# finding the element where the element is present and checking if the element is getting displayed or not
accordion = driver.find_element(By.XPATH, "(//div[starts-with(@id, 'demo-_R_')])[3]")
assert accordion.is_displayed()
print("element found")

#--------------------------------Verify there are two sections inside the accordion---------------------------------
section = accordion.find_elements(By.XPATH, ".//button[starts-with(@id,'panel')]")
total = len(section)
assert total == 2
print("the number of sections present is", total)

#--------------------------Verify there are headers present in each section-------------------------------------
text_find = accordion.find_elements(By.XPATH, ".//span[contains(@class,'MuiTypography-root')]")
all_texts = [span.text.strip() for span in text_find]
print(all_texts)
EXPECTED_LIST = ["Expanded by default", "Header"]
assert all_texts == EXPECTED_LIST, f"Expected {EXPECTED_LIST}, got {all_texts}"
time.sleep(1)

#----------------------------A Helper Function--------------------------------
def assert_section_state(section_button, should_be_expanded):
    if should_be_expanded:
        wait.until(
            lambda d: len(
                section_button.find_elements(
                    By.XPATH, ".//*[contains(@class,'Mui-expanded')]"
                )
            ) > 0
        )
    else:
        wait.until(
            lambda d: len(
                section_button.find_elements(
                    By.XPATH, ".//*[contains(@class,'Mui-expanded')]"
                )
            ) == 0
        )
#-------------------------------------Verify by default, the section 1 is expanded---------------------------------
expanded_element = accordion.find_element(By.XPATH,"(.//button[starts-with(@id,'panel')])[1]")
assert_section_state(expanded_element, should_be_expanded = True)
print("First section is expanded as expected")

#----------------------------------Verify by default, the section 2 is not expanded-------------------------------
collapsed_element = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[2]")
assert_section_state(collapsed_element, should_be_expanded = False)
print("Second section is collapsed as expected")

#-----------------------Verify clicking on the accordion header expands/closes the section----------------------------
# Verification of header behavior for section 1
sect1_click = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[1]")

# initially section 1 is expanded
sect1_click.click()

# after clicking, section 1 will be collapsed
assert_section_state(sect1_click, should_be_expanded = False)
print("First section closed successfully")

# expanding the section1 again to verify if it is expanding
sect1_click.click()
assert_section_state(sect1_click, should_be_expanded = True)

# Verification of header behavior for section 2
sect2_click = accordion.find_element(By.XPATH, "(.//button[starts-with(@id,'panel')])[2]")

# initially section 1 is expanded
sect2_click.click()

# after clicking, section 2 will be opened
assert_section_state(sect2_click, should_be_expanded = True)
print("Second section opened successfully")

# collapsing section 2 after expanding
sect2_click.click()
assert_section_state(sect2_click, should_be_expanded = False)
print("Second section closed successfully")

sect1_click.click()

#--------------------------------------Verify multi open expansion-------------------------------------------
section = accordion.find_elements(By.XPATH, ".//button[starts-with(@id,'panel')]")
expanded_sections = []
for ele in section:
    ele.click()
    expanded_sections.append(ele)
    for expanded in expanded_sections:
        assert_section_state(expanded, should_be_expanded=True)
# here, both sections are in open

#-------------Verify clicking on the icon present at the side, expands and collapses the section----------------------
icon_id = accordion.find_elements(By.XPATH, ".//span[contains(@class,'MuiAccordionSummary-expandIconWrapper')]")
for icon in icon_id:
    # find the parent section button of this icon
    section_button = icon.find_element(By.XPATH, "./ancestor::button")

    # click → should close
    icon.click()
    assert_section_state(section_button, should_be_expanded=False)
    print("Section collapsed via icon")

    assert "Mui-expanded" not in icon.get_attribute("class")

    transform_value1 = icon.value_of_css_property("transform")

    # click again → should open
    icon.click()
    assert_section_state(section_button, should_be_expanded=True)
    print("Section expanded via icon")

    assert "Mui-expanded" in icon.get_attribute("class"), "Icon is inverted unexpectedly"

    transform_value2 = icon.value_of_css_property("transform")

    # -----------------Verify that the icon becomes inverted (from 'v' to '^') when clicked on------------------
    if transform_value1 != transform_value2:
        assert "success"
    else:
        assert "failed"

# at this point, both the sections in accordion is expected to be in open

#-----------------Verify the content is fully visible when expanded------------------------------
# start from the button, climb up to its accordion, then search inside it for the content

def assert_content_visible(content_section_button, content_should_be_visible):
    content= content_section_button.find_element(
        By.XPATH,
        "./ancestor::h3"
        "/following-sibling::div[contains(@class,'MuiCollapse-root')]"
        "//div[contains(@class,'MuiAccordionDetails-root')]"
    )
    if content_should_be_visible:
        wait.until(lambda d: content.is_displayed())
        assert content.is_displayed(), "Accordion content is not visible"
        assert content.size["height"] > 0, "Accordion content is not fully expanded"
    else:
        wait.until(lambda d: not content.is_displayed())
        assert not content.is_displayed(), "Accordion content is visible"


# verification of content for section 1
# expanded view
content_sect1_button = accordion.find_element(
    By.XPATH, "(.//button[starts-with(@id,'panel')])[1]"
)

assert_section_state(content_sect1_button, should_be_expanded=True)
assert_content_visible(content_sect1_button, content_should_be_visible= True)


# verification of content for section 2
content_sect2_button = accordion.find_element(
    By.XPATH, "(.//button[starts-with(@id,'panel')])[2]"
)

# expanded view
assert_section_state(content_sect2_button, should_be_expanded=True)
assert_content_visible(content_sect2_button, content_should_be_visible= True)

content_sect1_button.click()

assert_section_state(content_sect1_button, should_be_expanded=False)
assert_content_visible(content_sect1_button, content_should_be_visible= False)

content_sect2_button.click()

assert_section_state(content_sect2_button, should_be_expanded=False)
assert_content_visible(content_sect2_button, content_should_be_visible= False)
driver.quit()
