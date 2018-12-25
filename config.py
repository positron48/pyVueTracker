from hashlib import sha256
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:querystring@localhost/pyvue'
DEBUG = True
SALT = sha256('qjvFNjCrziBTcoYiIxweneVpqDIbQrk'.encode()).hexdigest().encode()
