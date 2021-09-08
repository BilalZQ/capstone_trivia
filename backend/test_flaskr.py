"""Module for unit tests of trivia app."""

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, test_database_path
from constants import HTTP_STATUS, ERROR_MESSAGES


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = test_database_path
        setup_db(self.app, self.database_path)

        self.test_category = 1
        self.test_question = {
            "question": "TestQ",
            "answer": "TestA",
            "category": self.test_category,
            "difficulty": 1
        }
        self.quiz_data = {
            'quiz_category': {'id': 1},
            'previous_questions': []
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """
        Executed after reach test.

        :param self:
        :return:
        """
        pass

    def test_get_categories_successfully(self):
        """
        Test case to get all categories successfully.

        :param self:
        :return:
        """
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.OK)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('categories')))

    def test_get_categories_with_invalid_method(self):
        """
        Test case to get categories with invalid method.

        :param self:
        :return:
        """
        response = self.client().post('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.METHOD_NOT_ALLOWED)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.METHOD_NOT_ALLOWED]
        )

    def test_get_questions_successfully(self):
        """
        Test case to get questions successfully.

        :param self:
        :return:
        """
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.OK)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('questions')))
        self.assertTrue(len(data.get('categories')))
        self.assertTrue(data.get('total_questions'))

    def test_get_questions_with_invalid_page(self):
        """
        Test case to get questions with invalid page.

        :param self:
        :return:
        """
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.NOT_FOUND)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.NOT_FOUND]
        )

    def test_get_questions_with_invalid_method(self):
        """
        Test case to get questions with invalid method.

        :param self:
        :return:
        """
        response = self.client().put('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.METHOD_NOT_ALLOWED)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.METHOD_NOT_ALLOWED]
        )

    def test_add_question_successfully(self):
        """
        Test case to add question successfully.

        :param self:
        :return:
        """
        response = self.client().post('/questions', json=self.test_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.CREATED)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('id'))

    def test_add_question_with_invalid_request(self):
        """
        Test case to add questions with invalid request.

        :param self:
        :return:
        """
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.BAD_REQUEST)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.BAD_REQUEST]
        )

    def test_delete_question_successfully(self):
        """
        Test case to delete question successfully.

        :param self:
        :return:
        """
        response = self.client().post('/questions', json=self.test_question)
        response_id = json.loads(response.data).get('id')

        response = self.client().delete(f'/questions/{response_id}')
        self.assertEqual(response.status_code, HTTP_STATUS.NO_CONTENT)

    def test_delete_question_with_invalid_id(self):
        """
        Test case to delete questions with invalid id.

        :param self:
        :return:
        """
        response = self.client().delete(f'/questions/-1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.NOT_FOUND)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.NOT_FOUND]
        )

    def test_search_question_successfully(self):
        """
        Test case to search questions successfully.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions/search',
            json={'searchTerm': 'a'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.OK)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('questions')))

    def test_search_question_with_invalid_method(self):
        """
        Test case to search questions with invalid method.

        :param self:
        :return:
        """
        response = self.client().get('/questions/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.METHOD_NOT_ALLOWED)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.METHOD_NOT_ALLOWED]
        )

    def test_get_questions_by_category_successfully(self):
        """
        Test case to get questions by category successfully.

        :param self:
        :return:
        """
        response = self.client().get(
            f'/categories/{self.test_category}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.OK)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('questions')))
        self.assertTrue(len(data.get('current_category')))
        self.assertTrue(data.get('total_questions'))

    def test_search_question_with_invalid_category(self):
        """
        Test case to get questions by invalid category.

        :param self:
        :return:
        """
        response = self.client().get('/categories/-1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.NOT_FOUND)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.NOT_FOUND]
        )

    def test_quiz_successfully(self):
        """
        Test case to play quiz successfully.

        :param self:
        :return:
        """
        response = self.client().post('/quizzes', json=self.quiz_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.OK)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('question')))

    def test_add_question_with_invalid_request(self):
        """
        Test case to add questions with invalid request.

        :param self:
        :return:
        """
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.BAD_REQUEST)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.BAD_REQUEST]
        )


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
