from flask import Flask
from ProxyPool.db import db_client

app = Flask('__init__')


@app.route("/")
def hello():
    return 'hello world'


@app.route("/get")
def get():
    return db_client.get()


if __name__ == '__main__':
    app.run()

