#coding=utf-8
import clr
import os.path
import time
import subprocess


class SmWhiteInstallationLibrary(object):
    # Initializing the SmInstallationLibrary Class
    def __init__(self):
        # Importing TestStack.White Library
        clr.AddReference(os.path.join(os.path.dirname(__file__), 'TestStack.White.dll'))
        from TestStack.White import Application as test_stack_application
        from TestStack.White.UIItems import Button as test_stack_button
        from TestStack.White.UIItems import TextBox as test_stack_text_box
        from TestStack.White.UIItems.ListBoxItems import ComboBox as test_stack_combo_box
        from TestStack.White.UIItems import RadioButton as test_stack_radio_button
        from TestStack.White.AutomationElementSearch import \
            AutomationSearchCondition as test_stack_automation_search_condition
        from TestStack.White.UIItems.Finders import SearchCriteria as test_stack_search_criteria
        from TestStack.White.UIItems.Finders import AutomationElementProperty as test_stack_automation_element_property
        from TestStack.White.Factory import InitializeOption as test_stack_intialize_option
        from TestStack.White.UIItems import Label as test_stack_label
        from System.Windows.Automation import ControlType as ControlType

        # Using the imported libraries as local variables to the class
        self._test_stack_application = test_stack_application
        self._test_stack_button = test_stack_button
        self._test_stack_text_box = test_stack_text_box
        self._test_stack_combo_box = test_stack_combo_box
        self._test_stack_radiobutton = test_stack_radio_button
        self._test_stack_automation_search_condition = test_stack_automation_search_condition
        self._test_stack_search_criteria = test_stack_search_criteria
        self._test_stack_automation_element_property = test_stack_automation_element_property
        self._test_stack_label = test_stack_label
        self._test_stack_initialize_option = test_stack_intialize_option
        self._ControlType = ControlType

        # Defining locators
        self._to_continue_click_next_label_locator = "To continue, click Next."
        self._default_installation_path_locator = "C:\Program Files\CareFusion\Alaris Systems Manager\\"
        self._default_next_button_locator = "Next >"
        self._custom_setup_help_button_locator = "Help"
        self._default_change_button_locator = "Change..."
        self._please_select_certificate_label_locator = "Please select the certificate type:"
        self._certificate_type_carefusion_radiobutton_locator = "[ID:2747]"
        self._default_certificate_path_locator = "C:\Certs\\"
        self._certificate_confirm_button_locator = "Yes"
        self._default_browse_button_locator = "Browse..."
        self._default_username_textbox_locator = "RichEdit20W"
        self._default_password_textbox_locator = "Edit"
        self._default_administrator_textbox_locator = "RichEdit20W"
        self._customer_type_radiobutton_locator = "No"
        self._audit_log_enable_checkbox_locator = "Enable Audit Log Export"
        self._default_user_account_browse_button_locator = "Browse..."
        self._sql_admin_username_textbox_locator = "RichEdit20W"
        self._database_folder_help_button_locator = "Help"
        self._ready_install_button_locator = "Install"
        self._installation_completed_finish_button_locator = "Finish"
        self._db_server_name_combobox_locator = "ComboBox"

        # Defining constants
        self._installer_path = "C:\DropFolder\Release\Alaris Systems Manager v4.33.exe"
        # self._msi_path = os.path.join(os.path.dirname(__file__), "..", "setupfiles", u"Alaris® Systems Manager.msi")
        self._msi_path = os.path.join(self._installer_path, "setupfiles", u"Alaris® Systems Manager.msi")
        #self._default_window_title = "[REGEXPTITLE:(?i)(Alaris.* Systems Manage.*)]"  "Alaris™ Systems Manager  "
        self._default_window_title = "Alaris.* Systems Manager.*"
        self._expected_installation_path = "C:\Program Files\CareFusion\Alaris Systems Manager\\"
        self._expected_carefusion_certificate_path = "C:\Certs\\"
        self._installer_process_name = "Alaris Systems Manager v4.33"

        # Declaring class runtime variables
        self._sut = ""  # Software Under Test
        self._default_window = ""  # SM Installer main window
        self._default_next_button = ""  # The default next button on all installation screens

    def get_the_build_name (self, initial_path):
        build_name = os.listdir(initial_path)[0]
        return build_name

    # Executing the .exe file to start installation
    def start_installation_at(self, installer_path):
        print "Starting the installation: " + installer_path + ". Extracting MSI..."
        msi_folder = os.path.dirname(installer_path) + '\\setupfiles'
        print "MSI Folder is: " + msi_folder
        subprocess.call('"' + installer_path + '"' + ' /s /x /b"' + msi_folder + '" /v" /qn"')
        print "MSI file is successfully extracted."
        self._msi_path = os.path.join(msi_folder, u"Alaris Systems Manager.msi")        #v12
        print "MSI Full path is: " + self._msi_path
        # Launching MSI and getting the default window
        self._sut = self._test_stack_application.Launch(self._msi_path)
        self._default_window = self._sut.GetWindow(self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
                                                   self._test_stack_initialize_option.NoCache)

    # Assertion: Verify that the installer window is opened
    def The_installer_should_open(self):
        if not self._default_window.Exists:
            raise AssertionError("SM Installer failed to start.")
        else:
            print ("SM installer is started successfully.")

    # Pressing "Next" on the first screen - Welcome Screen
    def click_next_on_welcome_screen(self):
        # First, wait for the "To Continue, click Next." label to appear.
        self.wait_till_element_is_visible(self._to_continue_click_next_label_locator, "Label", 60)

        # Then, wait for the "Next" button to be enabled.
        self.wait_till_element_is_enabled(self._default_next_button_locator, "Button", 10)

        # Finally, Click the "Next" button the the Welcome screen.
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Clicking "Next" on the second screen - Custom Setup
    def click_next_on_custom_setup_screen(self):
        # First, wait for the "Help" button on the new window to appear.
        self.wait_till_element_is_visible(self._custom_setup_help_button_locator, "Button", 10)

        # Then, wait for the next button to be active/clickable
        self.wait_till_element_is_enabled(self._default_next_button_locator, "Button", 10)

        # Finally, click the "Next" button on the Custom Setup screen. No changes needed.
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Assertion: Verify that the default installation location is correct
    def Installation_location_should_be_default(self):
        # First, wait for the "Change" button on the new screen to appear
        self.wait_till_element_is_visible\
            (self._test_stack_search_criteria(self._default_change_button_locator), "Button", 10)

        # Verify that the installation location is correct
        default_installation_path = self._default_window.Get[self._test_stack_label]\
            (self._default_installation_path_locator)
        installation_path = default_installation_path.Text
        if installation_path != self._expected_installation_path:
            print("Installation destination is incorrect. Destination is expected to be '%s', but it was '%s'"
                  % (self._expected_installation_path, installation_path))

    # Clicking "Next" on the third screen - Destination Folder
    def click_next_on_destination_folder_screen(self):
        # First, wait for the "Next" button is enabled
        self.wait_till_element_is_enabled(self._default_next_button_locator, "Button", 10)

        # Click the "Next" button on the Destination Folder screen. No changes needed.
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Selecting CareFusion Certificates and clicking "Next" on the fourth screen - Certificate Type
    def click_next_on_certificate_type_screen(self):
        # First, wait for the "Please select the certificate type:" label to appear
        self.wait_till_element_is_visible(self._please_select_certificate_label_locator, "Label", 10)

        # Then, wait for the next button to be active/clickable
        self.wait_till_element_is_enabled(self._default_next_button_locator, "Button", 10)

        # Then, click the "Next" button on the Certificate Type screen. No changes needed.
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Verify that the default CareFusion Certificate location is correct
    def CareFusion_certificate_location_should_be_default(self):
        # First, wait for the "Change" button on the new screen to appear
        self.wait_till_element_is_visible(self._default_change_button_locator, "Button", 10)

        # Verify that the specified location for CareFusion Certificate is correct
        carefusion_certificate_path = self._default_window.Get[self._test_stack_label]\
            (self._default_certificate_path_locator).Text
        if carefusion_certificate_path != self._expected_carefusion_certificate_path:
            print("Certificate Folder is incorrect. The path is expected to be '%s', but it was '%s'"
                  % (self._expected_carefusion_certificate_path,  carefusion_certificate_path))

    # Clicking "Next" on the fifth screen - Certificate Folder
    def click_next_on_certificate_folder_screen(self):
        # Then, click the "Next" button on the Certificate Folder screen. No changes needed.
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    def click_yes_on_confirm_certificate_screen(self):
        yes_button = self._default_window.Get[self._test_stack_button](self._certificate_confirm_button_locator)
        yes_button.Click()

    # Enter DB Server on sixth screen - Database Server: Default is (local), can be overridden in cmd.
    def select_db_server(self, server_name):
        # First, wait for the "browse" button on the new screen to appear
        self.wait_till_element_is_visible(self._default_browse_button_locator, "Button", 10)

        # Then, wait for 10 more seconds, to make sure that Server Information are successfully retrieved.
        time.sleep(10)

        # After that, enter the server name in the Server Name Combobox
        server_name_combobox = self._default_window.Get[self._test_stack_combo_box] \
            (self._test_stack_search_criteria.ByClassName(self._db_server_name_combobox_locator))
        server_name_combobox.Focus()

        server_name_combobox.EnterData(server_name)

        # Finally, click the "Next" button on the Database Server screen.
        time.sleep(2)
        self._default_next_button = self._default_window.Get[self._test_stack_button](
            self._default_next_button_locator)
        self._default_next_button.Click()

    # Clicking "Next" on the sixth screen - Database Server
    def click_next_on_database_server_screen(self):
        # First, wait for the "browse" button on the new screen to appear
        self.wait_till_element_is_visible(self._default_browse_button_locator, "Button", 10)

        # Then, wait for 10 more seconds, to make sure that Server Information are successfully retrieved.
        time.sleep(10)

        # Finally, click the "Next" button on the Database Server screen. No changes needed.
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Entering the current Domain User and Password on the seventh screen - Authentication Service
    def enter_domain_user_and_password_on_authentication_service_screen(self, username, password):
        # First, wait for the "Username" textbox on the new screen to appear
        time.sleep(5)
        self.wait_till_element_is_visible\
            (self._test_stack_search_criteria.ByClassName(self._default_username_textbox_locator),"Text Box", 10)

        # Then, enter the username supplied by the test case
        username_textbox = self._default_window.Get[self._test_stack_text_box]\
            (self._test_stack_search_criteria.ByClassName(self._default_username_textbox_locator))
        username_textbox.Focus()
        username_textbox.EnterData(username)

        # After that, enter the password supplied by the test case
        password_textbox = self._default_window.Get[self._test_stack_text_box] \
            (self._test_stack_search_criteria.ByClassName(self._default_password_textbox_locator))
        password_textbox.Focus()
        password_textbox.EnterData(password)

        # Then, wait for 3 seconds, till the entry of the username and password is completed.
        time.sleep(3)

        # Finally, click "Next" button on the Authentication Service screen
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()
        time.sleep(5)

    # Assertion: Verify that the Administrator Account is supplied correctly to the Administrator Account screen
    def administrator_account_should_be(self, expected_admin_account):
        # First, wait for the "Administrator Account" textbox to appear on the new screen
        time.sleep (3)
        self.wait_till_element_is_visible\
            (self._test_stack_search_criteria.ByClassName(self._default_administrator_textbox_locator), "Text Box", 10)

        # Verify that the Administrator Account is correct
        admin_account = self._default_window.Get[self._test_stack_text_box]\
            (self._test_stack_search_criteria.ByClassName(self._default_administrator_textbox_locator)).Text
        if admin_account != expected_admin_account:
            raise AssertionError("Administrator Account is incorrect. It is expected to be '%s', but it was '%s'"
                                 % (expected_admin_account, admin_account))

    # Clicking "Next" on the eighth screen - Administrator Account
    def click_next_on_administrator_account_screen(self):
        # Click "Next" button on the Administrator Account screen. No changes required
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Clicking "Next" on the ninth screen - Customer Type
    def click_next_on_customer_type_screen(self):
        # First, wait for the "Customer Type" radiobutton to appear on the new screen
        self.wait_till_element_is_visible(self._customer_type_radiobutton_locator, "RadioButton", 10)

        # Then, click "Next" button on the Customer Type screen. No changes required
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Checking "Enable Audit Log" on the tenth screen - Audit log
    def check_audit_log_on_audit_log_screen(self):
        # First, wait for the "Enable Audit log Export" Checkbox to appear on the new screen
        self.wait_till_element_is_visible(self._audit_log_enable_checkbox_locator, "Button", 10)

        # Then, check the "Enable Audit Log Export" checkbox.
        self._default_window.Get[self._test_stack_button](self._audit_log_enable_checkbox_locator).Click()

        # Finally, click "Next" button on the Audit Log screen
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Entering the Current Domain User on the eleventh screen - SQL Administrator
    def enter_domain_user_on_sql_administrator_screen(self, username):
        # First, wait for the User Account "Browse" button to appear on the new screen
        self.wait_till_element_is_visible(self._default_user_account_browse_button_locator, "Button", 10)

        # Then, enter the username supplied by the test case
        self._default_window = self._sut.GetWindow(
            self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
            self._test_stack_initialize_option.NoCache)
        username_textbox = self._default_window.Get[self._test_stack_text_box] \
            (self._test_stack_search_criteria.ByClassName(self._sql_admin_username_textbox_locator))
        username_textbox.Focus()
        username_textbox.EnterData(username)

        # After that, wait for 3 seconds till user account entery is completed
        time.sleep(3)

        # Finally, click "Next" button on the SQL Administrator screen
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Clicking "Next" on the twelfth screen - Database Folder
    def click_next_on_database_folder_screen(self):
        # First, wait for the "Help" button to appear on the new screen
        self.wait_till_element_is_visible(self._database_folder_help_button_locator, "Button", 10)

        # Then, click "Next" button on the Database Folder screen. No changes required
        self._default_next_button = self._default_window.Get[self._test_stack_button](self._default_next_button_locator)
        self._default_next_button.Click()

    # Clicking "Install" to start the installation on the thirteenth screen - Reay to Install
    def click_install_on_ready_screen(self):
        # First, wait for the "Install" button to appear on the new screen
        self.wait_till_element_is_visible(self._ready_install_button_locator, "Button", 10)

        # Then, click "Install" button on the Ready to Install screen.
        self._default_window = self._sut.GetWindow(
            self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
            self._test_stack_initialize_option.NoCache)
        self._default_window.Get[self._test_stack_button](self._ready_install_button_locator).Click()

    # Clicking "Finish" to Finish the installation the the fourteenth screen - Installation Completed
    def click_finish_on_installation_completed_screen(self):
        # First wait for the "Finish" button to appear on the new screen
        self.wait_till_element_is_visible(self._installation_completed_finish_button_locator, "Button", 120)

        # Then, Click "Finish" button on the Installation Completed screen to exit the installer
        self._default_window = self._sut.GetWindow(
            self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
            self._test_stack_initialize_option.NoCache)
        self._default_window.Get[self._test_stack_button](self._installation_completed_finish_button_locator).Click()

    # Verify that the Installer window is closed after the installation is completed
    def The_installer_should_close(self):
        # First, wait for 10 seconds for the window to close
        time.sleep(10)

        # Verify that the installer window is no longer open
        try:
            self._default_window = self._sut.GetWindow(
                self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
                self._test_stack_initialize_option.NoCache)
            if self._default_window.Exists:
                raise AssertionError("An error prevented the installer window from closing.\n Please verify that the installation is completed successfully.")
        except:
            pass

    # Helper Methods.
    # Waiting for an element to be ready (enabled), before attempting to interact with it
    def wait_till_element_is_enabled(self, element_locator, element_type, timeout):
        # Initially, the timeout counter starts at 0 and the default element status is disabled.
        counter = 0
        enabled = False

        # Loop until either the element is enabled, or timeout occurs
        while not enabled and counter < timeout:
            print ("Is element '%s' of type '%s' enabled?... Iteration number: "
                   %(str(element_locator), element_type)) + str(counter)

            # First, search for the specified element, to put it in a passable variable.
            element = self.search_for_element(element_locator, element_type)

            # Then, if the element exists, try to determine whether or not it's enabled.
            try:
                # If element is enabled, set the status to true to exit the While Loop
                enabled = element.Enabled
            except:
                # If element is not enabled, do not fail the TC. Continue till element is found or timeout occurs
                pass
            time.sleep(1)
            counter += 1

        # At this point, either the element is found, or timeout occurred.
        if not enabled:
            # If the element is not found and enabled, fail the TC and raise an error.
            raise AssertionError("Timeout error. The element " + str(element_locator) +
                                 " was not enabled or couldn't be found for " + str(timeout) + " seconds.")
        elif enabled:
            # If the element is enabled, return to the original context to continue execution.
            print "Element " + str(element_locator) + " is now enabled!"
            return

    # Waiting for an element to be ready (visible), before attempting to interact with it
    def wait_till_element_is_visible(self, element_locator, element_type, timeout):
        # Initially, the timeout counter starts at 0 and the default element status is disabled.
        counter = 0
        visible = False

        # Loop until either the element is visible, or timeout occurs
        while not visible and counter < timeout:
            print ("Is element '%s' of type '%s' visible?... Iteration number: "
                   %(str(element_locator), element_type)) + str(counter)

            # First, search for the specified element, to put it in a passable variable.
            element = self.search_for_element(element_locator, element_type)

            # Then, if the element exists, try to determine whether or not it's visible.
            try:
                visible = element.Visible
            except:
                pass

            time.sleep(1)
            counter += 1

        # At this point, either the element is found, or timeout occurred.
        if not visible:
            # If the element is not found and visible, fail the TC and raise an error.
            raise AssertionError("Timeout error. The element " + str(element_locator) +
                                 " was not visible for " + str(timeout) + " seconds.")

        elif visible:
            # If the element is visible, return to the original context to continue execution.
            print "Element " + str(element_locator) + " is now visible!"
            return

    # This method is used to determine if a certain element exists. Once it is found, the method returns it
    # If the element is not found, log the status and return an empty string.
    def search_for_element(self, element_locator, element_type):
        element = ''

        # Try to find an element using to its type and locator:
        try:
            if element_type == "Label":
                self._default_window = self._sut.GetWindow(
                    self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
                    self._test_stack_initialize_option.NoCache)
                element = self._default_window.Get[self._test_stack_label](element_locator)
            elif element_type == "Button":
                self._default_window = self._sut.GetWindow(
                    self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
                    self._test_stack_initialize_option.NoCache)
                element = self._default_window.Get[self._test_stack_button](element_locator)
            elif element_type == "Text Box":
                self._default_window = self._sut.GetWindow(
                    self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
                    self._test_stack_initialize_option.NoCache)
                element = self._default_window.Get[self._test_stack_text_box](element_locator)
            elif element_type == "RadioButton":
                self._default_window = self._sut.GetWindow(
                    self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
                    self._test_stack_initialize_option.NoCache)
                element = self._default_window.Get[self._test_stack_radiobutton](element_locator)

        except:
            # If the element is not found, log the status and continue.
            print ("Element '%s' of type '%s' cannot be found yet. Retrying..." % (str(element_locator), element_type))
            pass

        # Return the element if found. If not, return an empty string.
        return element
