__author__ = 'neil'

from Section5.src.app import app

app.run(debug=app.config['DEBUG'], port=4990)  # instead of __main__ in app

