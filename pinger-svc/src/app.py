# -*- coding: utf-8 -*-

# Python

# Flask 

# App
from config import app
from routes import *

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )