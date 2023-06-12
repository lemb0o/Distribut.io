# coding: utf-8
from flask import Flask, render_template
from tunnel_server import run_server


app = Flask(__name__, template_folder='.')


@app.route('/')
def index():
    return 200


@app.route('/unregister/<id>')
def index(id):
    return 200

@app.route('/register/<id>')
def index(id):
    return 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

