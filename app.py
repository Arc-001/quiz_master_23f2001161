from models.database_innit import *
from flask import Flask, render_template, request,send_file
from flask import redirect,request,url_for
import flask_login
from decorator import decorator
import matplotlib.pyplot
import matplotlib
import io
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import random
from werkzeug.security import generate_password_hash, check_password_hash
from api import *

#global login managerW
login_manager = flask_login.LoginManager()


app = Flask(__name__)

app.secret_key = 'This is something I should probably use a random string for but mhy typos are random enough XDD'
init_api(app)

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
                    date_of_birth = datetime.strptime(form_['DOB'],'%Y-%m-%d').date(), 
                    password = generate_password_hash(form_['password'])
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
    
def gen_pi_plot(correct, wrong, missing):
    labels = ['Correct', 'Wrong', 'Missing']
    sizes = [correct, wrong, missing]
    colors = ['#4CAF50', '#FF5252','#808080']
    explode = (0.15, 0, 0)
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors)
    plt.title('Quiz Result')
    img = io.BytesIO()
    plt.savefig(img,format='png')
    img.seek(0)
    return img

@app.get("/user/<int:quiz_id>/<int:attempt_id>/get_pi_fig")
@flask_login.login_required
def get_result_chart(quiz_id, attempt_id):
    session = get_session()
    attempt = session.query(Attempt).filter_by(attempt_id = attempt_id).first()
    right = attempt.correct
    print(len(eval(attempt.wrong_question_answer_json)))
    wrong = len(eval(attempt.wrong_question_answer_json))
    missing = len(eval(attempt.missed_question_json))
    plt = gen_pi_plot(right,wrong,missing)
    return send_file(plt,mimetype="png")


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
        if check_password_hash(in_db.password, password):
            user_ = User()
            user_.id = email
            flask_login.login_user(user_)
            return redirect(url_for('home'))
    return 'Bad login'




##########################################################
#                                                        #
# ------------------------USER SIDE----------------------#
#                                                        #
##########################################################



@app.get('/home')
@flask_login.login_required
@redirect_admin
def home():
    session = get_session()
    subjects = session.query(Subject).all()
    # subject_id -> [date(next deadline), next_quiz_name]
    quiz_list = {}
    for subject in subjects:
        temp = []
        for chapter in subject.Chapters:
            for quiz in chapter.quizes:
                if quiz.date_of_quiz >= ((datetime.now()).date()):
                    temp.append((quiz.date_of_quiz, quiz.name))
        
        quiz_list[subject.subject_id] = min(temp, key = lambda x: x[0]) if temp else None
                
    close_session(session)
    return render_template('home.html', name = flask_login.current_user.id, subjects = subjects, next_quiz_map = quiz_list)


@app.get('/user/<int:subject_id>')
@flask_login.login_required
@redirect_admin
def user_chapters(subject_id):
    session = get_session()
    chapters = session.query(Chapter).filter_by(Subject_id = subject_id).all()
    quiz_list = {}
    for chapter in chapters:
        temp = []
        for quiz in chapter.quizes:
            if quiz.date_of_quiz >=((datetime.now()).date()):
                temp.append((quiz.date_of_quiz, quiz.name))
        
        quiz_list[chapter.chapter_id] = min(temp, key= lambda x:x[0]) if temp else None
    
    close_session(session)
    return render_template('user_chapters.html', name = flask_login.current_user.id, chapters = chapters, subject_id = subject_id, next_quiz_map = quiz_list)

@app.get('/user/<int:subject_id>/<int:chapter_id>')
@flask_login.login_required
@redirect_admin
def user_quiz(subject_id, chapter_id):
    session = get_session()
    quizzes = session.query(Quiz).filter_by(chapter_id = chapter_id).all()
    close_session(session)
    date_now = datetime.now().date()
    return render_template(
        'user_quizes.html',
        name = flask_login.current_user.id, 
        quizzes = quizzes, 
        subject_id = subject_id, 
        chapter_id = chapter_id,
        date_now = date_now)

@app.get('/user/<int:subject_id>/<int:chapter_id>/<int:quiz_id>')
@flask_login.login_required
@redirect_admin
def quiz_test(subject_id, chapter_id, quiz_id):
    session = get_session()
    quiz = session.query(Quiz).filter_by(quiz_id = quiz_id).first()
    user_id = flask_login.current_user.id
    options = {}
    for question in quiz.question:
        options_ = question.option
        options[question.question_id] = [(option.option_id, option.option_text ) for option in options_]
    for qid in options:
        random.shuffle(options[qid])
    return render_template("user_quiz.html", quiz = quiz, subject_id = subject_id, chapter_id = chapter_id, quiz_id = quiz_id,submiter = user_id, options = options)


@app.post('/user/<int:subject_id>/<int:chapter_id>/<int:quiz_id>')
@flask_login.login_required
@redirect_admin
def quiz_transcript_eval(subject_id,chapter_id,quiz_id):
    # dic question id <int> -> option id <int>
    transcript = request.form
    print(f'{request.form['user_email']}')
    session = get_session()
    quiz = session.query(Quiz).filter_by(quiz_id = quiz_id).first()
    correct_count = 0
    total_count = 0
    correct_question_option = {}
    wrong_question_list = {}

    for question in quiz.question:
        total_count+=1
        for option in question.option:
            if option.is_correct:
                correct_question_option[question.question_id] = option.option_id
    
    for qid in transcript:
        if qid == "user_email":
            continue
        try:
            if str(transcript[qid]) == str(correct_question_option[int(qid)]):
                correct_count+=1
            else:
                wrong_question_list[qid]=(str(transcript[qid]),str(correct_question_option[int(qid)]))
        except:
            continue
    
    all_qids = [str(question.question_id) for question in quiz.question]
    missed_qids = [qid  for qid in all_qids if qid not in transcript.keys()]
    missed_correct_dict = {}
    for missed_qid in missed_qids:
        missed_correct_dict[missed_qid] = str(correct_question_option[int(missed_qid)])
    

    email = flask_login.current_user.id
    user = session.query(User).filter_by(email = email).first()
    user_id = user.user_id

    attempt = Attempt()
    attempt.attempt_date_time = datetime.now()
    attempt.user_id = user_id
    attempt.quiz_id = quiz_id
    attempt.correct = correct_count
    attempt.total_question = total_count
    attempt.wrong_question_answer_json = str(wrong_question_list)
    attempt.missed_question_json = str(missed_correct_dict)
    session.add(attempt)
    session.commit()
    attempt_id = attempt.attempt_id
    close_session(session)
    return redirect(f'/user/{subject_id}/{chapter_id}/{quiz_id}/{attempt_id}/result')
    
@app.get("/user/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:attempt_id>/result")
@flask_login.login_required
def quiz_result(subject_id,chapter_id, quiz_id, attempt_id):
    session = get_session()
    attempt = session.query(Attempt).filter_by(attempt_id = attempt_id).first()
    quiz = session.query(Quiz).filter_by(quiz_id = quiz_id).first()
    wrong_question_opt = eval(f'{attempt.wrong_question_answer_json}')
    missing_question_opt = eval(f'{attempt.missed_question_json}')
    wrong_question_statement = {}
    #note we get {qid ->[ wrong_id,correct_id]}
    # this does the wrong_question_opt -> wrong_question_statement conversion
    for qid in wrong_question_opt:
        question = session.query(Question).filter_by(question_id = qid).first()
        wrong_option = session.query(Option).filter_by(option_id = wrong_question_opt[qid][0]).first()
        correct_option = session.query(Option).filter_by(option_id = wrong_question_opt[qid][1]).first()
        wrong_question_statement[question.question_stmt] = [wrong_option.option_text, correct_option.option_text]
    '''
    {wrong_question_statement -> [answered_option_statement,correct_option_statement]} 
    '''
    missing_question_statement = {}
    for qid in missing_question_opt:
        question = session.query(Question).filter_by(question_id = int(qid)).first()
        option = session.query(Option).filter_by(option_id = int(missing_question_opt[qid])).first()
        missing_question_statement[question.question_stmt] = option.option_text

    return render_template(
    'user_quiz_end_landing.html',
    attempt_id = attempt_id,
    quiz_id = quiz_id,
    questions = wrong_question_statement,
    missing = missing_question_statement
    )

@app.get("/user/result")
@flask_login.login_required
def get_result_home():
    session  = get_session()
    subjects = session.query(Subject).all()
    user = session.query(User).filter_by(email = flask_login.current_user.id).first()
    close_session(session)
    return render_template("user_result_subjects.html",subjects = subjects, name = user.username)



@app.get("/user/<int:subject_id>/result")
@flask_login.login_required
def get_result_chapters(subject_id):
    session = get_session()
    chapters = session.query(Chapter).filter_by(Subject_id = subject_id).all()
    user = session.query(User).filter_by(email = flask_login.current_user.id).first()
    return render_template("user_result_chapters.html",name = user.username, chapters = chapters, subject_id = subject_id)


@app.get("/user/<int:subject_id>/<int:chapter_id>/result")
@flask_login.login_required
def get_result_quizzes(subject_id,chapter_id):
    session = get_session()
    quiz = session.query(Quiz).filter_by(chapter_id = chapter_id).all()
    user = session.query(User).filter_by(email = flask_login.current_user.id).first()
    attempts = user.attempt
    marks_lst = []
    for attempt in attempts:
        marks_lst.append(attempt.correct)
    

    return render_template(
        "user_result_quiz.html",
        name = user.username, 
        subject_id = subject_id, 
        chapter_id = chapter_id, 
        quizzes = quiz,
        user_attempts = attempts,
        marks = marks_lst
        )
    


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
        user_.username = request.form['username']
        user_.email = request.form['email']
        if request.form['password'] != user_.password:
            user_.password = generate_password_hash(request.form['password'])
        user_.date_of_birth = datetime.strptime(str(request.form['DOB']), '%Y-%m-%d').date()
        user_.qualification = request.form['qualification_info']
        session.commit()
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
    subject = session.query(Subject).filter_by(subject_id = subject_id).first()
    print(subject.subject_id)
    session.delete(subject)
    session.commit()
    session.close()
    return redirect(url_for("admin_subjects"))

@app.post("/admin/subject/edit")
@flask_login.login_required
@check_admin
def edit_subject():
    print(request.form)
    session = get_session()
    subject = session.query(Subject).filter_by(subject_id = request.form['subject_id']).first()
    if subject:
        subject.name = request.form['subject_name']
        subject.description = request.form['subject_description']
    session.commit()
    close_session(session)
    return redirect(url_for("admin_subjects"))

@app.post("/admin/subject/add")
@flask_login.login_required
@check_admin
def add_subject():
    print(request.form)
    session = get_session()
    subject = Subject()
    subject.name = request.form["subject_name"]
    subject.description = request.form["subject_description"]
    session.add(subject)
    session.commit()
    return redirect(url_for("admin_subjects"))



#admin chapters


@app.get("/admin/<int:subject_id>")
@flask_login.login_required
@check_admin
def admin_chapter(subject_id):
    session = get_session()
    chapters = session.query(Chapter).filter_by(Subject_id = str(subject_id)).all()
    subject = session.query(Subject).filter_by(subject_id = str(subject_id)).first()
    subject_name = subject.name
    close_session(session)
    print(subject_id)
    return render_template("edit_chapters.html",chapters = chapters, subject_id = subject_id, subject_name = subject_name)

@app.post("/admin/<int:subject_id>/add")
@flask_login.login_required
@check_admin
def add_chapter(subject_id):
    print(f"--------------------{subject_id}---------------")
    session = get_session()
    chapter = Chapter()
    chapter.Subject_id=subject_id
    chapter.name = request.form["chapter_name"]
    chapter.description = request.form["chapter_description"]
    session.add(chapter)
    session.commit()
    return redirect(f'/admin/{subject_id}')

@app.get("/admin/<int:subject_id>/<int:chapter_id>/delete")
@flask_login.login_required
@check_admin
def delete_chapter(subject_id,chapter_id):
    session = get_session()
    chapter = session.query(Chapter).filter_by(chapter_id=chapter_id).first()
    session.delete(chapter)
    session.commit()
    close_session(session)
    return redirect(f"/admin/{subject_id}")

@app.post("/admin/chapter/edit")
@flask_login.login_required
@check_admin
def edit_chapter():
    session = get_session()
    chapter = session.query(Chapter).filter_by(chapter_id = request.form["chapter_id"]).first()
    subject_id = chapter.Subject_id
    chapter.name = request.form["chapter_name"]
    chapter.description=request.form["chapter_description"]
    session.commit()
    close_session(session)
    return redirect(f"/admin/{subject_id}")




#admin Quiz edit



@app.get("/admin/<int:subject_id>/<int:chapter_id>")
@flask_login.login_required
@check_admin
def admin_quiz(subject_id,chapter_id):
    session = get_session()
    quizzes = session.query(Quiz).filter_by(chapter_id = chapter_id).all()
    close_session(session)
    return render_template('edit_quizzes.html', quizzes = quizzes, subject_id = subject_id , chapter_id = chapter_id )


@app.post("/admin/<int:subject_id>/<int:chapter_id>/quiz/add")
@flask_login.login_required
@check_admin
def admin_add_quiz(subject_id, chapter_id):
    try:
        session = get_session()
        quiz = Quiz()
        quiz.chapter_id = chapter_id
        quiz.name = request.form["quiz_name"]
        quiz.description = request.form["quiz_description"]
        quiz.date_of_quiz = datetime.strptime(request.form["date_of_quiz"],'%Y-%m-%d').date()
        quiz.remarks = request.form["remarks"]
        quiz.time_duration = request.form["time_duration"]
        session.add(quiz)
        session.commit()
        return redirect(f'/admin/{subject_id}/{chapter_id}')
    except:
        return 'Internal server error', 500
    finally:
        close_session(session)


@app.get("/admin/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/delete")
@flask_login.login_required
@check_admin
def admin_delete_quiz(subject_id, chapter_id, quiz_id):
    try:
        session = get_session()
        quiz = session.query(Quiz).filter_by(quiz_id = quiz_id).first()
        session.delete(quiz)
        session.commit()
        return redirect(f'/admin/{subject_id}/{chapter_id}')
    except:
        return 'Internal server error', 500
    finally:
        close_session(session)



@app.post("/admin/<int:subject_id>/<int:chapter_id>/edit")
@flask_login.login_required
@check_admin
def admin_edit_quiz(subject_id, chapter_id):
    try:
        session = get_session()
        quiz = session.query(Quiz).filter_by(quiz_id = request.form["quiz_id"]).first()
        quiz.name = request.form["quiz_name"]
        quiz.description = request.form["quiz_description"]
        quiz.date_of_quiz = datetime.strptime(request.form["date_of_quiz"],'%Y-%m-%d').date()
        quiz.remarks = request.form["remarks"]
        quiz.time_duration = request.form["time_duration"]
        session.commit()
        return redirect(f'/admin/{subject_id}/{chapter_id}')
    except:
        return 'Internal server error', 500
    finally:
        close_session(session)


#---------------------Admin Questions / Quiz--------------------

@app.get("/admin/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/questions")
@flask_login.login_required
@check_admin
def admin_questions(subject_id, chapter_id, quiz_id):
    session = get_session()
    questions = session.query(Question).filter_by(quiz_id = quiz_id).all()
    options = session.query(Option).filter_by(quiz_id = quiz_id).all()
    question_options = {}
    for question in questions:
        question_options[question] = []
        for option in options:
            if option.question_id == question.question_id:
                question_options[question].append(option)
    close_session(session)
    return render_template("admin_add_edit_quiz.html", questions = questions, options = options, question_options = question_options, subject_id = subject_id, chapter_id = chapter_id, quiz_id = quiz_id)

@app.post("/admin/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/add")
@flask_login.login_required
@check_admin
def add_question_redirect(subject_id, chapter_id, quiz_id):
    no_of_options = request.form["no_of_options"]
    session = get_session()
    question = Question()
    question.question_stmt = request.form["question_stmt"]
    question.quiz_id = quiz_id
    session.add(question)
    session.commit()
    for i in range(int(no_of_options)-1):
        opt = Option()
        opt.option_text = "placeholder-wrong"
        opt.is_correct = 0
        opt.question_id = question.question_id
        opt.quiz_id = quiz_id
        session.add(opt)
    opt = Option()
    opt.option_text = "placeholder-correct"
    opt.is_correct = 1
    opt.quiz_id = quiz_id
    opt.question_id = question.question_id
    session.add(opt)
    session.commit()
    
    question_id = question.question_id
    close_session(session)

    return redirect(f'/admin/{subject_id}/{chapter_id}/{quiz_id}/{question_id}/edit')

@app.get("/admin/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>/edit")
@flask_login.login_required
@check_admin
def edit_question(subject_id, chapter_id, quiz_id, question_id):
    session = get_session()
    question = session.query(Question).filter_by(question_id = question_id).first()
    options = question.option
    close_session(session)
    try:
        no_of_options = request.args.get('options')
    except:
        no_of_options = -1
    return render_template("admin_edit_question.html",question = question, options = options, subject_id = subject_id, chapter_id = chapter_id, quiz_id = quiz_id, no_of_options = no_of_options)

@app.post("/admin/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>/edit")
@flask_login.login_required
@check_admin
def edit_question_post(subject_id, chapter_id, quiz_id, question_id):
    session = get_session()
    question = session.query(Question).filter_by(question_id = question_id).first()
    options = question.option
    question.question_stmt = request.form["question_stmt"]
    for option in options:
        option.option_text = request.form[f"{option.option_id}"]
    session.commit()
    close_session(session)
    return redirect(f'/admin/{subject_id}/{chapter_id}/{quiz_id}/questions')


@app.get("/admin/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>/delete")
@flask_login.login_required
@check_admin
def delete_question(subject_id, chapter_id, quiz_id, question_id):
    session = get_session()
    question = session.query(Question).filter_by(question_id = question_id).first()
    session.delete(question) #can be done as on cascade is declared in model so options are deleted automatically
    session.commit()
    close_session(session)
    return redirect(f'/admin/{subject_id}/{chapter_id}/{quiz_id}/questions')


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
                    return redirect(url_for('login_get'))
                else:
                    raise e
            else:
                return 'Password does not match'
            
    except Exception as e:
        return 'internal server error',500

    
        

@app.get('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login_get'))


app.run(debug = True)

