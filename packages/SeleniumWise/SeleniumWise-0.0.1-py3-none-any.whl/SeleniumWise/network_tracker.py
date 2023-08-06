"""
The Module is used to track the network traffic of the browser.
"""
import logging
import json
from typing import Any


class NetworkTracker:
    """
    The Class is used to track the network traffic of the browser.
    """

    def __init__(self, driver):
        self.driver = driver

    def get_network_traffic(self) -> list[Any]:
        """
        Get network traffic
        :return: network traffic
        """
        try:
            entries = self.driver.get_log("performance")
            entries = [json.loads(entry["message"])["message"] for entry in entries]
            entries = [
                entry for entry in entries if "Network.response" in entry["method"]
            ]
            return entries
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def get_network_traffic_by_url(self, url: str) -> list[Any]:
        """
        Get network traffic by url
        :param url: url
        :return: network traffic
        """
        try:
            entries = self.get_network_traffic()
            entries = [
                entry for entry in entries if entry["params"]["response"]["url"] == url
            ]
            return entries
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def get_network_traffic_by_status(self, status: int) -> list[Any]:
        """
        Get network traffic by status
        :param status: status
        :return: network traffic
        """
        try:
            entries = self.get_network_traffic()
            entries = [
                entry
                for entry in entries
                if entry["params"]["response"]["status"] == status
            ]
            return entries
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def get_network_traffic_by_type(self, type: str) -> list[Any]:
        """
        Get network traffic by type
        :param type: type
        :return: network traffic
        """
        try:
            entries = self.get_network_traffic()
            entries = [entry for entry in entries if entry["params"]["type"] == type]
            return entries
        except Exception as error:
            logging.error(f"Operation Failed: {error}")

    def get_network_traffic_by_url_and_status(self, url: str, status: int) -> list[Any]:
        """
        Get network traffic by url and status
        :param url: url
        :param status: status
        :return: network traffic
        """
        try:
            entries = self.get_network_traffic()
            entries = [
                entry
                for entry in entries
                if entry["params"]["response"]["url"] == url
                and entry["params"]["response"]["status"] == status
            ]
            return entries
        except Exception as error:
            logging.error(f"Operation Failed: {error}")
