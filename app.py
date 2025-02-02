from models.database_innit import db_innit
from flask import Flask, render_template, request
from flask import redirect,request,url_for
from flask_login import LoginManager

#global login manager
login_manager = LoginManager()


app = Flask(__name__)

# #integrate login manager to 
# login_manager.init_app(app)

@app.route('/',methods = ['GET'])
def login():
    return render_template('index.html')

@app.route('/',methods = ['POST'])
def login_post():
    print (request.form)
    return redirect(url_for('login'))


app.run(debug = True)

