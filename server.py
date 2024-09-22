import logging
from datetime import datetime

import requests
from flask import Flask, render_template, request
from flask_cors import CORS

from config import filename, base_url, does_not_exist_message, added_message, already_added_message, \
    all_offline_message, online_message, removed_message, remove_message_not_in_list, \
    remove_empty_string, too_many_requests, list_all_message

app = Flask(__name__, static_folder='templates/assets', static_url_path='/assets')
CORS(app)

headers = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

logging.basicConfig(level=logging.DEBUG)

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
                    file.write('{}\n'.format(person))
                    file.close()
                message = added_message.format(person)
            else:
                message = already_added_message.format(person)

    return render_template('add.html', message=message)


@app.route('/list/', methods=['post', 'get'])
def list_all():
    message = ''
    if request.method == 'POST':
        person = request.form.get('name')
        if person:
            found = remove_line_from_file(person)
            if found:
                message = removed_message.format(person)
            else:
                message = remove_message_not_in_list.format(person)
        else:
            message = remove_empty_string

    my_file = open(filename, 'r')
    people = my_file.readlines()
    my_file.close()

    people_list = {}
    for person in people:
        new_key_values_dict = {list_all_message.format(person): base_url.format(person)}
        people_list.update(new_key_values_dict)

    data = [people_list]

    return render_template('list.html', data=data,  message=message)


@app.route('/', methods=['get', 'post'])
def home():
    return render_template('home.html')


@app.route('/online/', methods=['post', 'get'])
def online():
    import pytz

    tz = pytz.timezone('Europe/Amsterdam')
    now = datetime.now(tz)
    logging.info(f'Online check called at {now}')

    _online = {}
    person_data = sorted(read_file())
    for person in person_data:
        resp = make_request(person)

        if resp.status_code == 429:
            logging.error('Status code was {}'.format(resp.status_code))
            _dict = [{too_many_requests: base_url.format("")}]
            return render_template('online.html', data=_dict)

        offline_count = str(resp.content).count('offline')

        logging.info(f'Offline count for user {person} is {offline_count}')

        if offline_count == 5:
            new_key_values_dict = {online_message.format(person): base_url.format(person)}
            _online.update(new_key_values_dict)

    if not len(_online):
        _online.update({all_offline_message: base_url.format("")})
    online_dict = [_online]
    return render_template('online.html', data=online_dict)


def get_method(url):
    return requests.get(url)


def check_for_string(string_to_search):
    with open(filename, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False


def remove_line_from_file(person):
    found = 0
    lines = read_file()
    with open(filename, 'w') as f:
        for line in lines:
            if line.strip('\n') == person:
                found = 1
            else:
                f.write(line)
        f.close()
    return found


def make_request(person):
    person = person.rstrip('\n')
    session = requests.Session()
    session.headers['User-Agent'] = headers
    return session.get(base_url.format(person))


def read_file():
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
