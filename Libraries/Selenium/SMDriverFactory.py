from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os
from time import sleep
from BrowserAutoIt import BrowserAutoIt


class driver_factory(object):
    @staticmethod
    def getDriver(browser, ip, username, password):
        exec_path = os.path.join(os.path.dirname(__file__), "..", "..", "Tools")
        print "Starting {} browser session ...".format(browser)
        if browser == "Chrome":
            driver = webdriver.Chrome(executable_path=exec_path + "/chromedriver.exe")
            driver.get("https://" + username + ":" + password + "@" + ip + "/SystemsManager/")
            driver.get("https://" + ip + "/SystemsManager/")

        elif browser == "IE":
            driver = webdriver.Ie(executable_path=exec_path + "/IEDriverServer.exe")
            driver.get("https://" + ip + "/SystemsManager/")
            if driver.title.__contains__("Certificate"):
                driver.execute_script("document.getElementById('overridelink').click()")
            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                driver.switch_to.alert.authenticate(username, password)
            except TimeoutException:
                print "Alert authentication timed out .. using AutoIt to Login"
                BrowserAutoIt.login("Windows Security", username, password)

        elif browser == "Edge":
            driver = webdriver.Edge(executable_path=exec_path + "/MicrosoftWebDriver.exe")
            driver.get("https://" + ip + "/SystemsManager/")
            if driver.title.__contains__("Certificate"):
                # driver.find_element_by_id("continueLink").click()
                driver.execute_script("document.getElementById('continueLink').click()")
            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                driver.switch_to.alert.authenticate(username, password)
            except TimeoutException:
                print "Alert authentication timed out .. using AutoIt to Login"
                BrowserAutoIt.login("Windows Security", username, password)

        sleep(5)
        driver.implicitly_wait(30)
        driver.maximize_window()
        driver.refresh()

        if ("https://{}/SystemsManager".format(ip)) not in driver.current_url:
            driver.get("https://{}/SystemsManager".format(ip))
            assert(("https://{}/SystemsManager".format(ip)) in driver.current_url), "Cannot Navigate to SM Home URL"

        return driver
