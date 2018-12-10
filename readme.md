# Install and run

## Backend

git clone https://github.com/positron48/pyVueTracker.git

cd pyVueTracker/backend

virtualenv venv

source venv/bin/activate

pip3 install -r requirements.txt

cd ..

edit config.py

flask run

developer_mode: sh start_dev.sh

## Frontend

cd frontend

npm install

### dev

npm run dev

### prod

npm run build