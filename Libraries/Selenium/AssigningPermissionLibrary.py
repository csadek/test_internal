import traceback
from time import sleep
from pyad import *
from pyad.adcontainer import ADContainer
from pyad.aduser import ADUser
from TestExceptionHandler import driverhandler
from SMDriverFactory import driver_factory
from selenium.webdriver.common.by import By
from WebElementWait import WebElementWait
from robot.api import logger


class AssigningPermissionLibrary(object):

    def __init__(self):
        # Import User Locators
        self.Import_Users_button = (By.LINK_TEXT, "Import Users")
        self.Search_button = (By.ID, "search-users")
        self.Uncheck_all = (By.ID, "check-all")
        self.UsersIds_list = (By.XPATH, ".//*[@id='userimport-tablecontainer']/tbody/tr")
        self.UserId = (By.XPATH, ".//td[5]")
        self.New_User = (By.XPATH, ".//td[1]/input")
        self.New_User_Id = (By.XPATH, ".//td[4]")
        self.Next_button = (By.ID, "continue-user-permission")
        self.Facility_User_option = (By.ID, "idFacility")
        self.Manage_Dataset_permission = (By.ID, "Permissions_Facilities_0__Permissions_1__IsGranted")
        self.Manage_Users_permission = (By.ID, "Permissions_Facilities_0__Permissions_2__IsGranted")
        self.Import_button = (By.ID, "btnSubmitEditPermissions")
        self.Imported_Users = (By.XPATH, ".//*[@id='usersTableContainer']/tbody/tr" )
        self.User_Permission = (By.XPATH, ".//td[5]/a")
        self.Save_button = (By.ID, "btnSubmitEditPermissions")

    # Create User in Active directory
    def create_user_in_active_directory(self, server_name, domain_name, domain_password, domain_controller, new_user_name, new_user_passowrd):
        try:
            pyad.set_defaults(ldap_server=server_name, username=domain_name, password=domain_password)
            ou = ADContainer.from_dn("CN=Users, dc="+domain_controller+", dc=local")
            ADUser.create(new_user_name, ou, password=new_user_passowrd)
            print("User {} added successfully to Active Directory".format(new_user_name))
        except:
            print traceback.print_exc()
            raise Exception("User {} is not added successfully to Active Directory".format(new_user_name))

    # Open SM and navigate to Manage Users page
    @driverhandler
    def open_browser_and_login_then_navigate_to_manage_users_page(self, browser, ip, username, password):
        self.driver = driver_factory.getDriver(browser, ip, username, password)
        sleep(5)

        # Navigate to Manage Users page
        logger.console("| Navigating to: " + self.driver.current_url + "MVC/User/ManageUsers")
        self.driver.get(self.driver.current_url + "MVC/User/ManageUsers")

    # Import user from Available users in SM
    @driverhandler
    def import_user(self, User_ID):
        # Find Import users button and click
        WebElementWait.wait_for_element(self.driver, self.Import_Users_button)
        self.driver.find_element(*self.Import_Users_button).click()

        # Find Search users button and click
        WebElementWait.wait_for_element(self.driver, self.Search_button)
        self.driver.find_element(*self.Search_button).click()

        # Find Check All checkbox and click to uncheck
        WebElementWait.wait_for_element(self.driver, self.Uncheck_all)
        self.driver.find_element(*self.Uncheck_all).click()

        # Create list for the available users and loop to select the new user
        Available_Users_List = self.driver.find_elements(*self.UsersIds_list)
        user_found = False
        for user in Available_Users_List:
            userid = user.find_element(*self.UserId).text
            if userid == User_ID:
                user_found = True
                checkuser = user.find_element(*self.New_User)
                checkuser.click()
                break

        if not user_found:
            raise Exception('Cannot find user with ID: {} in users list'.format(User_ID))

        # Find Next button and click
        WebElementWait.wait_for_element(self.driver, self.Next_button)
        self.driver.find_element(*self.Next_button).click()

        # Find Facility user option and click
        sleep(5)
        self.driver.find_element(*self.Facility_User_option).click()

        # Find dataset permission and click
        WebElementWait.wait_for_element(self.driver, self.Manage_Dataset_permission)
        self.driver.find_element(*self.Manage_Dataset_permission).click()

        # Find Import button and click
        WebElementWait.wait_for_element(self.driver, self.Import_button)
        self.driver.find_element(*self.Import_button).click()
        sleep(3)

        # Create list for users to confirm importing
        Users_List = self.driver.find_elements(*self.Imported_Users)
        user_found = False
        for user in Users_List:
            user_id = user.find_element(*self.New_User_Id).text
            if user_id == User_ID:
                user_found = True
                print("User imported successfully")
                break

        if not user_found:
            raise Exception('Cannot find user with ID: {} in users list'.format(User_ID))

    # Remove dataset management permission for facility user
    @driverhandler
    def remove_permission(self, UserID):
        user_found = False
        Users_List = self.driver.find_elements(*self.Imported_Users)
        for user in Users_List:
            user_id = user.find_element(*self.New_User_Id).text
            if user_id == UserID:
                user_found = True
                Permissions = user.find_element(*self.User_Permission)
                Permissions.click()
                break

        if not user_found:
            raise Exception('Cannot find user with ID: {} in users list'.format(UserID))

        # Find dataset permission and uncheck
        WebElementWait.wait_for_element(self.driver, self.Manage_Dataset_permission)
        self.driver.find_element(*self.Manage_Dataset_permission).click()

        # Assign another permission to save changes
        WebElementWait.wait_for_element(self.driver, self.Manage_Users_permission)
        self.driver.find_element(*self.Manage_Users_permission).click()

        # Find save button anc click
        WebElementWait.wait_for_element(self.driver, self.Save_button)
        self.driver.find_element(*self.Save_button).click()

    # Close Browser
    def close_web_browser(self):
        self.driver.close()

    # End the assign permission test method
    def end_assign_permission_test(self):
        self.driver.close()












