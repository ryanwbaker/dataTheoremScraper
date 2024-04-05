import requests
from bs4 import BeautifulSoup, Tag
import re
from urllib.parse import urlparse

class AptoideApp:
    """Class for scraping the Aptoide App store (https://en.aptoide.com)."""
    def __init__(self, 
                 url: str, 
                 app_name: str = "", 
                 app_version: str = "", 
                 downloads: str = "", 
                 release_date: str = "",
                 description: str = "") -> None:
        self.url: str = url
        self.soup: BeautifulSoup = self.parse_html_as_soup()
        if self.soup is None:
            raise ValueError("Failed to parse HTML as BeautifulSoup object.")
        
        self.app_name: str = app_name
        self.app_version: str = app_version
        self.downloads: str = downloads
        self.release_date: str = release_date
        self.description: str = description

        if self.app_name == "":
            self.app_name = self.parse_app_name()
        if self.app_version == "":
            self.app_version = self.parse_app_version()
        if self.downloads == "":
            self.downloads = self.parse_downloads()
        if self.release_date == "":
            self.release_date = self.parse_release_date()
        if self.description == "":
            self.description = self.parse_description()


    def parse_html_as_soup(self) -> BeautifulSoup:
        """Checks if URL is a valid Aptoide URL and returns BeautifulSoup object if valid."""
        parsed_url = urlparse(self.url)
        # fragment not necessary because requested app is sent as query string (falcon request object removes fragment when parsed)
        if not(parsed_url.scheme == 'https'):
            raise ValueError("The provided URL does not have an https scheme.")
        if not(parsed_url.netloc.endswith('.aptoide.com')):
            raise ValueError("The provided URL does not come from the aptoide.com domain.")
        if not(parsed_url.path == '/app'):
            raise ValueError("The provided URL does not have the path '/app'.")
        if not(parsed_url.query == ''):
            raise ValueError("The provided URL contains a query string.")
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return BeautifulSoup(response.text,
                                features="html.parser")
            else: 
                raise ValueError(f"HTTP Status Code {response.status_code} when accessing provided URL.")
        except Exception as e:
            raise ValueError(f"There was an error in processing the GET request. {e}")


    def parse_app_name(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns app name."""
        try:
            regex = re.compile("app-informations__Title")
            soup_obj = self.soup.find("h1", {"class": regex})
            if soup_obj is not None:
                return soup_obj.get_text()
            else:
                raise ValueError("Failed to find app name element.")
        except Exception as e:
            raise ValueError("There was an error parsing the app name:", e)


    def parse_app_version(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns app version."""
        try:
            regex = re.compile("VersionsRatingRow")
            soup_obj = self.soup.find("div", {"class": regex})
            if soup_obj is not None:
                if isinstance(soup_obj, Tag):
                    soup_obj = soup_obj.span
                    if soup_obj is not None:
                        return soup_obj.get_text()
            raise ValueError("Failed to find app version element.")
        except Exception as e:
            raise ValueError("There was an error parsing the app version:", e)


    def parse_downloads(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns number of app downloads."""
        try:
            regex = re.compile("DetailsMainSpan")
            soup_obj = self.soup.find("span", {"class": regex})
            if soup_obj is not None:
                return soup_obj.get_text()
            else:
                raise ValueError("Failed to find downloads element.")
        except:
            raise ValueError("There was an error parsing the app downloads.")


    def parse_release_date(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns app release date as string in DD-MM-YYYY format."""
        try:
            regex = re.compile("VersionsRatingRow")
            soup_obj = self.soup.find("div", {"class": regex})
            if soup_obj is not None:
                soup_obj = soup_obj.find_next('span')
                if soup_obj is not None:
                    soup_obj = soup_obj.find_next('span')
                    if soup_obj is not None:
                        return soup_obj.get_text()[1:-1]
            raise ValueError("Failed to find release date element.")
        except Exception as e:
            raise ValueError("There was an error parsing the release date:", e)


    def parse_description(self) -> str:
        """Parses BeautifulSoup object from Aptoide store URL and returns app description."""
        try:
            regex = re.compile("description")
            soup_obj = self.soup.find("div", {"itemprop": regex})
            if isinstance(soup_obj, Tag):
                children = soup_obj.findChildren()
                els = [el.get_text() for el in children]
                return '\n'.join(els)
            else:
                raise ValueError("Failed to find description element")
        except Exception as e:
            raise ValueError("There was an error parsing the description:", e)


