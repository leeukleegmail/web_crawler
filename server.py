import requests
from flask import Flask, render_template, request
from flask_cors import CORS

from config import filename, base_url, does_not_exist_message, added_message, already_added_message, \
    all_offline_message, online_message, offline_message

app = Flask(__name__, static_folder='templates/assets', static_url_path='/assets')
CORS(app)


@app.route('/add/', methods=['post', 'get'])
def add():
    message = ''
    if request.method == 'POST':
        person = request.form.get('name')
        if get_method(base_url.format(person)).status_code == 404:
            message = does_not_exist_message.format(person)
        else:
            if not check_for_string(person):
                with open(filename, 'a') as file:
                    file.write("{}\n".format(person))
                    file.close()
                message = added_message.format(person)
            else:
                message = already_added_message.format(person)

    return render_template('add.html', message=message)


@app.route('/list/')
def list_all():
    my_file = open(filename, "r")
    data = my_file.readlines()
    return render_template("list.html", data=data)


@app.route('/', methods=['post', 'get'])
def check():
    online = []
    my_file = open(filename, "r")
    person_data = my_file.readlines()
    for person in person_data:
        person = person.rstrip("\n")
        session = requests.Session()
        session.headers[
            "User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        if str(session.get(base_url.format(person)).content).count("offline") == 4:
            print(online_message.format(person, base_url.format(person)))
            online.append(online_message.format(person, base_url.format(person)))
        else:
            print(offline_message.format(person))
    if not len(online):
        online.append(all_offline_message)

    return render_template("check.html", data=online)


def get_method(url):
    return requests.get(url)


def check_for_string(string_to_search):
    with open(filename, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
