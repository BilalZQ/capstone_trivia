"""Init module for trivia app."""

import os
from flask import Flask, json, request, abort, jsonify
from sqlalchemy.orm import query
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from .auth import AuthError, requires_auth
from models import setup_db, Question, Category
from utils import (
  paginated_data, get_formatted_categories, error_response
)
from constants import QUESTIONS_PER_PAGE, HTTP_STATUS


def create_app(test_config=None):
    """
    Create & configure the app.

    :param test_config:
    :return:
    """
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'*': {'origins': '*'}})

    # CORS headers
    @app.after_request
    def after_request(response):
        """
        Set response headers after request.

        :param response:
        :return:
        """
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE')
        return response

    @app.route('/categories')
    def get_categories():
        """
        Return all categories.

        :return:
        """
        return jsonify({
            'success': True,
            'categories': get_formatted_categories(),
          })

    @app.route('/questions')
    def get_questions():
        """
        Return paginated questions.

        :return:
        """
        paginated_response, questions_count = paginated_data(
            request, Question, Question.id, QUESTIONS_PER_PAGE)

        if not paginated_response:
            abort(HTTP_STATUS.NOT_FOUND)

        return jsonify({
          'success': True,
          'questions': paginated_response,
          'total_questions': questions_count,
          'categories': get_formatted_categories(),
          'current_category': None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @requires_auth('delete-question')
    def delete_question(token, question_id):
        """
        Delete question.

        :param question_id:
        :return:
        """
        question = Question.query.get(question_id)
        if not question:
            abort(HTTP_STATUS.NOT_FOUND)

        question.delete()

        return jsonify({
          'success': True
        }), HTTP_STATUS.NO_CONTENT

    @app.route('/questions', methods=['POST'])
    @requires_auth('add-question')
    def add_question(token):
        """
        Create question.

        :return:
        """
        question = request.get_json()

        if not question:
            abort(HTTP_STATUS.BAD_REQUEST)

        question = Question(**question)
        question.insert()

        return jsonify({
          'success': True,
          'id': question.id
        }), HTTP_STATUS.CREATED

    @app.route('/questions/<int:question_id>', methods=['PATCH'])
    @requires_auth('edit-question')
    def edit_question(token, question_id):
        """
        Edit question.

        :return:
        """
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            abort(HTTP_STATUS.NOT_FOUND)

        request_data = request.get_json()
        question.question = request_data.get('question')
        question.answer = request_data.get('answer')
        question.category = request_data.get('category')
        question.difficulty = request_data.get('difficulty')
        question.update()

        return jsonify({
          'success': True,
          'question': question.format()
        }), HTTP_STATUS.CREATED

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        Search question.

        :param question_id:
        :return:
        """
        search_term = request.get_json().get('searchTerm')
        questions = [question.format() for question in Question.query.filter(
          Question.question.ilike(f'%{search_term}%'))]
        return jsonify({
          'success': True,
          'questions': questions,
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        Get question by category.

        :param category_id:
        :return:
        """
        category = Category.query.get(category_id)
        if not category:
            abort(HTTP_STATUS.NOT_FOUND)

        questions = [
          question.format()
          for question in Question.query.filter_by(category=category_id)]

        return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(questions),
          'current_category': category.format()
        })

    @app.route('/quizzes', methods=['POST'])
    @requires_auth('play-quiz')
    def play_quiz(token):
        """
        Play quiz.

        :return:
        """
        request_data = request.get_json()
        category = request_data.get('quiz_category')
        previous_questions = request_data.get('previous_questions', [])

        if not category:
            abort(HTTP_STATUS.BAD_REQUEST)

        category_id = category.get('id')
        filters = [Question.id.notin_(previous_questions)]
        if category_id:
            filters.append(Question.category == category_id)
        questions = Question.query.filter(*filters)

        questions = [question.format() for question in questions]
        random_question = random.choice(questions) if questions else None
        return jsonify({
          'success': True,
          'question': random_question
        })


    # Error Handling
    @app.errorhandler(AuthError)
    def auth_error(error):
        """
        Error handling for our custom auth error class.
        :param error:
        :return:
        """
        return jsonify(error.error), error.status_code

    @app.errorhandler(HTTP_STATUS.UNAUTHORIZED)
    def not_found(error):
        """
        Error handler for status code 401.
        :param error:
        :return:
        """
        return error_response(HTTP_STATUS.UNAUTHORIZED)

    @app.errorhandler(HTTP_STATUS.FORBIDDEN)
    def not_found(error):
        """
        Error handler for status code 403.
        :param error:
        :return:
        """
        return error_response(HTTP_STATUS.FORBIDDEN)

    @app.errorhandler(HTTP_STATUS.NOT_FOUND)
    def not_found(error):
        """
        Error handler for status code 404.

        :param error:
        :return:
        """
        return error_response(HTTP_STATUS.NOT_FOUND)

    @app.errorhandler(HTTP_STATUS.BAD_REQUEST)
    def bad_request(error):
        """
        Error handler for status code 400.

        :param error:
        :return:
        """
        return error_response(HTTP_STATUS.BAD_REQUEST)

    @app.errorhandler(HTTP_STATUS.UNPROCESSABLE_ENTITY)
    def unprocessable_entity(error):
        """
        Error handler for status code 422.

        :param error:
        :return:
        """
        return error_response(HTTP_STATUS.UNPROCESSABLE_ENTITY)

    @app.errorhandler(HTTP_STATUS.INTERNAL_SERVER_ERROR)
    def internal_server_error(error):
        """
        Error handler for status code 500.

        :param error:
        :return:
        """
        return error_response(HTTP_STATUS.INTERNAL_SERVER_ERROR)

    @app.errorhandler(HTTP_STATUS.METHOD_NOT_ALLOWED)
    def method_not_allowed(error):
        """
        Error handler for status code 405.

        :param error:
        :return:
        """
        return error_response(HTTP_STATUS.METHOD_NOT_ALLOWED)

    return app
