from models.database_innit import *
from flask import Flask, render_template, request
from flask import redirect,request,url_for
import flask_login
from decorator import decorator
#global login managerW
login_manager = flask_login.LoginManager()


app = Flask(__name__)

app.secret_key = 'super secret string'


#-----------------------login_innit-------------------------


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


# class user(flask_login.UserMixin):
#     pass




#----------------Helper Functions-------------------#


def register(form_):
    '''
    
    Takes a form and registers a new user in the database.
    
    '''
    try:
        session = get_session()
        new_user = User(
                    full_name = form_['full_name'],
                    email = form_['email'], 
                    username = form_['username'],
                    qualification = form_['qualification'] + ' | ' + request.form['qualification_info'], 
                    date_of_birth = datetime.strptime(form_['DOB'], '%m/%d/%Y').date(), 
                    password = form_['password']
        )
        session.add(new_user)
        session.commit()
    except:
        return False
    finally:
        close_session(session)
    return True

#----------------------Role Management--------------------------

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
    



#---------------------Login Routes (/)------------------

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


#----------------------Admin--------------


# admin home 

@app.get('/admin/home')
@flask_login.login_required
@check_admin
def admin_home():
    return render_template('admin.html')



# admin edit users

@app.get('/admin/edit_user')
@flask_login.login_required
@check_admin
def admin_edit_user():
    session = get_session()
    Users_ = session.query(User).all()
    close_session(session)
    return render_template("edit_users.html", Users = Users_)



@app.post('/admin/edit_user/edit')
@flask_login.login_required
@check_admin
def edit_user():
    try:
        session = get_session()
        print(request.form)
        user_ = session.query(User).filter_by(user_id = request.form["user_id"]).first()
        print(user_.user_id)
        user_.full_name = request.form['full_name']
        print(1)
        user_.username = request.form['username']
        print(2)
        user_.email = request.form['email']
        print(3)
        user_.password = request.form['password']
        print(4)
        user_.date_of_birth = datetime.strptime(request.form['DOB'], '%m/%d/%Y').date()
        print(5)
        user_.qualification = request.form['qualification_info']
        print(6)
        session.commit()
        print(7)
        return redirect(url_for('admin_edit_user'))
    except:
        return 'Internal server error', 500
    finally:
        close_session(session)


@app.get('/admin/edit_user/delete/<int:user_id>')
@flask_login.login_required
@check_admin
def delete_user(user_id):
    try:    
        session = get_session()
        user_ = session.query(User).filter_by(user_id = user_id).first()
        session.delete(user_)
        session.commit()
        return redirect(url_for('admin_edit_user'))
    except:
        return 'Internal server error', 500
    finally:
        close_session(session)


@app.post("/admin/edit_user/add_user")
@flask_login.login_required
@check_admin
def add_user():
    session = get_session()
    in_db = session.query(User).filter_by(email = request.form['email']).first()
    if in_db:
        return '<a href = "/admin/edit_user">Email already exists</a>'
    close_session(session)
    print(request.form)
    if register(request.form):
        return redirect(url_for("admin_edit_user"))
    else:
        return 'Internal server error', 500



#admin subject

@app.get("/admin/subjects")
@flask_login.login_required
@check_admin
def admin_subjects():
    # try:
    session = get_session()
    subjects = session.query(Subject).all()
    return render_template("edit_subjects.html", subjects = subjects)
    # except:
    #     return 'Internal server error', 500
    # finally:
    #     close_session(session)

@app.get("/admin/subject/delete/<int:subject_id>")
@flask_login.login_required
@check_admin
def del_subject(subject_id):
    session = get_session()
    print(1)
    subject = session.query(Subject).filter_by(subject_id = subject_id).first()
    print(subject.subject_id)
    print(2)
    session.delete(subject)
    print(3)
    session.commit()
    session.close()
    print(4)
    return redirect(url_for("admin_subjects"))


#register
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
        close_session(session)
        if in_db:
            return 'Email already exists'
        else:
            if (request.form['password'] == request.form['password_check']):
                print('password matched')
                if (register(request.form)):
                    return redirect(url_for('success_reg'))
                else:
                    raise e
            else:
                return 'Password does not match'
            
    except Exception as e:
        return 'internal server error',500

    
@app.get('/success_reg')
def success_reg():
    return render_template('success_reg.html')
        

@app.get('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login_get'))


app.run(debug = True)

