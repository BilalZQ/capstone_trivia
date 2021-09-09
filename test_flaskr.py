"""Module for unit tests of trivia app."""

import os
import pdb
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import app
from models import setup_db, Question, Category, test_database_path
from constants import (HTTP_STATUS, ERROR_MESSAGES, MISSING_AUTHORIZATION,
                       INVALID_BEARER_TOKEN, INVALID_BEARER_TOKEN)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
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
        self.test_edit_question = {
            "question": "TestQ1",
            "answer": "TestA1",
            "category": self.test_category,
            "difficulty": 2
        }
        self.quiz_data = {
            'quiz_category': {'id': 1},
            'previous_questions': []
        }

        with open('./trivia_tokens.json') as json_file:
            data = json.load(json_file)
            self.admin_header = {
                'Authorization': 'Bearer {}'.format(data.get('admin'))
            }
            self.user_header = {
                'Authorization': 'Bearer {}'.format(data.get('user'))
            }

        self.invalid_bearer_token = {
            'Authorization': 'Bearer {} invalid'.format(data.get('member'))
        }

        self.without_token = {
            'Authorization': 'Bearer'
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
        self.assertEqual(
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
        self.assertEqual(
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
        self.assertEqual(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.METHOD_NOT_ALLOWED]
        )

    def test_add_question_successfully(self):
        """
        Test case to add question successfully.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json=self.test_question, headers=self.admin_header)
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
        response = self.client().post(
            '/questions', json={}, headers=self.admin_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.BAD_REQUEST)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.BAD_REQUEST]
        )

    def test_add_question_without_auth_header(self):
        """
        Test case to add questions without auth.

        :param self:
        :return:
        """
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), MISSING_AUTHORIZATION)

    def test_add_question_with_invalid_bearer(self):
        """
        Test case to add questions with invalid bearer token.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json={}, headers=self.invalid_bearer_token)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), INVALID_BEARER_TOKEN)

    def test_add_question_without_token(self):
        """
        Test case to add questions without token.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json={}, headers=self.without_token)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), INVALID_BEARER_TOKEN)

    def test_add_question_with_invalid_user(self):
        """
        Test case to add questions with wrong unauthorized user.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json={}, headers=self.user_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.FORBIDDEN)
        self.assertEqual(data.get('success'), False)
        self.assertTrue(ERROR_MESSAGES[HTTP_STATUS.FORBIDDEN])

    def test_delete_question_successfully(self):
        """
        Test case to delete question successfully.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json=self.test_question, headers=self.admin_header)
        response_id = json.loads(response.data).get('id')

        response = self.client().delete(
            f'/questions/{response_id}', headers=self.admin_header)
        self.assertEqual(response.status_code, HTTP_STATUS.NO_CONTENT)

    def test_delete_question_with_invalid_id(self):
        """
        Test case to delete questions with invalid id.

        :param self:
        :return:
        """
        response = self.client().delete(
            f'/questions/-1', headers=self.admin_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.NOT_FOUND)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.NOT_FOUND]
        )

    def test_delete_question_without_auth_header(self):
        """
        Test case to delete questions without auth.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json=self.test_question, headers=self.admin_header)
        response_id = json.loads(response.data).get('id')

        response = self.client().delete(f'/questions/{response_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), MISSING_AUTHORIZATION)

    def test_delete_question_with_invalid_bearer(self):
        """
        Test case to delete questions with invalid bearer token.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json=self.test_question, headers=self.admin_header)
        response_id = json.loads(response.data).get('id')

        response = self.client().delete(
            f'/questions/{response_id}', headers=self.invalid_bearer_token)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), INVALID_BEARER_TOKEN)

    def test_delete_question_without_token(self):
        """
        Test case to delete questions without token.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json=self.test_question, headers=self.admin_header)
        response_id = json.loads(response.data).get('id')

        response = self.client().delete(
            f'/questions/{response_id}', headers=self.without_token)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), INVALID_BEARER_TOKEN)

    def test_delete_question_with_invalid_user(self):
        """
        Test case to delete questions with wrong unauthorized user.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json=self.test_question, headers=self.admin_header)
        response_id = json.loads(response.data).get('id')

        response = self.client().delete(
            f'/questions/{response_id}', headers=self.user_header)
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, HTTP_STATUS.FORBIDDEN)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'),
                         ERROR_MESSAGES[HTTP_STATUS.FORBIDDEN])

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
        self.assertEqual(
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
        self.assertEqual(
            data.get('message'),
            ERROR_MESSAGES[HTTP_STATUS.NOT_FOUND]
        )

    def test_quiz_successfully(self):
        """
        Test case to play quiz successfully.

        :param self:
        :return:
        """
        response = self.client().post(
            '/quizzes', json=self.quiz_data, headers=self.user_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.OK)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('question')))

    def test_play_quiz_without_auth_header(self):
        """
        Test case to play quiz without auth.

        :param self:
        :return:
        """
        response = self.client().post(
            '/quizzes', json=self.quiz_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), MISSING_AUTHORIZATION)

    def test_play_quiz_with_invalid_bearer(self):
        """
        Test case to play quiz with invalid bearer token.

        :param self:
        :return:
        """
        response = self.client().post(
            '/quizzes', json=self.quiz_data, headers=self.invalid_bearer_token)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), INVALID_BEARER_TOKEN)

    def test_play_quiz_without_token(self):
        """
        Test case to play quiz without token.

        :param self:
        :return:
        """
        response = self.client().post(
            '/quizzes', json=self.quiz_data, headers=self.without_token)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), INVALID_BEARER_TOKEN)

    def test_play_quiz_with_admin(self):
        """
        Test case to play quiz with admin token.

        :param self:
        :return:
        """
        response = self.client().post(
            '/quizzes', json=self.quiz_data, headers=self.admin_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTP_STATUS.OK)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(len(data.get('question')))

    def test_edit_question_successfully(self):
        """
        Test case to successfully edit question.

        :param self:
        :return:
        """
        response = self.client().post(
            '/questions', json=self.test_question, headers=self.admin_header)
        question_id = response.get_json().get('id')
        response = self.client().patch(f'/questions/{question_id}',
                                       json=self.test_edit_question,
                                       headers=self.admin_header)
        json_data = response.get_json()
        edited_question = {**self.test_edit_question, "id": question_id}
        self.assertEqual(response.status_code, HTTP_STATUS.CREATED)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('question'), edited_question)

    def test_update_question_without_auth_header(self):
        """
        Test case to add questions with invalid request.

        :param self:
        :return:
        """
        response = self.client().patch('/questions/1', json={})
        data = response.get_json()
        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), MISSING_AUTHORIZATION)

    def test_update_question_with_invalid_bearer(self):
        """
        Test case to update questions with invalid bearer token.

        :param self:
        :return:
        """
        response = self.client().patch(
            '/questions/1', json={}, headers=self.invalid_bearer_token)
        data = response.get_json()
        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), INVALID_BEARER_TOKEN)

    def test_update_question_without_token(self):
        """
        Test case to update questions without token.

        :param self:
        :return:
        """
        response = self.client().patch(
            '/questions/1', json={}, headers=self.without_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, HTTP_STATUS.UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), INVALID_BEARER_TOKEN)

    def test_update_question_with_invalid_user(self):
        """
        Test case to update questions with wrong unauthorized user.

        :param self:
        :return:
        """
        response = self.client().patch(
            '/questions/1', json={}, headers=self.user_header)
        json_data = response.get_json()
        self.assertEqual(response.status_code, HTTP_STATUS.FORBIDDEN)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[HTTP_STATUS.FORBIDDEN])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
