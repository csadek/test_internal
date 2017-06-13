import csv
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from WebElementWait import WebElementWait
from SMDriverFactory import driver_factory
import os, sys
import subprocess
from TestExceptionHandler import driverhandler
from robot.api import logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PCU_Simulator.PcuSim import PcuSim


class WirelessPackageDeploymentLibrary(object):

    def __init__(self):

        # Deployment Group Locators
        self.Create_DG_button = (By.ID, "add-facility-link")
        self.DG_textbox = (By.ID, "group-name")
        self.Switch_slider = (By.ID, "switch-slider")
        self.Save_button = (By.ID, "group-edit")
        self.Confirm_button = (By.ID, "yes-default")
        self.DG_added_name = (By.XPATH, ".//*[@id='deployment-group-grid-table']/tbody/tr/td[3]/div")

        # Wireless Packages Import Locators
        self.edge_file_input = os.path.join(os.path.dirname(__file__), 'MSEdge_FileUpload.py')
        self.Wireless_Packages_button =(By.ID, "wireless-link")
        self.Import_Package_button = (By.ID, "import-package")
        self.Select_file_button = (By.XPATH, ".//*[@id='modalBox']//input")
        self.Package_Password_textbox = (By.ID, "password")
        self.Invalid_Password_msg = (By.ID, "message-alert-text")
        self.Upload_button = (By.ID, "submit-upload")
        self.Confirm_Import_button = (By.ID, "confirm-import")
        self.WPs_added_id = (By.XPATH, ".//*[@id='wireless-package-grid-table']/tbody/tr/td[3]")

        # Wireless Packages deploy Locators
        self.Select_checkbox = (By.XPATH, ".//*[@id='wireless-package-grid-table']/tbody/tr/td[1]/input")
        self.Deploy_button = (By.ID, "wireless-group-deploy")
        self.Deployment_Facility_menu = (By.ID, "deployment-facility-list")
        self.DG_Name_dropdown_menu = (By.ID, "d-deployment-group")
        self.Next_DG_button = (By.ID, "next-deploy-group")
        self.Confirm_Deployment_button = (By.ID, "yes")
        self.Final_Deploy_button = (By.ID, "import-final")
        self.Transfers_completed_label = (By.XPATH, ".//*[@id='deployment-group-grid-table']/tbody/tr/td[7]")

        # Delete Wireless Package Locators
        self.Wireless_Packages_list = (By.XPATH, ".//*[@id='wireless-package-grid-table']/tbody/tr")
        self.WP_deletion_check = (By.XPATH, ".//td[1]/input")
        self.Delete_WP_button = (By.ID, "delete-package")
        self.Confirm_WP_deletion_button = (By.ID, "delete-grid-item")

        # Create instance from PcuSim
        self.pcusim = PcuSim()

        # Get the Wireless Package path
        #self.wireless_package_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) + "\Data\WirelessPackages")

    # Open Browser and Login then Navigate to Manage DeploymentGroups page Method
    @driverhandler
    def open_browser_and_login_then_navigate_to_manage_deployment_groups_page(self, browser, ip, username, password):
        self.driver = driver_factory.getDriver(browser, ip, username, password)
        self.driver.get(self.driver.current_url + "MVC/DeploymentGroup/ManageDeploymentGroups")

    # Create Deployment Group Method
    @driverhandler
    def create_deployment_group(self, deployment_group_name):
        # Wait for Create New Button element to be visible and Click
        WebElementWait.wait_for_element(self.driver, self.Create_DG_button)
        self.driver.find_element(*self.Create_DG_button).click()

        # Wait for Deployment Group Name textbox element to be visible and send keys with DG_name
        WebElementWait.wait_for_element(self.driver, self.DG_textbox)
        self.driver.find_element(*self.DG_textbox).send_keys(deployment_group_name)

        # Wait for Switch Slider Button element to be visible and Click
        WebElementWait.wait_for_element(self.driver, self.Switch_slider)
        self.driver.find_element(*self.Switch_slider).click()

        # Wait for Save Button element to be visible and Click
        if self.driver.name == "MicrosoftEdge":
            self.driver.execute_script("document.getElementById('" + self.Save_button[1] + "').click()")
        else:
            WebElementWait.wait_for_element(self.driver, self.Save_button)
            self.driver.find_element(*self.Save_button).click()

        # Wait for Yes Button element to be visible and Click
        WebElementWait.wait_for_element(self.driver, self.Confirm_button)
        self.driver.find_element(*self.Confirm_button).click()

        # Assert that Deployment group is created successfully
        # Get the Deployment group name created
        WebElementWait.wait_for_element(self.driver, self.DG_added_name)
        DG_created_name = self.driver.find_element(*self.DG_added_name).text

        # Assert that Deployment group name created equals deployment group name parameter
        assert(DG_created_name == deployment_group_name), "Deployment Group is not created successfully"

    # Import and deploy Wireless Package Method
    @driverhandler
    def import_wireless_package_and_deploy(self,shared_path, facility_name, DG_name, package_password, number_of_devices, device_version, server_address, server_port, aes_key):
        wireless_packages_path = shared_path+"\\WirelessPackages"
        WirelessPackages = os.listdir(wireless_packages_path)
        row_index = 0
        for package in WirelessPackages:
            # Wait for Wireless Package Button element to be visible and Click
            self.driver.find_element(*self.Wireless_Packages_button).click()

            # Wait for Import Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Import_Package_button)
            self.driver.find_element(*self.Import_Package_button).click()

            # Find the select file button element and send keys with full path of wireless package location
            if self.driver.name == "MicrosoftEdge":
                subprocess.Popen(['python.exe', self.edge_file_input,
                                              "\"" + wireless_packages_path + "\\" + package + "\""])
                select_file = self.driver.find_element(*self.Select_file_button)
                self.driver.execute_script("arguments[0].click();", select_file)
            else:
                self.driver.find_element(*self.Select_file_button).send_keys(
                                wireless_packages_path + "\\" + package)

            # Wait for Password textbox element to be visible and send keys with WP password
            WebElementWait.wait_for_element(self.driver, self.Package_Password_textbox)
            self.driver.find_element(*self.Package_Password_textbox).send_keys(package_password)
            sleep(3)

            # Wait for Upload Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Upload_button)
            self.driver.find_element(*self.Upload_button).click()

            # Check that security password is valid
            try:
                self.driver.find_element(*self.Invalid_Password_msg)
                raise Exception("Security Password is invalid, please insert another correct password")
            except (NoSuchElementException, StaleElementReferenceException):
                pass

            # Wait for Yes Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Confirm_Import_button)
            if self.driver.name == "MicrosoftEdge":
                confirm_button = self.driver.find_element(*self.Confirm_Import_button)
                self.driver.execute_script("arguments[0].click()", confirm_button)
            else:
                self.driver.find_element(*self.Confirm_Import_button).click()

            self.driver.refresh()
            added_packages = None

            # Verify that the data set inserted record appears on the UI
            trials = 10
            while trials > 0:
                added_packages = self.driver.find_elements(*self.WPs_added_id)
                if len(added_packages) < (row_index + 1):
                    sleep(3)
                    self.driver.refresh()
                    trials -= 1
                else:
                    break

            # Assert that Wireless Package is imported successfully
            WP_imported_id = self.driver.find_elements(*self.WPs_added_id)[row_index].text
            print ("Wireless Package with id: {} is imported successfully".format(WP_imported_id))

            # Wait for Checkbox Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Select_checkbox)
            self.driver.find_element(*self.Select_checkbox).click()

            # Wait for Deploy Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Deploy_button)
            self.driver.find_element(*self.Deploy_button).click()

            # Send keys with facility name to Deployment facility drop down menu
            WebElementWait.wait_for_element(self.driver, self.Deployment_Facility_menu)
            self.driver.find_element(*self.Deployment_Facility_menu).send_keys(facility_name)

            # Send keys with DG name to DG Name drop down menu
            WebElementWait.wait_for_element(self.driver, self.DG_Name_dropdown_menu)
            self.driver.find_element(*self.DG_Name_dropdown_menu).send_keys(DG_name)

            # Wait for Next button to be displayed and Click
            WebElementWait.wait_for_element(self.driver, self.Next_DG_button)
            self.driver.find_element(*self.Next_DG_button).click()

            # Wait for Yes Button element to be visible and Click    
            WebElementWait.wait_for_element(self.driver, self.Confirm_Deployment_button)
            self.driver.find_element(*self.Confirm_Deployment_button).click()

            # Wait for Deploy Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Final_Deploy_button)
            self.driver.find_element(*self.Final_Deploy_button).click()

            # Start PCU Sim and Connecting devices
            self.pcusim.start_simulator(number_of_devices, device_version, server_address, server_port, aes_key)

            # Verify that the uploaded Data Set is Deployed successfully for each PCU
            self.pcusim.verify_wireless_package_deployment()
            self.driver.refresh()
            WebElementWait.wait_for_element(self.driver, self.Transfers_completed_label)
            WP_Transfers = self.driver.find_elements(*self.Transfers_completed_label)[row_index].text
            assert (str(number_of_devices) == WP_Transfers), "Wireless Package deployment is not completed successfully"

            # Stop and Close the PCU Simulator
            self.pcusim.stop_simulator()
            self.pcusim.clear_existing_pcus()
            row_index += 1

    # End the test & Close Browser method
    def end_wireless_package_management_test(self):
        self.driver.close()

    # Delete WPs method
    @driverhandler
    def delete_wireless_packages(self):
        # Navigate to Wireless tab method
        WebElementWait.wait_for_element(self.driver, self.Wireless_Packages_button)
        self.driver.find_element(*self.Wireless_Packages_button).click()
        # Wait for page to load elements
        sleep(3)

        try:
            # Get the added Wireless Packages list
            WPs_List = self.driver.find_elements(*self.Wireless_Packages_list)
            # loop for the added WPs to apply delete method
            for package in WPs_List:
                # Click on check box
                package.find_element(*self.WP_deletion_check).click()

                # Wait for Delete button to be displayed and click
                WebElementWait.wait_for_element(self.driver, self.Delete_WP_button)
                self.driver.find_element(*self.Delete_WP_button).click()

                # Wait for Confirm Deletion button to be displayed and click
                WebElementWait.wait_for_element(self.driver, self.Confirm_WP_deletion_button)
                self.driver.find_element(*self.Confirm_WP_deletion_button).click()
                print("Wireless Package is deleted successfully")

        except (NoSuchElementException, StaleElementReferenceException):
            logger.console("No Wireless packages found to be deleted.")

        # Close the browser After Deletion
        self.driver.close()
