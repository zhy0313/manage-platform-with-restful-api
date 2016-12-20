# *-* coding:utf-8 *-*
'''
@author: ioiogoo
@date: 2016/12/14 13:35
'''
import logging

from flask import Flask, render_template
from flask_restful import Api

from config import config
from api import *

app = Flask(__name__)
api = Api(app)
app.config.from_object(config['defaultConfig'])


api.add_resource(getAttribute, '/api/getAttribute')
api.add_resource(deleteAttribute, '/api/deleteAttribute')
api.add_resource(addAttribute, '/api/addAttribute')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')