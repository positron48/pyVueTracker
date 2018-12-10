# все импорты
import datetime as dt
from backend.lib.hamster.db import Storage
from backend.lib.hamster import parse_fact, Fact
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from backend.lib.hamster.model import db

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_pyfile('config.py')
db.init_app(app)

@app.route('/regen')
def regen():
    db.drop_all()
    db.create_all()
    #todo тест каскадных удалений
    from backend.lib.hamster.model import User, Property, PropType, Project
    type = PropType('prop1t')
    prop1 = Property('prop1')

    user1 = User('first', 'hash')
    user2 = User('two', 'hash')
    user3 = User('three', 'hash')
    proj1 = Project('first2', 'frst')
    proj2 = Project('two', 'two')
    user1.projects.append(proj1)
    user2.projects.append(proj2)
    user3.projects.append(proj1)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    result = '<p>add</p>'
    for user in User.query.all():
        result += repr(user)
    #db.session.delete(proj1)
    #db.session.commit()
    return result


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
    fact['tags'] = [tag.strip() for tag in request.values['tags'].split(',')]

    start_dt = dt.datetime.strptime(fact['date'] + ' ' + fact['start_time'], "%d.%m.%Y %H:%M")

    if fact['end_time']:
        end_dt = dt.datetime.strptime(fact['date'] + ' ' + fact['end_time'], "%d.%m.%Y %H:%M")
    else:
        end_dt = None

    # todo: сделать инициализацию факта по id
    factNew = Fact(
        id=fact['id'],
        activity=fact['name'],
        category=fact['category'],
        start_time=fact['start_time'],
        end_time=fact['end_time'],
        description=fact['description'],
        tags=fact['tags']
    )

    result = storage.update_fact(fact['id'], factNew.serialized_name(), start_dt, end_dt)


    return jsonify(result)

@app.route('/api/stop', methods=['POST'])
def stop_tracking():
    storage = Storage()
    result = storage.stop_tracking(dt.datetime.now())
    return jsonify(result)

@app.route('/api/task/stop', methods=['POST'])
def stop_task():
    id = int(request.values['id'])
    storage = Storage()
    result = storage.touch_fact(id)

    return jsonify(result)


@app.route('/api/task/resume', methods=['POST'])
def resume_task():
    id = int(request.values['id'])
    storage = Storage()
    result = storage.resume_fact(id)

    return jsonify(result)

@app.route('/api/task/delete', methods=['POST'])
def delete_task():
    id = int(request.values['id'])
    storage = Storage()
    result = storage.remove_fact(id)

    return jsonify(result)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")