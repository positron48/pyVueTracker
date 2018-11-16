# все импорты
import datetime as dt
from backend.lib.hamster.db import Storage
from backend.lib.hamster import parse_fact, Fact
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/tasks')
def get_tasks():
    now = dt.datetime.now()

    interval = request.args.get('interval')
    dateFrom = now - dt.timedelta(days=1)
    dateTo = now

    if interval != None:
        interval = interval.split('-')
        if len(interval) == 2:
            dateFrom = dt.datetime.strptime(interval[0], "%d.%m.%Y")
            dateTo = dt.datetime.strptime(interval[1], "%d.%m.%Y")
        else:
            dateFrom = dt.datetime.strptime(interval[0], "%d.%m.%Y")
            dateTo = dateFrom

    storage = Storage()

    last_entries = storage.get_formated_facts(dateFrom, dateTo)

    return jsonify({"tasks": last_entries})

@app.route('/api/current')
def get_current():

    dateFrom = dt.datetime.now()

    storage = Storage()
    last_entries = storage.get_formated_facts(dateFrom)

    for k, item in enumerate(last_entries):
        if item['end_time'] is '':
            return jsonify(item)

    return jsonify(None)


@app.route('/api/completitions')
def complete_task():
    storage = Storage()
    return jsonify({"values": storage.get_suggestions()})

@app.route('/api/task', methods=['POST'])
def add_entry():
    storage = Storage()
    result = storage.add_fact(request.values['name'])
    return jsonify(result)

@app.route('/api/task/edit', methods=['POST'])
def edit_task():
    storage = Storage()

    fact = storage.get_fact(request.values['id'])
    fact['name'] = request.values['name']
    fact['category'] = request.values['category']
    fact['date'] = request.values['date']
    fact['start_time'] = request.values['start_time']
    fact['end_time'] = request.values['end_time']
    fact['description'] = request.values['description']
    fact['tags'] = [tag.encode("utf-8").strip() for tag in request.values['tags'].split(',')]

    factNew = Fact(
        id=fact['id'],
        activity=fact['name'],
        category=fact['category'],
        date=fact['date'],
        start_time=fact['start_time'],
        end_time=fact['end_time'],
        description=fact['description'],
        tags=fact['tags']
    )

    result = storage.update_fact(fact['id'], factNew.serialized_name(), fact['start_time'], fact['end_time'])


    return jsonify(result)

@app.route('/api/stop', methods=['POST'])
def stop_tracking():
    storage = Storage()
    result = storage.stop_tracking(dt.datetime.now())
    return jsonify(result)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")