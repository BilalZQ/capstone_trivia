"""Models module for trivia app."""

import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

os.environ['DB_HOST'] = ''
os.environ['DB_USER'] = ''
os.environ['DB_PASSWORD'] = ''

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'trivia')
TEST_DB_NAME = os.getenv('DB_NAME', 'trivia_test')

base_path = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/'

database_path = f"{base_path}{DB_NAME}"
test_database_path = f"{base_path}{TEST_DB_NAME}"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """
    Bind a flask application and a SQLAlchemy service.

    :param app:
    :param database_path:
    :return:
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    """Question Model."""

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        """
        Init method.

        :param question:
        :param answer:
        :param category:
        :param difficulty:
        """
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        """
        Insert question.

        :param self:
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Update question.

        :param self:
        :return:
        """
        db.session.commit()

    def delete(self):
        """
        Delete question.

        :param self:
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'question': self.question,
          'answer': self.answer,
          'category': self.category,
          'difficulty': self.difficulty
        }


class Category(db.Model):
    """Category Model."""

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        """
        Init method.

        :param self:
        :param type:
        """
        self.type = type

    def format(self):
        """
        Format method.

        :param self:
        :return:
        """
        return {
            'id': self.id,
            'type': self.type
        }
