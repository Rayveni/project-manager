from flask import Flask,render_template,request,jsonify
from .api import api_bp

app = Flask(__name__)
app.secret_key = 'random string'
app.static_folder = 'static'
app.config['JSON_AS_ASCII'] = False
app.template_folder='templates'
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(api_bp,url_prefix='/api')

@app.route("/", methods =["GET", "POST"])
def index_func():
    data={'title':'index'}
    return render_template('index.html',data=data)
   
  