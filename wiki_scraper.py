# Source: Geeks for Geeks - Web scraping from Wikipedia using Python – A Complete Guide
# Accessed 4/19/22
# URL: https://www.geeksforgeeks.org/web-scraping-from-wikipedia-using-python-a-complete-guide/

# import required modules
from bs4 import BeautifulSoup
import requests


def get_text_under(url, title_name):
    # get URL
    page = requests.get(url)
    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')
    headlines = soup.find_all('span', {"class": "mw-headline"})
    for headline in headlines:
        for title in headline:
            if title == title_name:  # correct title was found
                # get the paragraph by navigating back to the header then to sibling paragraph
                header = headline.find_parent('h2')
                paragraphs = []
                paragraph = header.find_next_sibling()
                # print paragraph until encounters next section marked by h2
                while paragraph.name != 'h2':
                    paragraphs.append(paragraph)
                    paragraph = paragraph.find_next_sibling()
                # create easily readable form
                return_str = ""
                for paragraph in paragraphs:
                    return_str += paragraph.get_text()
                    return_str += "\n"
                return return_str
    return 'title does not exist'
