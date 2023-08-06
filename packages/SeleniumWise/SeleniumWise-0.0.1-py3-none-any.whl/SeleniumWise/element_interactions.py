"""
The Module is a part of the SeleniumWise package.
"""
import logging
from typing import List

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ElementOperations:
    """
    The following methods are for the WebElement class
    """

    def __init__(self, driver):
        self.driver = driver

    def get_element(self, *by) -> WebElement:
        """
        Get element by locator
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        :return: WebElement

        """
        try:
            return self.driver.find_element(*by)
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def get_elements(self, *by) -> WebElement:
        """
        Get elements by locator
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        :return: WebElement

        """
        try:
            return self.driver.find_elements(*by)
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def click_element(self, *by) -> None:
        """
        Click on element
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        :return: None

        """
        try:
            self.get_element(*by).click()
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for element to be visible
        :param timeout:
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        :return: WebElement
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_elements(self, *by, timeout: int = 10) -> List[WebElement]:
        """
        Wait for elements to be visible
        :param timeout:
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_clickable(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for element to be clickable
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_invisible(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for element to be invisible
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_selected(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for element to be selected
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_selected(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_not_selected(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for element to be not selected
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_located_to_be_selected(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_present(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for element to be present
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_elements_to_be_present(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for elements to be present
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_stale(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for element to be stale
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(EC.staleness_of(*by))
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_text_present(
        self, *by, text: str, timeout: int = 10
    ) -> WebElement:
        """
        Wait for element to be text present
        :param timeout: maximum time to wait
        :param by: locator
        :param text: text to wait for
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(*by, text)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_text_present_in_value(
        self, *by, text: str, timeout: int = 10
    ) -> WebElement:
        """
        Wait for element to be text present in value
        :param timeout: maximum time to wait
        :param by: locator
        :param text: text to wait for
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element_value(*by, text)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_alert_present(self, timeout: int = 10) -> WebElement:
        """
        Wait for element to be alert present
        :param timeout: maximum time to wait
        """
        try:
            return WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_frame_available_and_switch_to_it(
        self, *by, timeout: int = 10
    ) -> WebElement:
        """
        Wait for element to be frame available and switch to it
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_frame_available_and_switch_to_it_by_index(
        self, index: int, timeout: int = 10
    ) -> WebElement:
        """
        Wait for element to be frame available and switch to it by index
        :param timeout: maximum time to wait
        :param index: index of frame
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(index)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_frame_available_and_switch_to_it_by_webElement(
        self, element: WebElement, timeout: int = 10
    ) -> WebElement:
        """
        Wait for element to be frame available and switch to it by webelement
        :param timeout: maximum time to wait
        :param element: webelement of frame
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(element)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_invisibility(self, *by, timeout: int = 10) -> WebElement:
        """
        Wait for element to be invisibility
        :param timeout: maximum time to wait
        :param by: locator
        :Example: LOCATOR = (By.ID, 'id')
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(*by)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def wait_for_element_to_be_invisibility_by_webElement(
        self, element: WebElement, timeout: int = 10
    ) -> WebElement:
        """
        Wait for element to be invisibility by webelement
        :param timeout: maximum time to wait
        :param element: webelement
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element(element)
            )
        except Exception as error:
            logging.error(f"Operation Failed: {error}")
