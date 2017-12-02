# coding=utf-8
from os import environ
from src import app
# app.run(host='127.0.0.1', port=8080, debug=True)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '127.0.0.1')
    try:
        PORT = int(environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080

    app.run(HOST, PORT)
