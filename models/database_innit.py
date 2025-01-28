from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table,Boolean
from sqlalchemy.orm import DeclarativeBase, relationship,backref,sessionmaker
from datetime import datetime

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
    date_of_quiz = Column(DateTime, default = datetime.utcnow)
    time_duration = Column(String, default = "NA")
    remarks = Column(String, default = "NA")
    chapter = relationship("Chapter", back_populates="quizes")
    subject  = relationship("Subject", back_populates="Chapters")
    question = relationship("Question", back_populates="quiz", cascade = "all, delete, delete-orphan")

class Question(Base):
    __tablename__ = "question"
    question_id = Column(Integer, primary_key = True, autoincrement = True)
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    question_stmt = Column(String, nullable = False)
    quiz = relationship("Quiz", back_populates="question")
    chapter = relationship("Chapter", back_populates="quizes")
    subject = relationship("Subject", back_populates="Chapters")
    option = relationship("belongs_to", back_populates="question", cascade = "all, delete, delete-orphan")

class Option(Base):
    __tablename__="option"
    option_id = Column(Integer,primary_key= True,  autoincrement= True)
    question_id = Column(Integer, ForeignKey('question.question_id'), nullable = False)
    option_text = Column(String, nullable = False)
    is_correct = Column(Boolean, nullable = False, default = False)
    question = relationship("Question", back_populates="option")

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable= False)
    password = Column(String, nullable= False)
    qualification = Column(String)
    date_of_birth = Column(DateTime)
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
    attempt = relationship("Attempt", back_populates="score", cascade = "all, delete, delete-orphan")

class Attempt(Base):
    __tablename__ = "attempt"
    user_id = Column(Integer, ForeignKey("user.user_id"))
    attempt_id = Column(Integer, primary_key=True)
    score_id = Column(Integer, ForeignKey("score.score_id"))
    correct = Column(Integer)
    wrong_question_csv = Column(String)
    total_question = Column(Integer)
    score = relationship("Score", back_populates="attempt")
    user = relationship("User", back_populates="attempt")

def db_innit():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
