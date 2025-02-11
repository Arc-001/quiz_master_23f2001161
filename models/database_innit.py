from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date,DateTime, Table,Boolean
from sqlalchemy.orm import DeclarativeBase, relationship,backref,sessionmaker
from sqlalchemy.orm import Session
from datetime import datetime
import flask_login

engine = create_engine('sqlite:///main.db', echo=True)

class Base(DeclarativeBase):
    pass



class Subject(Base):
    __tablename__="subject"
    subject_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    Chapters = relationship("Chapter", back_populates="subject", cascade = "all, delete, delete-orphan")


class Chapter(Base):
    __tablename__="chapter"
    chapter_id = Column(Integer, primary_key=True)
    Subject_id = Column(Integer,ForeignKey('subject.subject_id'),nullable= False )
    name = Column(String, nullable=False)
    description = Column(String)
    subject = relationship("Subject", back_populates="Chapters")
    quizes = relationship("Quiz", back_populates="chapter", cascade = "all, delete, delete-orphan")

class Quiz(Base):
    __tablename__="quiz"
    quiz_id = Column(Integer, primary_key = True, autoincrement = True)
    chapter_id = Column(Integer, ForeignKey('chapter.chapter_id'))
    name = Column(String, nullable = False)
    description = Column(String)
    date_of_quiz = Column(Date, default = datetime.utcnow)
    time_duration = Column(String, default = "NA")
    remarks = Column(String, default = "NA")
    score = relationship("Score", back_populates="quiz", cascade="all, delete, delete-orphan")
    chapter = relationship("Chapter", back_populates="quizes")
    question = relationship("Question", back_populates="quiz", cascade = "all, delete, delete-orphan")

class Question(Base):
    __tablename__ = "question"
    question_id = Column(Integer, primary_key = True, autoincrement = True)
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    question_stmt = Column(String, nullable = False)
    quiz = relationship("Quiz", back_populates="question")
    option = relationship("Option", back_populates="question", cascade = "all, delete, delete-orphan")

class Option(Base):
    __tablename__="option"
    option_id = Column(Integer,primary_key= True,  autoincrement= True)
    question_id = Column(Integer, ForeignKey('question.question_id'), nullable = False)
    option_text = Column(String, nullable = False)
    is_correct = Column(Boolean, nullable = False, default = False)
    question = relationship("Question", back_populates="option")

class User(Base, flask_login.UserMixin):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable= False)
    username = Column(String, nullable= True)
    password = Column(String, nullable= False)
    qualification = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    is_admin = Column(Integer, default = '0', nullable=False)
    # def is_admin(self):
    #     if self.is_admin == 1:
    #         return True
    #     else:
    #         return False
    score = relationship("Score", back_populates="user", cascade = "all, delete, delete-orphan")
    attempt = relationship("Attempt", back_populates="user", cascade = "all, delete, delete-orphan")

class Score(Base):
    __tablename__ = "score"
    score_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"),nullable=False)
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"), nullable=False)
    attempt_id= Column(Integer, ForeignKey("attempt.attempt_id"), nullable=False)
    attempt_date_time = Column(DateTime)
    total_score = Column(Integer) 
    user = relationship("User", back_populates="score")
    quiz = relationship("Quiz", back_populates="score")
    attempt = relationship("Attempt", back_populates="score")

class Attempt(Base):
    __tablename__ = "attempt"
    user_id = Column(Integer, ForeignKey("user.user_id"))
    attempt_id = Column(Integer, primary_key=True)
    correct = Column(Integer)
    wrong_question_csv = Column(String)
    total_question = Column(Integer)
    score = relationship("Score", back_populates="attempt", cascade = "all, delete, delete-orphan")
    user = relationship("User", back_populates="attempt")



def db_innit():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    result = session.query(User).filter_by(username = "admin").first()
    if result == None:
        print("Creating default admin, username: admin, password: admin, Please change password after login")
        default_admin = User(full_name = "admin",email = 'admin@admin.in', username = "admin", password = "admin", is_admin = 1)
        session.add(default_admin)
        session.commit()
    session.close()
    print("Database created successfully")

def get_session():
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    return session

def close_session(session):
    session.close()



if __name__ == "__main__":
    print("Not to be run directly, call as module")
else:
    db_innit()
    print("Database created successfully")
 
