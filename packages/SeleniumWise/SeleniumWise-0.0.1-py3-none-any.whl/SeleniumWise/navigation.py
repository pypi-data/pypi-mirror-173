"""
Module inherits the SeleniumWise class and adds navigation methods.
"""

import logging

from selenium.webdriver.remote.webelement import WebElement


class Navigation:
    """
    The following methods are not part of the SeleniumWise class
    """

    def __init__(self, driver):
        self.driver = driver

    def back(self):
        """
        Navigate back to the previous page
        :return:
        """
        self.driver.back()

    def forward(self):
        """
        Navigate forward to the next page
        :return:
        """
        self.driver.forward()

    def refresh(self):
        """
        Refresh the current page
        :return:
        """
        self.driver.refresh()

    def navigate(self, url):
        """
        Navigate to the specified URL
        :param url:
        :return:
        """
        self.driver.get(url)

    def close(self):
        """
        Close the current window
        :return:
        """
        self.driver.close()

    def quit(self):
        """
        Close the current window and quit the driver
        :return:
        """
        self.driver.quit()

    def maximize(self):
        """
        Maximize the current window
        :return:
        """
        self.driver.maximize_window()

    def minimize(self):
        """
        Minimize the current window
        :return:
        """
        self.driver.minimize_window()

    def fullscreen(self):
        """
        Fullscreen the current window
        :return:
        """
        self.driver.fullscreen_window()

    def get_title(self):
        """
        Get the title of the current page
        :return:
        """
        return self.driver.title

    def get_url(self):
        """
        Get the current URL
        :return:
        """
        return self.driver.current_url

    def get_page_source(self):
        """
        Get the page source
        :return:
        """
        return self.driver.page_source

    def get_window_size(self):
        """
        Get the current window size
        :return:
        """
        return self.driver.get_window_size()

    def get_window_position(self):
        """
        Get the current window position
        :return:
        """
        return self.driver.get_window_position()

    def set_window_size(self, width, height):
        """
        Set the window size
        :param width:
        :param height:
        :return:
        """
        self.driver.set_window_size(width, height)

    def set_window_position(self, x, y):
        """
        Set the window position
        :param x:
        :param y:
        :return:
        """
        self.driver.set_window_position(x, y)

    def set_window(self, width, height, x, y):
        """
        Set the window size and position
        :param width:
        :param height:
        :param x:
        :param y:
        :return:
        """
        self.driver.set_window_size(width, height)
        self.driver.set_window_position(x, y)

    def get_screenshot_as_file(self, filename):
        """
        Get a screenshot of the current window
        :param filename:
        :return:
        """
        self.driver.get_screenshot_as_file(filename)

    def get_screenshot_as_base64(self):
        """
        Get a screenshot of the current window
        :return:
        """
        return self.driver.get_screenshot_as_base64()

    def get_screenshot_as_png(self):
        """
        Get a screenshot of the current window
        :return:
        """
        return self.driver.get_screenshot_as_png()

    def get_cookies(self):
        """
        Get all cookies
        :return:
        """
        return self.driver.get_cookies()

    def get_cookie(self, name):
        """
        Get a cookie by name
        :param name:
        :return:
        """
        return self.driver.get_cookie(name)

    def add_cookie(self, cookie_dict):
        """
        Add a cookie
        :param cookie_dict:
        :return:
        """
        self.driver.add_cookie(cookie_dict)

    def delete_cookie(self, name):
        """
        Delete a cookie by name
        :param name:
        :return:
        """
        self.driver.delete_cookie(name)

    def delete_all_cookies(self):
        """
        Delete all cookies
        :return:
        """
        self.driver.delete_all_cookies()

    def switch_to_frame(self, frame_reference):
        """
        Switch to the specified frame
        :param frame_reference:
        :return:
        """
        self.driver.switch_to.frame(frame_reference)

    def switch_to_default_content(self):
        """
        Switch to the default content
        :return:
        """
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_name):
        """
        Switch to the specified window
        :param window_name:
        :return:
        """
        self.driver.switch_to.window(window_name)

    def switch_to_alert(self):
        """
        Switch to the alert
        :return:
        """
        return self.driver.switch_to.alert

    def switch_to_active_element(self):
        """
        Switch to the active element
        :return:
        """
        return self.driver.switch_to.active_element

    def switch_to_parent_frame(self):
        """
        Switch to the parent frame
        :return:
        """
        return self.driver.switch_to.parent_frame

    def scroll_to_element(self, element: WebElement):
        """
        Scroll to the specified element
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_click(self, element: WebElement):
        """
        Scroll to the specified element and click
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_send_keys(self, element: WebElement, keys):
        """
        Scroll to the specified element and send keys
        :param element:
        :param keys:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            element.send_keys(keys)
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_clear(self, element: WebElement):
        """
        Scroll to the specified element and clear
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            element.clear()
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_attribute(
        self, element: WebElement, attribute: str
    ) -> str:
        """
        Scroll to the specified element and get attribute
        :param element:
        :param attribute:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.get_attribute(attribute)
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_property(
        self, element: WebElement, property: str
    ) -> str:
        """
        Scroll to the specified element and get property
        :param element:
        :param property:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.get_property(property)
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_css_value(
        self, element: WebElement, css_property: str
    ) -> str:
        """
        Scroll to the specified element and get css value
        :param element:
        :param css_property:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.value_of_css_property(css_property)
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_text(self, element: WebElement) -> str:
        """
        Scroll to the specified element and get text
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.text
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_horizontally(self, x):
        """
        Scroll horizontally
        :param x:
        :return:
        """
        try:
            self.driver.execute_script(f"window.scrollTo({x}, 0)")
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_vertically(self, y):
        """
        Scroll vertically
        :param y:
        :return:
        """
        try:
            self.driver.execute_script(f"window.scrollTo(0, {y})")
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_location(self, element: WebElement) -> dict:
        """
        Scroll to the specified element and get location
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.location
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_size(self, element: WebElement) -> dict:
        """
        Scroll to the specified element and get size
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.size
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_tag_name(self, element: WebElement) -> str:
        """
        Scroll to the specified element and get tag name
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.tag_name
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_rect(self, element: WebElement) -> dict:
        """
        Scroll to the specified element and get rect
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.rect
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_is_displayed(self, element: WebElement) -> bool:
        """
        Scroll to the specified element and get is displayed
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.is_displayed()
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_is_enabled(self, element: WebElement) -> bool:
        """
        Scroll to the specified element and get is enabled
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.is_enabled()
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_to_element_and_get_is_selected(self, element: WebElement) -> bool:
        """
        Scroll to the specified element and get is selected
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.is_selected()
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_into_view(self, element: WebElement):
        """
        Scroll to the specified element
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def scroll_into_view_and_click(self, element: WebElement):
        """
        Scroll to the specified element and click
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
        except Exception as error:
            logging.error(f"Operation Failed: {error}")
