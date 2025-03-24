from models.database_innit import *
from flask import Blueprint, jsonify


api = Blueprint("API", __name__)

@api.get("/subjects/all")
def get_subjects():
    session = get_session()
    subjects  =session.query(Subject).all()
    dic_subject = {}
    for subject in subjects:
        dic_subject[subject.subject_id] = {"subject name":subject.name, "subject id":subject.subject_id}
    return jsonify(dic_subject)

@api.get("/subjects/<int:subject_id>/chapters")
def get_chapters(subject_id):
    session = get_session()
    chapters =session.query(Chapter).filter_by(Subject_id = subject_id).all()
    dic_chapters ={}
    for chapter in chapters:
        dic_chapters[chapter.chapter_id] = {
            "chapter name": chapter.name,
            "chapter id": chapter.chapter_id
            }
    return jsonify(dic_chapters)

@api.get("/chapters/<int:chapter_id>/quizzes_data")
def get_quizes(chapter_id):
    session = get_session()
    quizes = session.query(Quiz).filter_by(chapter_id = chapter_id).all()
    dic_quizes = {}
    for quiz in quizes:
        dic_quizes[quiz.quiz_id] = {
            "quiz title":quiz.name, 
            "quiz id":quiz.quiz_id, 
            "quiz duration": quiz.time_duration, 
            "quiz remarks": quiz.remarks
            }
    return jsonify(dic_quizes)

@api.get("/quiz/<int:quiz_id>/questions")
def get_questions(quiz_id):
    session = get_session()
    questions = session.query(Question).filter_by(quiz_id = quiz_id).all()
    dic_questions = {}
    for question in questions:
        dic_questions[f"{question.question_id}"] = {"question": question.question_stmt, "correct answer": None}
        for option in question.option:
            if option.is_correct:
                dic_questions[f"{question.question_id}"]["correct answer"] = option.option_text
    return jsonify(dic_questions)

@api.get("/attempt/<int:attempt_id>/details")
def get_attempt_details(attempt_id):
    session = get_session()
    attempt = session.query(Attempt).filter_by(attempt_id = attempt_id).first()
    user = attempt.user
    attempt_dict = {
        "Attempter name": user.full_name,
        "Attempter email": user.email,
        "Attempter id": user.user_id,
        "Attempt date": attempt.attempt_date_time,
        "Total questions": attempt.total_question,
        "Marks": attempt.correct,
        "Wrong answers": attempt.wrong_question_answer_json
    }
    return jsonify(attempt_dict)


def init_api(app):
    app.register_blueprint(api, url_prefix="/api")
    return

