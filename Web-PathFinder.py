from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to the PathFinder web service!'


if __name__ == '__main__':
    app.run()
