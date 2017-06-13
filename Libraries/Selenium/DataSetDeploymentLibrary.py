from selenium.webdriver.common.by import By
import os, sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from WebElementWait import WebElementWait
from SMDriverFactory import driver_factory
from time import sleep
from robot.api import logger
import subprocess
from TestExceptionHandler import driverhandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PCU_Simulator.PcuSim import PcuSim


class DataSetDeploymentLibrary(object):

    def __init__(self):
        self.edge_file_input = os.path.join(os.path.dirname(__file__), 'MSEdge_FileUpload.py')

        # Deploy DataSets Locators
        self.Import_DataSet_button = (By.ID, "import-data")
        self.Dataset_status = (By.XPATH, ".//td[5]")
        self.Browse_button = (By.XPATH, ".//*[@id='modalBox']//input")
        self.Upload_button = (By.XPATH, ".//*[@class='modal-body global-body']/div[2]/button")
        self.Next_button = (By.ID, "next-upload")
        self.Facility_Assign_button = (By.ID, "facility-assign")
        self.Right_Cursor = (By.ID, "search_rightAll")
        self.Activate_button = (By.ID, "activate-all")
        self.Confirm_Activate_button =(By.ID, "confirm-activate")
        self.Confirm_Activate_message = (By.ID, "ok")
        self.Imported_Datasets_list = (By.XPATH, ".//*[@id='dataSetGrid']/div/div/div/div/table/tbody//tr/td[5]")
        self.Datasets_IDs = (By.XPATH, ".//*[@id='dataSetGrid']/div/div/div/div/table/tbody//tr/td[4]")
        self.pcusim = PcuSim()

    # Open Browser and Login then Navigate to Manage DataSets page Method
    @driverhandler
    def open_browser_and_login_then_navigate_to_manage_data_sets_page(self, browser, ip, username, password):
        self.driver = driver_factory.getDriver(browser, ip, username, password)
        self.driver.get(self.driver.current_url + "MVC/DataSet/ManageDataSets")

    # Check that user is authorized and redirected to Manage Datasets page
    @driverhandler
    def the_user_should_be_authorized_to_access(self):
        assert (("ManageDataSets" in self.driver.current_url) == True), "User should be authorized but error happened"
        print ("User is authorized to view this page")

    # Open Browser and Login with non authorized facility user then Navigate to Manage DataSets page Method
    @driverhandler
    def login_with_non_authorized_facility_user_then_navigate_to_manage_data_sets_page(self, browser, ip, non_admin_username, non_admin_password):
        self.driver = driver_factory.getDriver(browser, ip, non_admin_username, non_admin_password)
        self.driver.get(self.driver.current_url + "MVC/DataSet/ManageDataSets")

    # Check that user is not authorized and redirected to not authorized page
    @driverhandler
    def the_user_should_not_be_authorized_to_access(self):
        assert (("Not Authorized" in self.driver.page_source) == True), "User should not be authorized but error happened"
        print ("User is not authorized to view this page")

    # Import and Deploy Data sets then verify deployment
    @driverhandler
    def upload_and_deploy_data_sets(self, shared_path, number_of_devices, device_version, server_address, server_port, aes_key):
        # Upload DataSets
        data_sets_path = shared_path+"\\DataSets"
        data_sets = os.listdir(data_sets_path)
        print ("Importing and activating {} data sets".format(str(len(data_sets))))
        # Loop through the Data Sets to upload then deploy
        row_index = 0
        for data_set in data_sets:
            print (("Importing data set {} of " + str(len(data_sets))).format(str(row_index + 1)))
            print ("Data set file: " + str(data_set))

            # Wait for Data set Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Import_DataSet_button)
            self.driver.find_element(*self.Import_DataSet_button).click()
            sleep(3)
            data_set_path = self.driver.find_element(*self.Browse_button)

            if self.driver.name == "MicrosoftEdge":
                subprocess.Popen(['python.exe', self.edge_file_input, "\"" + data_sets_path + "\\" + data_set + "\""])
                self.driver.execute_script("arguments[0].click();", data_set_path)
            else:
                data_set_path.send_keys(data_sets_path+"\\"+data_set)

            # Wait for Upload Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Upload_button)
            upload_button = self.driver.find_element(*self.Upload_button)

            if self.driver.name == "MicrosoftEdge":
                self.driver.execute_script("arguments[0].click();", upload_button)
            else:
                self.driver.find_element(*self.Upload_button).send_keys(Keys.ENTER)

            # Wait for Next Button element to be clickable and Click
            wait = WebDriverWait(self.driver, 30)
            Next = wait.until(EC.element_to_be_clickable(self.Next_button))
            Next.click()

            # Wait for Right Cursor Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Right_Cursor)
            self.driver.find_element(*self.Right_Cursor).click()

            # Wait for Facility Assign  Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Facility_Assign_button)
            self.driver.find_element(*self.Facility_Assign_button).click()

            # Wait for Activate Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Activate_button)
            self.driver.find_element(*self.Activate_button).click()

            # Wait for Confirm Activating Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Confirm_Activate_button)
            self.driver.find_element(*self.Confirm_Activate_button).click()

            # Wait for Ok Button element to be visible and Click
            WebElementWait.wait_for_element(self.driver, self.Confirm_Activate_message)
            self.driver.find_element(*self.Confirm_Activate_message).click()

            # Locate the status  of Activation  Element for every Data set
            print ("Getting data set activation status")
            self.driver.refresh()
            data_sets_status = None

            # Verify that the data set inserted record appears on the UI
            trials = 10
            while trials > 0:
                data_sets_status = self.driver.find_elements(*self.Imported_Datasets_list)
                if len(data_sets_status) < (row_index + 1):
                    sleep(3)
                    self.driver.refresh()
                    trials -= 1
                else:
                    break

            activation_status = data_sets_status[row_index].text

            # verify successful Activation
            assert (activation_status == "Active"), "Not Activated"

            # Locate the Data set name Element
            # Getting data set ID
            imported_dataset_id = self.driver.find_elements(*self.Datasets_IDs)[row_index].text
            print "Data set with ID: {} is activated".format(imported_dataset_id)

        # Deploy DataSets #
            # Start PCU Simulator and Create then Activate
            self.pcusim.start_simulator(number_of_devices, device_version, server_address, server_port, aes_key)
            # Verify that the uploaded Data Set is Deployed successfully for each PCU
            self.pcusim.verify_dataset_deployment(imported_dataset_id)
            # Stop and Close the PCU Simulator
            self.pcusim.stop_simulator()
            self.pcusim.clear_existing_pcus()
            row_index += 1

    # End the test & Close Browser method
    def end_data_set_management_test(self):
        self.driver.close()
