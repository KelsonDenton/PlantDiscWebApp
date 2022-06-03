import json
from time import sleep
import requests


def get_item(url: str, title: list, plant_name=None):
    """
    Uses get_item() and get_photo() to get a description and photo of a plant
    :param url:
    :param title:
    :return: two strings description and photo_url, description being a description of the plant and photo url being the
    url returned by the api service of where a photo can be found.
    """
    description = get_description(url, title)
    if plant_name is not None:
        photo_url = get_photo(plant_name)
        return description, photo_url
    return description


def get_description(url: str, titles: list):
    """
    Uses reading and writing to wiki.json file to gather information from wiki_scraper.py
    :param url: string representing url of wikipedia article that must be scraped
    :param title: list of strings representing titles in decreasing priority to try to find on wiki page
    :return: string containing description if search was successful or title not found if unsuccessful
    """
    for title in titles:
        dict = {"url": url, "title": title}
        json_obj = json.dumps(dict)
        try:
            with open("wiki.json", "w") as openfile:
                openfile.write(json_obj)
        finally:
            openfile.close
        sleep(1.0)
        try:
            with open("wiki.json", "r") as openfile:
                wiki_info = json.load(openfile)
            try:
                data = wiki_info["text"]
            except:
                data = "Error communicating with Wikipedia"
        finally:
            openfile.close()
        if data != f"Title {title} does not exist":
            return data
    return data


def underscore_name(name: str):
    """
    Makes names have underscores for spaces for urls
    :param name: name that needs to be converted to underscore
    :return: name with underscores in place of spaces
    """
    underscr_name = ''
    for letter in name:
        if letter == " ":
            underscr_name += "_"
        else:
            underscr_name += letter
    return underscr_name


def get_photo(plant_name: str):
    """
    Uses microservice created by Elizabeth Khoury to get image urls
    :param plant_name: name of plant that is desired for image
    :return: string that is url of image
    """
    """api_url = "http://khourye.pythonanywhere.com/users"
    data = {'api_key': 'chickens456', 'keyword': plant_name + ' plant', 'num_images': 1}
    response = requests.post(api_url, json=data)
    resp = response.json()
    img_url = resp["urls"][0]
    return img_url"""
    pass
