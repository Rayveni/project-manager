from flask import Flask,render_template,request,jsonify
from .api import api_bp

app = Flask(__name__)
app.secret_key = 'random string'
app.static_folder = 'static'
app.config['JSON_AS_ASCII'] = False
app.template_folder='templates'
app.register_blueprint(api_bp,url_prefix='/api2')
@app.route("/", methods =["GET", "POST"])
def index_func():
    data={'title':'index'}
    task_param = request.form.get("task_param")
    task_param='None'
    data={'title':'index',
          'queue_count':11,
          'completed':2,          
          'task_param':task_param}
    return render_template('index.html',data=data)
   
  