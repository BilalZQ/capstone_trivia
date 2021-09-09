"""Constants module for trivia app."""

AUTH0_DOMAIN = 'fsnd-bilal.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone-trivia'

QUESTIONS_PER_PAGE = 10


class HTTP_STATUS:
    """HTTP Status codes."""

    NOT_FOUND = 404
    NO_CONTENT = 204
    BAD_REQUEST = 400
    CREATED = 201
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
    METHOD_NOT_ALLOWED = 405
    OK = 200
    UNAUTHORIZED = 401
    FORBIDDEN = 403


ERROR_MESSAGES = {
    HTTP_STATUS.NOT_FOUND: 'Resource Not Found',
    HTTP_STATUS.BAD_REQUEST: 'Bad Request',
    HTTP_STATUS.UNPROCESSABLE_ENTITY: 'Unprocessable Entity',
    HTTP_STATUS.INTERNAL_SERVER_ERROR: 'Internal Server Error',
    HTTP_STATUS.METHOD_NOT_ALLOWED: 'Method Not Allowed',
    HTTP_STATUS.FORBIDDEN: 'Forbidden Request',
    HTTP_STATUS.UNAUTHORIZED: 'Unauthorized Request'
}


MISSING_AUTHORIZATION = \
    'Authorization header in request headers is mandatory.'
INVALID_BEARER_TOKEN = \
    'Invalid authorization format, expected "Bearer <Token>"'
