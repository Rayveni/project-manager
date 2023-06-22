from flask import Flask,render_template,request,jsonify,g
from time import strftime,time
from .api import api_bp
from os import getenv
import logging
from logging.handlers import RotatingFileHandler

import traceback
#https://dev.to/rhymes/logging-flask-requests-with-colors-and-structure--7g1
#https://gist.github.com/alexaleluia12/e40f1dfa4ce598c2e958611f67d28966

logs_dir=getenv('app_logs')
app = Flask(__name__)
app.secret_key = 'random string'
app.static_folder = 'static'
app.config['JSON_AS_ASCII'] = False
app.template_folder='templates'

app.register_blueprint(api_bp,url_prefix='/api')

handler = RotatingFileHandler(f'{logs_dir}/app.log', maxBytes=100000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(handler)

@app.before_request
def start_timer():
    g.start = (strftime('[%Y-%b-%d %H:%M]:'),time())
    
@app.after_request
def after_request(response):
    if (request.path == "/favicon.ico" or ("static" in request.full_path)):
        return response
    timestamp_and_duration = g.start[0]+str(round(time() - g.start[1], 2))
    logger.error('%s %s %s %s %s %s', timestamp_and_duration, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    if (request.path == "/favicon.ico" or ("static" in request.full_path)):
        tb = traceback.format_exc()
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
        return e.status_code

@app.route("/", methods =["GET", "POST"])
def index_func():
    data={'title':'index'}
    return render_template('index.html',data=data)
  