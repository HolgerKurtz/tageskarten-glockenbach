# script to web scrape food data
# THOUGHTS:
# Starting with bs4 maybe switching to a more complex crawler later

import io
import requests
from bs4 import BeautifulSoup
import PyPDF2 as pypdf
import json


class Restaurants:
    def __init__(self, ID: str):
        self.ID = ID
        self.FULL_NAME = self._restaurant_data("full_name")
        self.ADDRESS = self._restaurant_data("address")

    def _restaurant_data(self, info):
        with open("restaurants.json") as json_file:
            data = json.load(json_file)
            restaurant_info = data[self.ID][info]
        return restaurant_info

    def get_tageskarte(self):
        restaurant_url = self._restaurant_data("url")
        response = requests.get(restaurant_url)
        soup = BeautifulSoup(response.text, "html.parser")

        if self.ID == "1":
            # faun
            for a in soup.find_all("a", href=True):
                if ("MITTAGSKARTE" in a.get_text()) and (".pdf" in a.get("href")):
                    tageskarte_url = f"{restaurant_url}{a.get('href')}"
                    return self.get_pdf_data(tageskarte_url), tageskarte_url

        elif self.ID == "2":  # rumpler
            tageskarte = "<table>"
            for tr in soup.find_all("table")[1]:
                tageskarte += str(tr)

            tageskarte += "</table>"
            return [tageskarte, "n/a"], restaurant_url

        elif self.ID == "3":  # kaiser otto
            link_tageskarte = soup.find_all("a", href=True)[8]
            full_link_tageskarte = f"{restaurant_url}{link_tageskarte.get('href')}"
            return self.get_pdf_data(full_link_tageskarte), full_link_tageskarte

        elif self.ID == "4":  # FUGAZI
            tageskarte_raw = soup.find_all(
                "div", class_="sqs-block-content")

            tageskarte_formatted = "".join(
                [str(x) for x in tageskarte_raw])

            return [tageskarte_formatted, "n/a"], restaurant_url

        elif self.ID == "5":  # Le Du
            return [self._restaurant_data("menu"), "n/a"], restaurant_url

        elif self.ID == "6":  # Tabula Rasa
            return [self._restaurant_data("menu"), "n/a"], restaurant_url

        elif self.ID == "7":  # Cafe Schneewitchen
            tageskarte_url = self._restaurant_data("url")
            # TODO: format pdf data
            return self.get_pdf_data(tageskarte_url), tageskarte_url

    def get_pdf_data(self, tageskarte_url):
        response = requests.get(tageskarte_url)
        print(response.status_code)
        with io.BytesIO(response.content) as open_pdf_file:
            read_pdf = pypdf.PdfFileReader(open_pdf_file)
            # .getDocumentInfo()#.getPage(0)# .extractText()
            created_at = read_pdf.getXmpMetadata().xmp_modifyDate
            page_string = read_pdf.getPage(0).extractText()
            tageskarte_formatted = page_string.replace(
                "\n", "<br><br>").replace("•", " <br> ")
        return tageskarte_formatted, created_at


if __name__ == "__main__":
    r = Restaurants("6")
    r.get_tageskarte()
