import json
from time import sleep
import requests


def get_item(url: str, title: str, plant_name=None):
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


def get_description(url: str, title: str):
    """
    Uses reading and writing to wiki.json file to gather information from wiki_scraper.py
    :param url: string representing url of wikipedia article that must be scraped
    :param title: string representing title on page under which text will be scraped from
    :return: string containing description if search was successful or title not found if unsuccessful
    """
    # turn into JSON object
    dict = {"url": url, "title": title}
    json_obj = json.dumps(dict)
    # write info to JSON file
    try:
        with open("wiki.json", "w") as openfile:
            openfile.write(json_obj)
    finally:
        openfile.close
    sleep(1.0)
    # read from JSON file
    try:
        with open("wiki.json", "r") as openfile:
            wiki_info = json.load(openfile)
        data = wiki_info["text"]
    finally:
        openfile.close()
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
