from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from WebElementWait import WebElementWait
from SMDriverFactory import driver_factory
from time import sleep
from robot.api import logger
from TestExceptionHandler import driverhandler


class CreateFacilityLibrary(object):

    def __init__(self):
        # Add Facility Locators
        self.Add_Facility_button = (By.ID, "add-facility-link")
        self.Facility_Name_textbox = (By.ID, "facilityName")
        self.Facility_Desc_textbox = (By.ID, "facilityDescription")
        self.Facility_Key_textbox = (By.ID, "facilityAeskey")
        self.Save_Facility_addition_button = (By.ID, "facility-edit")
        self.Continue_button = (By.ID, "continue-noApply")
        self.Confirm_Addition_message = (By.XPATH, ".//*[@id='facility-table']/tbody/tr/td[1]")

        # Add IP Address Range Locators
        self.Add_Range_button = (By.ID, "add-ip-range-link")
        self.IP_Start_textbox = (By.ID, "ip-address-start1")
        self.IP_End_textbox = (By.ID, "ip-address-end1")
        self.Save_Range_button = (By.ID, "ip-address-range-add")
        self.Confirm_Adding_IPStart_label = (By.XPATH, ".//*[@id='ip-table']/tbody/tr/td[1]")
        self.Confirm_Adding_IPEnd_label = (By.XPATH, ".//*[@id='ip-table']/tbody/tr/td[2]")

        # Apply Settings Locators
        self.Apply_Settings_button = (By.XPATH, ".//*[@id='message-alert-text']/button")
        self.Confirm_Action_button = (By.ID, "send-apply-action")

        # Delete Facility Locators
        self.Added_Facility_list = (By.XPATH, ".//*[@id='facility-table']/tbody/tr")
        self.Delete_Facility_button = (By.XPATH, ".//td[7]/button")
        self.Confirm_Deletion_button = (By.ID, "delete-grid-item")

    # Open Browser and Login then Navigate Method
    @driverhandler
    def open_browser_and_login_then_navigate_to_manage_network_page(self, browser, ip, username, password):
        # Open browser and login with valid username & password
        self.driver = driver_factory.getDriver(browser, ip, username, password)
        sleep(5)

        # Navigate to Manage Network page
        logger.console("| Navigating to: " + self.driver.current_url + "MVC/InfusionNetwork/ManageInfusionNetworks")
        self.driver.get(self.driver.current_url + "MVC/InfusionNetwork/ManageInfusionNetworks")

    # Add Facility Method
    @driverhandler
    def add_facility(self, facility_name, facility_desc, facility_key):
        # Click Add Facility button
        WebElementWait.wait_for_element(self.driver, self.Add_Facility_button)
        self.driver.find_element(*self.Add_Facility_button).click()

        # Enter Facility Name, Description & Key
        WebElementWait.wait_for_element(self.driver, self.Facility_Name_textbox)
        self.driver.find_element(*self.Facility_Name_textbox).send_keys(facility_name)
        self.driver.find_element(*self.Facility_Desc_textbox).send_keys(facility_desc)
        self.driver.find_element(*self.Facility_Key_textbox).send_keys(facility_key)

        # Clicking on Save facility button
        WebElementWait.wait_for_element(self.driver, self.Save_Facility_addition_button)
        self.driver.find_element(*self.Save_Facility_addition_button).click()

        # Clicking on confirmation button
        WebElementWait.wait_for_element(self.driver, self.Continue_button)
        self.driver.find_element(*self.Continue_button).click()

        # Clicking on Apply Settings button
        WebElementWait.wait_for_element(self.driver, self.Apply_Settings_button)
        self.driver.find_element(*self.Apply_Settings_button).click()

        # Clicking on Confirm Applying Settings button
        WebElementWait.wait_for_element(self.driver, self.Confirm_Action_button)
        self.driver.find_element(*self.Confirm_Action_button).click()

        # Get the created facility name and assert that facility added successfully
        WebElementWait.wait_for_element(self.driver, self.Confirm_Addition_message)
        facility_added_name = self.driver.find_element(*self.Confirm_Addition_message).text
        assert(facility_added_name == facility_name), "Facility wasn't added successfully"

    # Add IP Address Range Method
    @driverhandler
    def add_ip_address_range(self, ip_start, ip_end):
        # Click on Add IP Range button
        WebElementWait.wait_for_element(self.driver, self.Add_Range_button)
        self.driver.find_element(*self.Add_Range_button).click()

        # Entering IP Start & End
        WebElementWait.wait_for_element(self.driver, self.IP_Start_textbox)
        self.driver.find_element(*self.IP_Start_textbox).send_keys([i.replace(".", Keys.TAB) for i in ip_start])
        self.driver.find_element(*self.IP_End_textbox).send_keys([i.replace(".", Keys.TAB) for i in ip_end])

        # Clicking on save range button
        WebElementWait.wait_for_element(self.driver, self.Save_Range_button)
        self.driver.find_element(*self.Save_Range_button).click()

        # Clicking on confirm saving range button
        WebElementWait.wait_for_element(self.driver, self.Continue_button)
        self.driver.find_element(*self.Continue_button).click()

        # Clicking on Apply Settings button
        WebElementWait.wait_for_element(self.driver, self.Apply_Settings_button)
        self.driver.find_element(*self.Apply_Settings_button).click()

        # Clicking on Confirm Applying Settings button
        WebElementWait.wait_for_element(self.driver, self.Confirm_Action_button)
        self.driver.find_element(*self.Confirm_Action_button).click()

        # Get the added ip start & end and assert that they added successfully
        WebElementWait.wait_for_element(self.driver, self.Confirm_Adding_IPStart_label)
        ip_start_added = self.driver.find_element(*self.Confirm_Adding_IPStart_label).text
        ip_end_added = self.driver.find_element(*self.Confirm_Adding_IPEnd_label).text
        assert(ip_start_added == ip_start and ip_end_added == ip_end), "IP Address Range wasn't added successfully"

    # End the test & Close Browser method
    def end_create_facility_test(self):
        self.driver.close()

    # delete facility method
    @driverhandler
    def delete_facilities(self):
        # Get the added facilities list
        Facilities_List = self.driver.find_elements(*self.Added_Facility_list)

        # loop for the added facility to apply delete method
        for facility in Facilities_List:
            # Wait for Delete Button then click on it
            WebElementWait.wait_for_element(self.driver, self.Delete_Facility_button)
            facility.find_element(*self.Delete_Facility_button).click()

            # Wait for confirm deletion button to be displayed and click
            WebElementWait.wait_for_element(self.driver, self.Confirm_Deletion_button)
            self.driver.find_element(*self.Confirm_Deletion_button).click()

            # Wait for Continue button to be displayed and click
            WebElementWait.wait_for_element(self.driver, self.Continue_button)
            self.driver.find_element(*self.Continue_button).click()

            # Clicking on Apply Settings button
            WebElementWait.wait_for_element(self.driver, self.Apply_Settings_button)
            self.driver.find_element(*self.Apply_Settings_button).click()

            # Clicking on Confirm Applying Settings button
            WebElementWait.wait_for_element(self.driver, self.Confirm_Action_button)
            self.driver.find_element(*self.Confirm_Action_button).click()

            print("Facility is deleted successfully")

        # Close the browser After Deletion
        self.driver.close()
