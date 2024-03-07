import requests
from bs4 import BeautifulSoup
import re

class AptoideApp:
    """Class for scraping the Aptoide App store (https://en.aptoide.com)."""
    def __init__(self, url: str):
        self.url = url
        self.soup = self.parse_html_as_soup()
        if self.soup:
            self.app_name = self.parse_app_name()
            self.app_version = self.parse_app_version()
            self.downloads = self.parse_downloads()
            self.release_date = self.parse_release_date()
            self.description = self.parse_description()
        else:
            raise ValueError("There was an error instantiating the AptoideApp class.")

    def parse_html_as_soup(self) -> BeautifulSoup:
        """Checks if URL is a valid Aptoide URL and returns BeautifulSoup object if valid."""
        if not(self.url.endswith(".aptoide.com/app")):
            raise ValueError("The provided URL is an invalid link to an Aptoide app.")
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return BeautifulSoup(response.text,
                                features="html.parser")
            else: 
                raise ValueError(f"HTTP Status Code {response.status_code}")
        except:
            raise ValueError("There was an error in processing the GET request.")

    def parse_app_name(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns app name."""
        try:
            regex = re.compile("app-informations__Title")
            return self.soup.find("h1", {"class": regex}).get_text()
        except:
            raise ValueError("There was an error parsing the app name.")

    def parse_app_version(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns app version."""
        try:
            regex = re.compile("VersionsRatingRow")
            return self.soup.find("div", {"class": regex}).span.get_text()
        except:
            raise ValueError("There was an error parsing the app version.")

    def parse_downloads(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns number of app downloads."""
        try:
            regex = re.compile("DetailsMainSpan")
            return self.soup.find("span", {"class": regex}).get_text()
        except:
            raise ValueError("There was an error parsing the app downloads.")

    def parse_release_date(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns app release date as string in DD-MM-YYYY format."""
        try:
            regex = re.compile("VersionsRatingRow")
            return self.soup.find("div", {"class": regex}).find_next('span').find_next('span').get_text()[1:-1]
        except:
            raise ValueError("There was an error parsing the release date.")

    def parse_description(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns app description."""
        try:
            regex = re.compile("description")
            children = self.soup.find("div", {"itemprop": regex}).findChildren()
            els = [el.get_text() for el in children]
            return '\n'.join(els)
        except:
            raise ValueError("There was an error parsing the description.")

