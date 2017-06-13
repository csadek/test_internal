#coding=utf-8
import clr
import os.path
import time

class PCIWhiteInstallationLibrary(object):
    # Initializing the PCIInstallationLibrary Class
    def __init__(self):

        # Importing TestStack.White Library
        clr.AddReference(os.path.join(os.path.dirname(__file__), 'TestStack.White.dll'))
        from TestStack.White import Application as test_stack_application
        from TestStack.White.UIItems import Button as test_stack_button
        from TestStack.White.UIItems.ListBoxItems import ListItem as test_stack_list
        from TestStack.White.Factory import InitializeOption as test_stack_intialize_option
        from System.Windows.Automation import ControlType as ControlType
        from TestStack.White.UIItems.Finders import SearchCriteria


        # Using the imported libraries as local variables to the class
        self._test_stack_application = test_stack_application
        self._test_stack_button = test_stack_button
        self._test_stack_search_criteria = SearchCriteria
        self._test_stack_list = test_stack_list
        self._test_stack_initialize_option = test_stack_intialize_option
        self._ControlType = ControlType


        # Defining locators
        self._Install_button_locator = "Install"
        self._OK_button_locator = "OK"
        self._net_framework = ".Net Framework 4.6.2  (Installed)"

        # Declaring class runtime variables
        self._sut = ""  # Software Under Test
        self._default_window = ""  # SM Installer main window
        self._Install_button = ""
        self._OK_button = ""

    def get_the_build_name (self, initial_path):
        build_name = os.listdir(initial_path)[0]
        return build_name

    # Executing the .exe file to start installation
    def start_installation_at(self, installer_path):
        print "Starting the installation: " + installer_path
        # Launching exe and getting the default window
        self._sut = self._test_stack_application.Launch(installer_path)
        self._default_window = self._sut.GetWindow(self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
                                                   self._test_stack_initialize_option.NoCache)

     # Assertion: Verify that the installer window is opened
    def The_installer_should_open(self):
        if not self._default_window.Exists:
            raise AssertionError("ASM PCI Installer failed to start.")
        else:
            print ("ASM PCI is started successfully.")


    # Assertion: Verify that the .NET framework is installed
    def Ensure_the_net_framework_is_installed(self):
        # Verify that the .NET framework is exist with text "Installed"
        print ("Verify The installation of .Net framework .... \
                             If the Element doesn't exist it may means that the .Net framework isn't installed  ")
        self.wait_till_element_is_visible(self._net_framework, "List", 60)


    def click_Install_on_main_screen(self):
         # First, wait for the "Install" button to appear.
        self.wait_till_element_is_visible(self._Install_button_locator, "Button", 60)

        # Then, wait for the "Install" button to be enabled.
        self.wait_till_element_is_enabled(self._Install_button_locator, "Button", 10)

        # Finally, Click the "Install" button the the Main screen.
        self._Install_button = self._default_window.Get[self._test_stack_button](self._Install_button_locator)
        self._Install_button.Click()

    def click_Ok_on_completion_screen(self):
          # First, wait for the "OK" button to appear.
        self.wait_till_element_is_visible(self._OK_button_locator, "Button", 180)

        # Then, wait for the "OK" button to be enabled.
        self.wait_till_element_is_enabled(self._OK_button_locator, "Button", 10)

        # Finally, Click the "OK" button the the Completion screen.
        self._OK_button = self._default_window.Get[self._test_stack_button](self._OK_button_locator)
        self._OK_button.Click()


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
            elif element_type == "List":
                self._default_window = self._sut.GetWindow(
                    self._test_stack_search_criteria.ByControlType(self._ControlType.Window),
                     self._test_stack_initialize_option.NoCache)
                element = self._default_window.Get[self._test_stack_list](element_locator)

        except:
            # If the element is not found, log the status and continue.
            print ("Element '%s' of type '%s' cannot be found yet. Retrying..." % (str(element_locator), element_type))
            pass

        # Return the element if found. If not, return an empty string.
        return element
