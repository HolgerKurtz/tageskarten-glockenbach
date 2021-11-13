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

    def get_pdf_data(self, tageskarte_url):
        response = requests.get(tageskarte_url)
        print(response.status_code)
        with io.BytesIO(response.content) as open_pdf_file:
            read_pdf = pypdf.PdfFileReader(open_pdf_file)
            created_at = read_pdf.getXmpMetadata().xmp_modifyDate # .getDocumentInfo()#.getPage(0)# .extractText()
            page_string = read_pdf.getPage(0).extractText()
            tageskarte_formatted = page_string.replace("\n", "<br><br>").replace("•", " <br> ")
        return tageskarte_formatted, created_at


if __name__ == "__main__":
    r = Restaurants("1")
    info = r.get_pdf_data("https://faun-muenchen.de/site/assets/files/1074/mittag18_10_21.pdf")
    print(info)