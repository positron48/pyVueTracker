# Изменения

##### 2019.01.06
* В качестве логина/пароля теперь нужно использовать данные аккаунта в редмайн
* Название страницы в браузере теперь - "чч:мм название задачи"


# Install and run

## Backend

git clone https://github.com/positron48/pyVueTracker.git

cd pyVueTracker/backend

virtualenv venv

source venv/bin/activate

pip3 install -U -r requirements.txt

cd ..

cp config.py.dist config.py
edit config.py

flask db upgrade

flask run

developer_mode: sh start_dev.sh

## Frontend

cd frontend

npm install

### dev

npm run dev

### prod

npm run build

Для развертывания сервера:
* git clone
* установить зависимости: cd frontend && npm install (или yarn install)
* собрать фронт: cd frontend && npm run build (или yarn build)
* войти в виртуальное окружение:  cd backend && virtualenv venv && source venv/bin/activate
* установить зависимости: cd backend && pip3 install -U -r requirements.txt
* отредактировать путь к БД в config.py
* создать БД без таблиц внешним инструментом
* накатить миграции: flask db upgrade
* запустить сервер: cd backend && flask run
Node.js используется только для сборки фронта, сервер - питон

## Виджеты

Unix - https://github.com/positron48/pyTimeUnixWidget
* конфиг в ini-файле (хост, токен), ini нужно скопировать с dist, подставив свои данные
* отображает название и продолжительность текущей задачи в трее с обновлением каждые 5 секунд