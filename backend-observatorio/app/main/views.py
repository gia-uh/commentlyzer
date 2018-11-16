from . import main
from flask import send_file

@main.route('/')
def index():
    return 'caca'
    return send_file('static/index.html')
