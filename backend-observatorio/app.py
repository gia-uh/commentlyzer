import os
import sys
import click
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


app.run(host='0.0.0.0', port=8000, debug=True)