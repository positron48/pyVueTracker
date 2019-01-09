# все импорты
import datetime as dt
from backend.lib.hamster.db import Storage
from backend.lib.hamster import Fact
from backend.src.model.hamster import Fact as Fact2
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from backend.src.model.mysql import db
from backend.src.auth import Auth
from backend.src.controller import ApiController
from flask_debugtoolbar import DebugToolbarExtension
import json
from flask_migrate import Migrate

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
dtb = DebugToolbarExtension(app)


@app.route('/debug/fill_external')
def fill():
    from backend.src.sheduler import Sheduler
    user = Auth.get_user_by_token('MQinK4')
    s = Sheduler(user)
    return s.fetch_external_data()

@app.route('/debug/add_user')
def add_users():
    from backend.src.model.mysql import Tracker, User, TrackerUserLink
    trackerEvo = Tracker(title='evolution', code='evo', api_url=app.config.get('EVO_URL'), type='evo')
    trackerRedmine = Tracker(title='redmine', code='redmine', api_url=app.config.get('REDMINE_URL'), type='redmine')
    user = User(login='login', hash=Auth.get_hash('login', 'password', app.config.get('SALT')), token='MQinK4')
    user2 = User(login='login2', hash=Auth.get_hash('login2', 'password2', app.config.get('SALT')), token='MQinK42')

    tracker_link = TrackerUserLink(tracker=trackerEvo, user=user, external_api_key=app.config.get('REDMINE_KEY'))
    tracker_link2 = TrackerUserLink(tracker=trackerRedmine, user=user, external_api_key=app.config.get('EVO_KEY'))
    tracker_link3 = TrackerUserLink(tracker=trackerRedmine, user=user2)

    db.session.add(tracker_link)
    db.session.add(tracker_link2)
    db.session.add(tracker_link3)
    db.session.commit()
    return 'done!'

@app.route('/debug/regen')
def regen():
    # генератор тестовых данных
    from backend.src.model.mysql import Tracker, User, TrackerUserLink
    db.drop_all()
    db.create_all()
    return 'success!'


    # todo тест каскадных удалений
    from backend.src.model.mysql import User, Project, TrackerUserLink, Tracker, UserProjectLink

    user1 = User(login='first', hash='hash', token='asdasdasd')
    user2 = User(login='two', hash='hash', token='asdasd')
    user3 = User(login='three', hash='hash', token='asdasdfd')
    proj1 = Project(title='first2', code='frst')
    proj2 = Project(title='two', code='two')
    user2.projects.append(proj2)
    user3.projects.append(proj1)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    tracker = Tracker(title='title', code='code', ui_url='url', api_url='base')
    link = TrackerUserLink(tracker=tracker, user=user1, external_user_id=1234)
    alias = UserProjectLink(user=user1, project=proj1, aliases='alias1, alias2, alias3')
    db.session.add(link)
    db.session.add(alias)

    db.session.commit()
    result = '<p>add</p>'
    for user in User.query.all():
        result += repr(user)
    db.session.delete(user2)
    db.session.commit()
    return result


@app.route('/regen')
def regen_old():
    # генератор тестовых данных
    from backend.src.model.mysql import Tracker, User, TrackerUserLink
    db.drop_all()
    db.create_all()
    trackerRedmine = Tracker(title='intaro redmine', code='redmine', api_url=app.config.get('REDMINE_URL'), type='redmine')
    trackerEvo = Tracker(title='evolution', code='evo', api_url=app.config.get('EVO_URL'), type='evo')
    user = User(login='login', hash=Auth.get_hash('login', 'password', app.config.get('SALT')), token='MQinK4')
    user2 = User(login='login2', hash=Auth.get_hash('login2', 'password2', app.config.get('SALT')), token='MQinK42')
    db.session.add(user)
    db.session.add(user2)
    db.session.add(trackerRedmine)
    #подставь ниже api_key - при пересоздании таблиц проекты и задачи подтянутся в БД с редмайна
    tracker_link = TrackerUserLink(tracker=trackerRedmine, user=user, external_api_key=app.config.get('REDMINE_KEY'))
    tracker_link2 = TrackerUserLink(tracker=trackerEvo, user=user, external_api_key=app.config.get('EVO_KEY'))
    tracker_link3 = TrackerUserLink(tracker=trackerRedmine, user=user2)
    db.session.add(tracker_link)
    db.session.add(tracker_link2)
    db.session.add(tracker_link3)
    db.session.commit()

    return 'success!'


@app.route('/test')
def test():
    token = request.cookies.get('token')
    return jsonify(locals())


@app.route('/api/auth', methods=['POST'])
def auth():
    error = None

    def get(field):
        global error
        value = request.values.get(field)
        if value is None:
            error = 'заполни' + field
        if field not in ('password', 'token'):
            return value.lower()
        return value

    login, password, action = get('login'), get('password'), get('action')

    if error is not None:
        return jsonify({'message': error})

    hash = Auth.get_hash(login, password, app.config.get('SALT'))

    user = None
    if action == 'login':
        user = Auth.get_user_by_login_and_hash(login, hash)
    if action == 'registration':
        user = Auth.add_new_user(login, hash)

    if user is None:
        message = {
            'login': 'У нас нет пользователя с такими учетными данными.\r\nСкорее всего ты очепятался.',
            'registration': 'такой логин уже занят, попробуй другой'
        }[action]
        return jsonify({'message': message})

    response = {'token': user.token}

    return jsonify(response)


@app.route('/api/tasks')
@Auth.check_api_request
def get_tasks():
    now = dt.datetime.now()

    interval = request.args.get('interval')
    dateFrom = now - dt.timedelta(days=1)
    dateTo = now

    if interval is not None:
        interval = interval.split('-')
        if len(interval) == 2:
            dateFrom = dt.datetime.strptime(interval[0], "%d.%m.%Y")
            dateTo = dt.datetime.strptime(interval[1], "%d.%m.%Y")
        else:
            dateFrom = dt.datetime.strptime(interval[0], "%d.%m.%Y")
            dateTo = dateFrom

    if app.config.get('SQLITE'):
        storage = Storage()
        last_entries = storage.get_formated_facts(dateFrom, dateTo)
        return jsonify({"tasks": last_entries})

    api = ApiController()
    return api.get_tasks(dateFrom, dateTo)


@app.route('/api/trackers')
@Auth.check_api_request
def get_trackers():
    api = ApiController()
    return api.get_trackers()


@app.route('/api/evoUsers')
@Auth.check_api_request
def get_evo_users():
    api = ApiController()
    return api.get_evo_users()


@app.route('/api/current')
@Auth.check_api_request
def get_current():
    if app.config.get('SQLITE'):
        dateFrom = dt.datetime.now()

        storage = Storage()
        last_entries = storage.get_formated_facts(dateFrom)

        for k, item in enumerate(last_entries):
            if item['end_time'] is '':
                item['status'] = True
                return jsonify(item)

        return jsonify({"status": False})

    api = ApiController()
    return api.get_current()


@app.route('/api/completitions')
@Auth.check_api_request
def complete_task():
    if app.config.get('SQLITE'):
        storage = Storage()
        return jsonify({"values": storage.get_suggestions()})

    text = request.values.get('text')
    api = ApiController()
    return api.get_autocomlete(text)


@app.route('/api/grouped_tasks')
@Auth.check_api_request
def get_grouped_tasks():
    now = dt.datetime.now()

    interval = request.args.get('interval')
    dateFrom = now
    dateTo = now + dt.timedelta(days=1)

    if interval != None:
        interval = interval.split('-')
        if len(interval) == 2:
            dateFrom = dt.datetime.strptime(interval[0], "%d.%m.%Y")
            dateTo = dt.datetime.strptime(interval[1], "%d.%m.%Y") + dt.timedelta(days=1)
        else:
            dateFrom = dt.datetime.strptime(interval[0], "%d.%m.%Y")
            dateTo = dateFrom + dt.timedelta(days=1)

    if app.config.get('SQLITE'):
        storage = Storage()
        tasks = storage.get_facts_by_dates(dateFrom, dateTo)
        # jsonify always encode unicode
        return app.response_class(json.dumps({"tasks": tasks}, ensure_ascii=False), mimetype='application/json')

    api = ApiController()
    return api.get_grouped_tasks(dateFrom, dateTo)


@app.route('/api/projects')
@Auth.check_api_request
def get_projects():
    project_ids = request.args.getlist('projects[]')
    project_ids = list(map(int, project_ids))

    api = ApiController()
    return api.get_projects(project_ids)


@app.route('/api/task', methods=['POST'])
@Auth.check_api_request
def add_entry():
    if app.config.get('SQLITE'):
        storage = Storage()
        id = storage.add_fact(request.values['name'])
        return jsonify({"status": True, "id": id})

    name = request.values.get('name').strip()
    api = ApiController()
    return api.add_activity(name)


@app.route('/api/tracker', methods=['POST'])
@Auth.check_api_request
def save_tracker():
    # todo: валидация
    id = request.values.get('id')
    type = request.values.get('type')
    title = request.values.get('title').strip()
    api_url = request.values.get('api_url').strip()

    api = ApiController()
    return api.save_tracker(id, type, title, api_url)


@app.route('/api/evoUser', methods=['POST'])
@Auth.check_api_request
def save_evo_user():
    id = request.values.get('id')

    api = ApiController()
    return api.save_evo_user(id)


@app.route('/api/tracker/delete', methods=['POST'])
@Auth.check_api_request
def delete_tracker():
    # todo: валидация
    id = request.values.get('id')

    api = ApiController()
    return api.delete_tracker(id)


@app.route('/api/getToken', methods=['POST'])
@Auth.check_api_request
def get_token():
    tracker_id = request.values.get('id')
    login = request.values.get('login').strip()
    password = request.values.get('password')
    api = ApiController()
    return api.get_token(tracker_id, login, password)


@app.route('/api/task/edit', methods=['POST'])
@Auth.check_api_request
def edit_task():
    fact = {
        'id': request.values['id'],
        'name': request.values['name'],
        'category': request.values['category'],
        'date': request.values['date'],
        'start_time': request.values['start_time'],
        'end_time': request.values['end_time'],
        'description': request.values['description'],
        'tags': [tag.strip() for tag in request.values['tags'].split(',')]
    }
    start_dt = dt.datetime.strptime(fact['date'] + ' ' + fact['start_time'], "%d.%m.%Y %H:%M")
    if len(fact['end_time']) < 5:
        end_dt = None
    else:
        end_dt = dt.datetime.strptime(fact['date'] + ' ' + fact['end_time'], "%d.%m.%Y %H:%M")

    if app.config.get('SQLITE'):
        storage = Storage()
        db_fact = storage.get_fact(request.values['id'])
        for k, v in fact.items():
            db_fact[k] = v
        fact = db_fact
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
        return jsonify({"status": True, "id": result})

    api = ApiController()
    return api.edit_task(fact['id'], Fact2(
        activity=fact['name'],
        category=fact['category'],
        description=fact['description'],
        start_time=start_dt,
        end_time=end_dt,
        tags=fact['tags']
    ))


@app.route('/api/task/stop', methods=['POST'])
@Auth.check_api_request
def stop_task():
    id = int(request.values['id'])
    if app.config.get('SQLITE'):
        storage = Storage()
        result = storage.touch_fact(id)
        return jsonify(result)

    api = ApiController()
    return api.stop_task(id)


@app.route('/api/task/resume', methods=['POST'])
@Auth.check_api_request
def resume_task():
    id = int(request.values['id'])
    if app.config.get('SQLITE'):
        storage = Storage()
        result = storage.resume_fact(id)
        return jsonify(result)

    api = ApiController()
    return api.resume_task(id)


@app.route('/api/task/delete', methods=['POST'])
@Auth.check_api_request
def delete_task():
    id = int(request.values['id'])

    if app.config.get('SQLITE'):
        storage = Storage()
        result = storage.remove_fact(id)
        return jsonify(result)

    api = ApiController()
    return api.delete_task(id)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)
