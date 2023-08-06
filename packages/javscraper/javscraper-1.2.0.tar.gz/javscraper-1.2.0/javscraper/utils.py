import cloudscraper

from typing import List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

__all__ = ["SCRAPER", "JAVResult", "perform_request", "fix_jav_code", "USER_AGENT", "jav_code_to_content"]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/85.0.4183.121 Safari/537.36"

# Global scraper without needing to make a new instance per request
SCRAPER = cloudscraper.create_scraper(
    # Make sure mobile pages are not served
    browser={
        "custom": USER_AGENT
    }
)


@dataclass
class JAVResult:
    """Results returned for a site"""
    name: str
    code: str
    studio: str
    image: str
    actresses: List[str]
    genres: List[str]
    release_date: datetime
    sample_video: Optional[str] = None
    description: Optional[str] = None
    score: Union[int, float] = 0


def perform_request(method: str, url: str, *args, **kwargs):
    """
    Creates a request with cloudscraper to avoid being stopped by cloudflare
    :param method: HTTP Method
    :param url: HTTP URL
    :param args: args to pass into cloudscraper
    :param kwargs: kwargs to pass into cloudscraper
    :return:
    """
    return SCRAPER.request(method, url, *args, **kwargs)


def jav_code_to_content(code: str) -> str:
    """
    Unfixes a fixed JAV code to a content code for DMM.
    :param code:
    :return:
    """
    letters = ""
    numbers = ""

    # Force lowercase
    code = code.lower()

    # Find starting letters (IPX-XXX)
    for char in code:
        # For characters in lowercase alphabet or is a number
        if ord(char) in range(97, 123):
            letters += char
        elif ord(char) in range(48, 58):
            numbers += char

    # Return rejoined code with padded number
    number = int(numbers) if numbers else 00000
    return f"{letters}{number:05}"


def fix_jav_code(code: str) -> str:
    """
    Fixes JAV code for a joined code, only works with standard? codes,
    non amateur or other studios.
    :param code: Code to fix
    :return: Fixed code
    """
    letters = ""
    numbers = ""

    # Force uppercase
    code = code.upper()

    # Find starting letters (IPX-XXX)
    for char in code:
        # For characters in uppercase alphabet or is a number
        if ord(char) in range(65, 91):
            letters += char
        elif ord(char) in range(48, 58):
            numbers += char

    # Return rejoined code with padded number
    number = int(numbers)
    return f"{letters}-{number:03}"
