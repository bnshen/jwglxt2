from flask import Flask,render_template,request,redirect,url_for,jsonify


from auths import Auth
from flask_cors import *

app = Flask(__name__)



CORS(app, supports_credentials=True)        #跨域请求

from views.Student import Student as Student_blueprint
app.register_blueprint(Student_blueprint,url_prefix='/Student')

from views.OpenC import C as C_blueprint
app.register_blueprint(C_blueprint,url_prefix='/OpenC')

from views.Admin import Admin as Admin_blueprint
app.register_blueprint(Admin_blueprint,url_prefix='/Admin')

from views.Public import Public as Public_blueprint
app.register_blueprint(Public_blueprint,url_prefix='/Public')

from views.Teacher import Teacher as Teacher_blueprint
app.register_blueprint(Teacher_blueprint,url_prefix='/Teacher')

from exts import start_job

import threading,time

def wakeup():
    while 1:
        start_job()
        time.sleep(60*30)


t=threading.Thread(target=wakeup)
t.start()

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        _data = request.get_json()
        user_name=_data.get("user_name","")
        password=_data.get("password","")
        return jsonify(Auth.authenticate(Auth, user_name, password))
    else:
        return render_template("login.html")

@app.route('/identify')
def identify():
    print(Auth.identify(Auth,request))
    return "6666"


if __name__ == '__main__':
    app.run(debug=True)
