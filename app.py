# все импорты
import datetime as dt
from backend.lib.hamster.db import Storage
from backend.lib.hamster import Fact
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from backend.src.model.mysql import db
from backend.src.auth import Auth
from backend.src.controller import ApiController

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/regen')
def regen():
    # генератор тестовых данных
    from backend.src.model.mysql import Tracker, User, TrackerUserLink
    db.drop_all()
    db.create_all()
    tracker = Tracker(title='intaro redmine', code='redmine', api_url='https://redmine.skillum.ru', type='redmine')
    user = User(login='login', hash=Auth.get_hash('login', 'password', app.config.get('SALT')), token='MQinK4')
    user2 = User(login='login2', hash=Auth.get_hash('login2', 'password2', app.config.get('SALT')), token='MQinK42')
    db.session.add(user)
    db.session.add(user2)
    db.session.add(tracker)
    #подставь ниже api_key - при пересоздании таблиц проекты и задачи подтянутся в БД с редмайна
    tracker_link = TrackerUserLink(tracker=tracker, user=user, external_api_key='123456')
    tracker_link2 = TrackerUserLink(tracker=tracker, user=user2)
    db.session.add(tracker_link)
    db.session.add(tracker_link2)
    db.session.commit()

    from backend.src.sheduler import Sheduler
    s = Sheduler(Auth.get_user_by_token('MQinK4'))
    s.fetch_external_data()
    db.session.commit()


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

    user = {
        'login': Auth.get_user_by_login_and_hash(login, hash),
        'registration': Auth.add_new_user(login, hash)
    }[action]

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
@Auth.check_api_request
def get_current():
    dateFrom = dt.datetime.now()

    storage = Storage()
    last_entries = storage.get_formated_facts(dateFrom)

    for k, item in enumerate(last_entries):
        if item['end_time'] is '':
            return jsonify(item)

    return jsonify(None)


@app.route('/api/completitions')
@Auth.check_api_request
def complete_task():
    storage = Storage()
    return jsonify({"values": storage.get_suggestions()})


@app.route('/api/task', methods=['POST'])
@Auth.check_api_request
def add_entry():
    name = request.values.get('name').strip()
    api = ApiController()
    return api.add_activity(name)

    # storage = Storage()
    # result = storage.add_fact(request.values['name'])
    # return jsonify(result)


@app.route('/api/task/edit', methods=['POST'])
@Auth.check_api_request
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
@Auth.check_api_request
def stop_tracking():
    storage = Storage()
    result = storage.stop_tracking(dt.datetime.now())
    return jsonify(result)


@app.route('/api/task/stop', methods=['POST'])
@Auth.check_api_request
def stop_task():
    id = int(request.values['id'])
    storage = Storage()
    result = storage.touch_fact(id)

    return jsonify(result)


@app.route('/api/task/resume', methods=['POST'])
@Auth.check_api_request
def resume_task():
    id = int(request.values['id'])
    storage = Storage()
    result = storage.resume_fact(id)

    return jsonify(result)


@app.route('/api/task/delete', methods=['POST'])
@Auth.check_api_request
def delete_task():
    id = int(request.values['id'])
    storage = Storage()
    result = storage.remove_fact(id)

    return jsonify(result)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)
