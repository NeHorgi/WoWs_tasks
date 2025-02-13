import pytest
import requests
from bs4 import BeautifulSoup, Tag

from wiki_table_test.constants import constants
from wiki_table_test.models import CompanyInfo


@pytest.fixture(scope="session")
def fetch_html_wiki_table() -> BeautifulSoup:
    url = requests.get(constants.table_url)
    return BeautifulSoup(url.text, "html.parser")


def parse_wiki_table(soup: BeautifulSoup) -> list[CompanyInfo]:
    table = soup.find("table")
    parsed_data = []

    for row in table.find_all("tr"):
        columns = row.find_all("td")
        if not columns:
            continue
        row_data = []
        for index, column in enumerate(columns):
            text = clean_text(column)
            if index == 1:
                numbers = [int(s) for s in text.replace(".", "").replace(",", "").split()
                           if s.isdigit()]
                text = numbers[0] if numbers else text
            row_data.append(text)
        parsed_data.append(CompanyInfo(*row_data))

    return parsed_data


def clean_text(element: Tag) -> str:
    for a_tag in element.find_all("a"):
        a_tag.unwrap()
    for sup_tag in element.find_all("sup", class_="reference"):
        sup_tag.decompose()
    return element.get_text(strip=True)


@pytest.fixture(scope="session")
def wiki_table_data(fetch_html_wiki_table) -> list[CompanyInfo]:
    return parse_wiki_table(fetch_html_wiki_table)
