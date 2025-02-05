from models.database_innit import *
from flask import Flask, render_template, request
from flask import redirect,request,url_for
import flask_login

#global login managerW
login_manager = flask_login.LoginManager()


app = Flask(__name__)

app.secret_key = 'super secret string'

class user(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):


    session = get_session()
    in_db = session.query(User).filter_by(username = email).first()
    close_session(session)


    if in_db:
        user_ = user()
        print (in_db)
        user.id = email
        return user
    else:
        return
    
@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')


    session = get_session()
    in_db = session.query(User).filter_by(username = email).first()
    close_session(session)

    if in_db:
        user_ = user()
        user.id = email
        return user
    else:
        return
    

        
    


# #integrate login manager to 
login_manager.init_app(app)

@app.get('/')
def login_get():
    return render_template('index.html')

@app.post('/')
def login_post():
    print (request.form)
    email = request.form['email']
    password = request.form['password']
    
    session = get_session()
    print (email)
    in_db = session.query(User).filter_by(username = email).first()
    print (in_db)
    close_session(session)

    if in_db:
        if in_db.password == password:
            user_ = user()
            user.id = email
            flask_login.login_user(user_)
            return redirect(url_for('protected'))
    return 'Bad login'


@app.get('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.get('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out'


app.run(debug = True)

