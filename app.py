import time

from flask import Flask, render_template, request
import random
import retrieve_info

app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True


def truncate_plant_name(plant_name):
    """
    truncates the plant name to not include anything after parentheses or brackets
    :param plant_name: a string of a name of a plant to truncate
    :return: a name of a plant including everything before the brackets/parentheses
    """
    name = ''
    trunc_name = plant_name
    for letter in plant_name:
        if letter == "(" or letter == '[' or letter == ':':
            trunc_name = name[:-1]
        name += letter
    return trunc_name


# user searched using the search bar
@app.route('/', methods=['GET', 'POST'])
def get_plant():
    if request.method == "POST":  # searching for plant
        plant = request.form['plantname']
        # replace underscores for spaces
        underscr_name = retrieve_info.underscore_name(plant)
        desc_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}", "Description",
                                                  plant)
        if desc_information[0] == 'Title Description does not exist':  # look for alternative title
            desc_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}",
                                                      "Description and biology", plant)
        cult_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}", "Cultivation",
                                                  plant)
        if cult_information[0] == "Title Cultivation does not exist":  # look for alternative title
            cult_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}",
                                                      "Cultivation and uses", plant)
        if plant == '':  # display adequate error message
            plant = 'Sorry that plant could not be found. Please go back to the home screen and try again.'
        return render_template('display.html', header=plant, desc_data=desc_information[0],
                               cult_data=cult_information[0], img=desc_information[1])

    else:  # rendering home page list
        # get plant list from wiki article
        txt_block = retrieve_info.get_item('https://en.wikipedia.org/wiki/Houseplant', "List of common houseplants")
        # store information in readable block (list element for each line that has been returned)
        line = ""
        data = []
        for letter in txt_block:
            if letter == '\n':
                data.append(line)
                line = ""
            else:
                line += letter
        return render_template('home.html', data=data)


# user navigated using a link
@app.route('/link', methods=['GET'])
def list_search():
    args = request.args
    plant_name = args.get('plant')
    plant = truncate_plant_name(plant_name)  # convert into understandable form
    underscr_name = retrieve_info.underscore_name(plant)
    desc_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}", "Description", plant)
    if desc_information[0] == 'Title Description does not exist':  # look for alternative title
        desc_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}",
                                                  "Description and biology", plant)
    cult_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}", "Cultivation", plant)
    if cult_information[0] == "Title Cultivation does not exist":  # look for alternative title
        cult_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}",
                                                  "Cultivation and uses", plant)
    if plant == '':  # display adequate error message
        plant = 'Sorry that plant could not be found. Please go back to the home screen and try again.'
    return render_template('display.html', header=plant, desc_data=desc_information[0],
                           cult_data=cult_information[0], img=desc_information[1])


@app.route('/random', methods=['GET'])
def get_random():
    txt_block = retrieve_info.get_item('https://en.wikipedia.org/wiki/Houseplant', "List of common houseplants")
    time.sleep(1.0)
    # convert text into python list of plant names
    line = ""
    data = []
    for letter in txt_block:
        if letter == '\n':
            data.append(line)
            line = ""
        else:
            line += letter
    random_index = random.randint(0, len(data) - 1)
    while data[random_index] == '':
        random_index = random.randint(0, len(data) - 1)
    plant_name = truncate_plant_name(data[random_index])
    underscr_name = retrieve_info.underscore_name(plant_name)  # convert random plant name into underscore form
    # stop at parentheses if they are in name
    desc_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}", "Description",
                                              plant_name)
    time.sleep(1.0)
    if desc_information[0] == 'Title Description does not exist':  # look for alternative title
        desc_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}",
                                                  "Description and biology", plant_name)
    cult_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}", "Cultivation",
                                              plant_name)
    if cult_information[0] == "Title Cultivation does not exist":  # look for alternative title
        cult_information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}",
                                                  "Cultivation and uses", plant_name)
    if plant_name == '':  # display adequate error message
        plant_name = 'Sorry that plant could not be found. Please go back to the home screen and try again.'
    return render_template('display.html', header=plant_name, desc_data=desc_information[0],
                           cult_data=cult_information[0], img=desc_information[1])


if __name__ == '__main__':
    app.run(host='127.0.0.1', use_reloader=True, debug=True)
