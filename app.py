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


# @app.route('/debug/fill_external')
# def fill():
#     from backend.src.sheduler import Sheduler
#     user = Auth.get_user_by_token('MQinK4')
#     s = Sheduler(user)
#     return s.fetch_external_data()
#
# @app.route('/debug/add_user')
# def add_users():
#     from backend.src.model.mysql import Tracker, User, TrackerUserLink
#     trackerEvo = Tracker(title='evolution', code='evo', api_url=app.config.get('EVO_URL'), type='evo')
#     trackerRedmine = Tracker(title='redmine', code='redmine', api_url=app.config.get('REDMINE_URL'), type='redmine')
#     user = User(login='login', hash=Auth.get_hash('login', 'password', app.config.get('SALT')), token='MQinK4')
#     user2 = User(login='login2', hash=Auth.get_hash('login2', 'password2', app.config.get('SALT')), token='MQinK42')
#
#     tracker_link = TrackerUserLink(tracker=trackerEvo, user=user, external_api_key=app.config.get('EVO_KEY'))
#     tracker_link2 = TrackerUserLink(tracker=trackerRedmine, user=user, external_api_key=app.config.get('REDMINE_KEY'))
#     tracker_link3 = TrackerUserLink(tracker=trackerRedmine, user=user2)
#
#     db.session.add(tracker_link)
#     db.session.add(tracker_link2)
#     db.session.add(tracker_link3)
#     db.session.commit()
#     return 'done!'
#
# @app.route('/debug/regen')
# def regen():
#     db.drop_all()
#     db.create_all()
#     return 'success!'
#
#
#     # todo тест каскадных удалений
#     from backend.src.model.mysql import User, Project, TrackerUserLink, Tracker
#
#     user1 = User(login='first', hash='hash', token='asdasdasd')
#     user2 = User(login='two', hash='hash', token='asdasd')
#     user3 = User(login='three', hash='hash', token='asdasdfd')
#     proj1 = Project(title='first2', code='frst')
#     proj2 = Project(title='two', code='two')
#     user2.projects.append(proj2)
#     user3.projects.append(proj1)
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.add(user3)
#
#     tracker = Tracker(title='title', code='code', ui_url='url', api_url='base')
#     link = TrackerUserLink(tracker=tracker, user=user1, external_user_id=1234)
#     db.session.add(link)
#
#     db.session.commit()
#     result = '<p>add</p>'
#     for user in User.query.all():
#         result += repr(user)
#     db.session.delete(user2)
#     db.session.commit()
#     return result
#
#
# @app.route('/test')
# def test():
#     token = request.cookies.get('token')
#     return jsonify(locals())


@app.route('/api/auth', methods=['POST'])
def auth():
    error = None

    def get(field):
        global error
        value = request.values.get(field)
        if value is None:
            error = 'введите' + field
        if field not in ('password', 'token'):
            return value.lower()
        return value

    login, password = get('login'), get('password')

    if error is not None:
        return jsonify({'message': error})

    api = ApiController()
    return api.get_user_by_redmine(login, password)

@app.route('/api/tasks')
@Auth.check_api_request
def get_tasks():
    now = dt.datetime.now().replace(second=0, microsecond=0)

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


@app.route('/api/user_projects')
@Auth.check_api_request
def get_user_projects():
    api = ApiController()
    return api.get_user_projects()


@app.route('/api/user_tags')
@Auth.check_api_request
def get_user_tags():
    api = ApiController()
    return api.get_user_tags()


@app.route('/api/trackerProjects')
@Auth.check_api_request
def get_tracker_projects():
    id = request.args.get('id')

    api = ApiController()
    return api.get_tracker_projects(id)


@app.route('/api/evoUsers')
@Auth.check_api_request
def get_evo_users():
    api = ApiController()
    return api.get_evo_users()


@app.route('/api/current')
@Auth.check_api_request
def get_current():
    if app.config.get('SQLITE'):
        dateFrom = dt.datetime.now().replace(second=0, microsecond=0)

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
    now = dt.datetime.now().replace(second=0, microsecond=0)

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
    description = request.values['description']
    if description == 'null':
        description = ''

    fact = {
        'id': request.values['id'],
        'name': request.values['name'],
        'category': request.values['category'],
        'date': request.values['date'],
        'start_time': request.values['start_time'],
        'end_time': request.values['end_time'],
        'description': description,
        'tags': [tag.strip() for tag in request.values['tags'].split(',')]
    }

    try:
        start_dt = dt.datetime.strptime(fact['date'] + ' ' + fact['start_time'], "%d.%m.%Y %H:%M")
    except ValueError:
        return jsonify({"status": False, "message": "Дата и время начала введены некорректно"})

    if len(fact['end_time']) < 5 or fact['end_time'] == '__:__':
        end_dt = None
    else:
        try:
            end_dt = dt.datetime.strptime(fact['date'] + ' ' + fact['end_time'], "%d.%m.%Y %H:%M")
        except ValueError:
            return jsonify({"status": False, "message": "Время окончания заполнено некорректно"})

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


@app.route('/api/linkProject', methods=['POST'])
@Auth.check_api_request
def link_project():
    project_id = int(request.values['projectId'])
    tracker_id = int(request.values['trackerId'])
    tracker_project_id = int(request.values['trackerProjectId'])
    tracker_project_title = request.values['trackerProjectTitle'].strip()

    api = ApiController()
    return api.link_project(project_id, tracker_id, tracker_project_id, tracker_project_title)


@app.route('/api/settings', methods=['GET'])
@Auth.check_api_request_readonly
def get_settings():
    api = ApiController()
    return api.get_settings()


@app.route('/api/settings', methods=['POST'])
@Auth.check_api_request
def save_settings():
    data = {
        'evo_in_name': request.values['evo_in_name'],
        'evo_in_comment': request.values['evo_in_comment'],
        'evo_out_name': request.values['evo_out_name'],
        'evo_out_comment': request.values['evo_out_comment'],
    }

    api = ApiController()
    return api.save_settings(data)


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


@app.route('/api/trackerTask', methods=['GET'])
@Auth.check_api_request_readonly
def tracker_task():
    tracker_id = int(request.values['trackerId'])
    task_id = int(request.values['taskId'])

    api = ApiController()
    return api.get_tracker_task(tracker_id, task_id)


@app.route('/api/version', methods=['GET'])
def version():
    client_version = None
    if 'version' in request.values:
        try:
            client_version = float(request.values['version'])
        except (ValueError):
            client_version = None

    changes = []

    # чтобы попросить пользователя обновить страницу, если релизятся правки по фронту (стили/скрипты)
    history = {
        0.10: "скрытие графиков, если в них нет данных",
        0.11: "уведомление пользователей при обновлении",
        0.12: "увеличен интервал проверки обновлений до 5 минут",
        0.14: "увеличен интервал проверки обновлений до 5 минут fix",
        0.15: "переключение символов [#@,] по shift+tab в обратную сторону, мелкие правки",
        0.16: "стилизация окна уведомления о новой версии",
        0.17: "кнопка обновления записей на странице истории",
    }

    current_version = 0.17  # подобное не работает на боевом нормально - list(history.keys())[-1]

    if client_version is not None and current_version > client_version:
        for v in history:
            if v > client_version:
                changes.append(history[v])

    return jsonify({"status": True, "version": current_version, "changes": changes})


@app.route('/api/task/export', methods=['POST'])
@Auth.check_api_request_readonly
def export_task():
    external_id = request.values['external_id']
    if external_id == '':
        external_id = 0
    else:
        external_id = int(external_id)

    api = ApiController()
    return api.export(request.values['tracker_id'], {
        'date': dt.datetime.strptime(request.values['date'], "%d.%m.%Y").date(),
        'hours': float(request.values['hours']),
        'comment': request.values['comment'],
        'name': request.values['name'],
        'external_id': external_id,
        'project_id': int(request.values['project_id']),
        'external_name': request.values['external_name']
    })


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)
