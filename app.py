from models.database_innit import *
from flask import Flask, render_template, request
from flask import redirect,request,url_for
import flask_login
from decorator import decorator
#global login managerW
login_manager = flask_login.LoginManager()


app = Flask(__name__)

app.secret_key = 'super secret string'

# class user(flask_login.UserMixin):
#     pass

@decorator
@flask_login.login_required
def check_admin(f, *args, **kwargs):
    session = get_session()
    print("We get :",flask_login.current_user.id)
    user = session.query(User).filter_by(email = flask_login.current_user.id).first()
    close_session(session)
    if user.is_admin == 1:
        return f(*args, **kwargs)
    else:
        return 'You are not admin'
    
@decorator
@flask_login.login_required
def redirect_admin(f, *args, ** kwargs):
    session = get_session()
    user = session.query(User).filter_by(email = flask_login.current_user.id).first()
    close_session(session)
    if user.is_admin == 1:
        return redirect(url_for("admin_home"))
    else:
        return f(*args, **kwargs)
    

@login_manager.user_loader
def user_loader(email):


    session = get_session()
    in_db = session.query(User).filter_by(email = email).first()
    close_session(session)


    if in_db:
        user_ = User()
        print (in_db)
        user_.id = email
        return user_
    else:
        return
    
@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')


    session = get_session()
    in_db = session.query(User).filter_by(username = email).first()
    close_session(session)

    if in_db:
        user_ = User()
        user_.id = email
        return user_
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
    in_db = session.query(User).filter_by(email = email).first()
    print (in_db)
    close_session(session)

    if in_db:
        if in_db.password == password:
            user_ = User()
            user_.id = email
            flask_login.login_user(user_)
            return redirect(url_for('home'))
    return 'Bad login'


@app.get('/home')
@flask_login.login_required
@redirect_admin
def home():
    return render_template('home.html', name = flask_login.current_user.id)



@app.get('/admin/home')
@flask_login.login_required
@check_admin
def admin_home():
    return render_template('admin.html')



@app.get('/admin/edit_users')
@flask_login.login_required
@check_admin
def admin_edit_user():
    session = get_session()
    Users_ = session.query(User).all()
    close_session(session)
    return render_template("edit_users.html", Users = Users_)




@app.get('/register')
def register_get():
    return render_template('register.html')

@app.post('/register')
def register_post():
    print(request.form)
    try:
        session = get_session()
        print('session created')
        in_db = session.query(User).filter_by(email = request.form['email']).first()
        print ('queried' + str(in_db))
        if in_db:
            return 'Email already exists'
        else:
            if (request.form['password'] == request.form['password_check']):
                print('password matched')
                new_user = User(
                    full_name = request.form['full_name'],
                    email = request.form['email'], 
                    qualification = request.form['qualification'] + ' | ' + request.form['qualification_info'], 
                    date_of_birth = datetime.strptime(request.form['DOB'], '%m/%d/%Y').date(), 
                    password = request.form['password'])
                print('new user created')
                session.add(new_user)
                print('new user added')
                session.commit()
                print('new user commited')
                session.close()
            else:
                return 'Password does not match'
            
    except Exception as e:
        raise e
        return 'internal server error',500
    finally:
        close_session(session)
    return redirect(url_for('success_reg'))
    
@app.get('/success_reg')
def success_reg():
    return render_template('success_reg.html')
        


@app.get('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("login_get"))


app.run(debug = True)

