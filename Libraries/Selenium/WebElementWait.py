from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, TimeoutException, StaleElementReferenceException
from time import sleep


class WebElementWait(object):

    @staticmethod
    def wait_for_element(web_driver, locator, trials=6, interval=10):

        sleep(2)
        found = False
        displayed = False

        while trials != 0 and (not found or not displayed):
            try:
                element = web_driver.find_element(*locator)
                found = True
                if element.is_displayed():
                    displayed = True
            except (ElementNotVisibleException, NoSuchElementException, StaleElementReferenceException) as e:
                print ("Element not visible yet ...")

            trials -= 1
            if not found or not displayed:
                sleep(interval)

        if not found or not displayed:
            raise TimeoutException("Element with locator: (" + str(locator) + "), in the URL: (" + web_driver.current_url + ") is not found.")
