import time

from flask import Flask, render_template, request, redirect, url_for
import random
import retrieve_info

app = Flask(__name__)  # __name__ is a DUNDER (double under, look up)
app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def get_plant():
    if request.method == "POST":  # searching for plant
        plant = request.form['plantname']
        # replace underscores for spaces
        underscr_name = retrieve_info.underscore_name(plant)
        information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{underscr_name}", "Description", plant)
        print(information[1])
        return render_template('display.html', header=plant, data=information[0], img=information[1])

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

@app.route('/random', methods=['GET'])
def get_random():
    txt_block = retrieve_info.get_item('https://en.wikipedia.org/wiki/Houseplant', "List of common houseplants")
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
    underscr_name = retrieve_info.underscore_name(data[random_index])  # convert random plant name into underscore form
    time.sleep(1.2)
    # stop at parentheses if they are in name
    plant_name = underscr_name
    name = ''
    for letter in underscr_name:
        if letter == "(" or letter == '[' or letter == ':':
            plant_name = name[:-1]
            print(plant_name)
        name += letter
    information = retrieve_info.get_item(f"https://en.wikipedia.org/wiki/{plant_name}", "Description", plant_name)
    return render_template('display.html', header=data[random_index], data=information[0], img=information[1])


if __name__ == '__main__':
    app.run(host='127.0.0.1', use_reloader=True, debug=True)
