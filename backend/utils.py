"""Utils module for trivia app."""

from flask import jsonify
from models import Category
from constants import ERROR_MESSAGES


def get_formatted_categories():
    """
    Get all categories formatted.

    :return:
    """
    categories = Category.query.order_by(Category.type).all()
    return {category.id: category.type for category in categories}


def paginated_data(request, model, order_by, default_limit):
    """
    Get paginated data.

    :param request:
    :param queryset:
    :param page_limit:
    :return:
    """
    page_limit = request.args.get('limit', default_limit, type=int)
    selected_page = request.args.get('page', 1, type=int)
    index = selected_page - 1

    queryset = model.query.order_by(order_by).limit(
        page_limit).offset(page_limit * index).all()

    return [row.format() for row in queryset] \
        if queryset else [], model.query.count()


def error_response(http_status):
    """
    Get error response based on http status.

    :param http_status:
    :return:
    """
    return jsonify({
        "success": False,
        "error": http_status,
        "message": ERROR_MESSAGES[http_status]
        }), http_status
