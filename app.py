from flask import Flask, render_template, request, redirect, url_for
import wiki_scraper as scraper

app = Flask(__name__)  # __name__ is a DUNDER (double under, look up)
app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def get_plant():
    if request.method == "POST":
        plant = request.form['plantname']
        # replace underscores for spaces
        undscr_name = ''
        for letter in plant:
            if letter == " ":
                undscr_name += "_"
            else:
                undscr_name += letter
        data = scraper.get_text_under(f"https://en.wikipedia.org/wiki/{undscr_name}", "Description")
        return render_template('display.html', header=plant, data=data)
    else:
        txt_block = scraper.get_text_under('https://en.wikipedia.org/wiki/Houseplant', "List of common houseplants")  # get description from wiki article
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', use_reloader=True, debug=True)
