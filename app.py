# все импорты
import datetime as dt
from backend.lib.hamster.db import Storage
from backend.lib.hamster import parse_fact
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

    last_entries = storage.get_facts(dateFrom, dateTo)

    for k, item in enumerate(last_entries):
        last_entries[k]['delta'] = round(item['delta'].seconds/3600, 2)
        last_entries[k]['date'] = item['date'].strftime('%d.%m.%Y')
        last_entries[k]['start_time'] = item['start_time'].strftime('%H:%M')
        if item['end_time'] is not None:
            last_entries[k]['end_time'] = item['end_time'].strftime('%H:%M')
        else:
            last_entries[k]['end_time'] = ''

    return jsonify({"tasks": last_entries})


@app.route('/api/completitions')
def complete_task():
    storage = Storage()
    return jsonify({"values": storage.get_suggestions()})

@app.route('/api/task', methods=['POST'])
def add_entry():
    storage = Storage()
    result = storage.add_fact(request.values['name'])
    return jsonify(result)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")