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


class Chapter(Base):
    __tablename__="chapter"
    chapter_id = Column(Integer, primary_key=True)
    Subject_id = Column(Integer, ForeignKey('subject.subject_id'))
    name = Column(String, nullable=False)
    description = Column(String)

class Quiz(Base):
    __tablename__="quiz"
    quiz_id = Column(Integer, primary_key = True, autoincrement = True)
    chapter_id = Column(Integer, ForeignKey('chapter.chapter_id'))
    name = Column(String, nullable = False)
    description = Column(String)
    date_of_quiz = Column(DateTime, default = datetime.utcnow)
    time_duration = Column(String, default = "NA")
    remarks = Column(String, default = "NA")
    question = relationship("Question", back_populates="quiz", cascade = "all, delete, delete-orphan")

class Question(Base):
    __tablename__ = "question"
    question_id = Column(Integer, primary_key = True, autoincrement = True)
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    question_stmt = Column(String, nullable = False)
    quiz = relationship("Quiz", back_populates="question")
    option = relationship("belongs_to", back_populates="question", cascade = "all, delete, delete-orphan")

class belongs_to(Base):
    __tablename__ = "belongs_to"
    question_id = Column(Integer, ForeignKey('question.question_id'), primary_key = True)
    option_id = Column(Integer, ForeignKey('option.option_id'), primary_key = True)
    question = relationship("Question", back_populates="belongs_to")
    option = relationship("Option", back_populates="belongs_to")


class Option(Base):
    __tablename__="option"
    option_id = Column(Integer,primary_key= True, nullable = False)
    option_text = Column(String, nullable = False)
    is_correct = Column(Boolean, nullable = False, default = False)

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
    user_id = Column(Integer, ForeignKey="user.user_id")
    quiz_id = Column(Integer, ForeignKey="quiz.quiz_id")
    attempt_id= Column(Integer, ForeignKey="attempt.attempt_id")
    attempt_date_time = Column(DateTime)
    total_score = Column(Integer)
    user = relationship("User", back_populates="score")
    attempt = relationship("Attempt", back_populates="score", cascade = "all, delete, delete-orphan")

class Attempt(Base):
    __tablename__ = "attempt"
    attempt_id = Column(Integer, primary_key=True)
    score_id = Column(Integer, ForeignKey = "score.score_id")
    correct = Column(Integer)
    wrong_question_csv = Column(String)
    total_question = Column(Integer)
    score = relationship("Score", back_populates="attempt")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
    
