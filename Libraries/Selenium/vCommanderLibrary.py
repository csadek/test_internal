import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from WebElementWait import WebElementWait


class vCommanderLibrary(object):
    def __init__(self):
        # Locators for Login Page
        self.Username = (By.ID, "username")
        self.Password = (By.ID, "password")
        self.LoginButton = (By.ID, "login-button")

        # Locators for Home page
        self.message_ok = (By.ID, "motd:ok")
        self.all_vms = (By.XPATH, ".//*[@id='tree:PORTAL_FOLDER--1001']/div[2]/div")
        self.target_vm = (By.XPATH, ".//div[1]/label/span")
        self.view_snapshots = (By.LINK_TEXT, "View Snapshots")
        self.snapshot_tree = (By.ID, "vm_snapshots:_idJsp4")
        self.go_to_snapshot = (By.XPATH, ".//*[@id='vm_snapshots:_idJsp29']/table/tbody/tr/td/div/div[2]")
        self.confirm_button = (By.ID, "revert-snapshot:revert")
        self.close_snapshots = (By.ID, "vm_snapshots:_idJsp35")
        self.task_status = (By.ID, "task-pane:thegrid_0:recentTaskBacking-text-130")
        self.start_vm = (By.LINK_TEXT, "Start VM")

    def Open_Browser_To_Login_Page(self, browser, url):
        # Initiate driver and navigate to vCommander home page
        exec_path = os.path.join(os.path.dirname(__file__), "..", "..", "Tools")
        if browser == "Chrome":
            self.driver = webdriver.Chrome(executable_path=exec_path+"/chromedriver.exe")
            self.driver.get(url)
        elif browser == "IE":
            self.driver = webdriver.Ie(executable_path=exec_path+"/IEDriverServer.exe")
            self.driver.get(url)
            if self.driver.title.__contains__("Certificate"):
                self.driver.execute_script("document.getElementById('overridelink').click()")
        # self.driver.maximize_window()
        self.driver.implicitly_wait(30)

    def Login_To_vCommander(self, username, password):
        # Enter username & password then click Login
        WebElementWait.wait_for_element(self.driver, self.Username)
        self.driver.find_element(*self.Username).send_keys(username)
        self.driver.find_element(*self.Password).send_keys(password)
        self.driver.find_element(*self.LoginButton).click()
        # Confirm message of the day
        WebElementWait.wait_for_element(self.driver, self.message_ok)
        self.driver.find_element(*self.message_ok).click()

    def Select_VM(self, vm_name):
        WebElementWait.wait_for_element(self.driver, self.all_vms)
        vm_list = self.driver.find_elements(*self.all_vms)
        for vm in vm_list:
            selected_vm = vm.find_element(*self.target_vm)
            if vm_name == selected_vm.text:
                selected_vm.click()
                return
        raise Exception("VM {} Not Found !".format(vm_name))

    def wait_for_task(self, task, trials=12, interval=10):
        completed = False
        WebElementWait.wait_for_element(self.driver, self.task_status)
        while trials != 0 and not completed:
            status = self.driver.find_element(*self.task_status).get_attribute("innerHTML")
            if status == "Completed":
                return
            else:
                sleep(interval)

        raise Exception("VM " + task + " task took longer than expected !")

    def Revert_And_Start_Selected_VM(self, snapshot_name):
        # Open snapshots window
        WebElementWait.wait_for_element(self.driver, self.view_snapshots)
        self.driver.find_element(*self.view_snapshots).click()
        # Select snapshot
        WebElementWait.wait_for_element(self.driver, self.snapshot_tree)
        snapshot_list = self.driver.find_element(*self.snapshot_tree)
        snapshots = snapshot_list.find_elements(By.TAG_NAME, "span")
        found = False
        for snapshot in snapshots:
            if snapshot.text == snapshot_name:
                found = True
                snapshot.click()
                break

        if not found:
            raise Exception("Snapshots with name '{}' not found".format(snapshot_name))
        # Click on Go To button
        WebElementWait.wait_for_element(self.driver, self.go_to_snapshot)
        self.driver.find_element(*self.go_to_snapshot).click()
        # Confirm VM revert
        WebElementWait.wait_for_element(self.driver, self.confirm_button)
        self.driver.find_element(*self.confirm_button).click()
        WebElementWait.wait_for_element(self.driver, self.close_snapshots)
        self.driver.find_element(*self.close_snapshots).click()
        self.wait_for_task("Revert")
        # Start VM
        WebElementWait.wait_for_element(self.driver, self.start_vm)
        self.driver.find_element(*self.start_vm).click()
        self.wait_for_task("Start")

    def Close_The_Browser(self):
        self.driver.close()
