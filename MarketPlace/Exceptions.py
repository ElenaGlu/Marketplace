class AppExceptions(Exception):
    pass


class AppError(AppExceptions):
    pass


class ErrorType:
    TOKEN_ERROR = {
        'status_code': 403,
        'summary': 'Forbidden',
    }

    REGISTRATION_ERROR = {
        'status_code': 409,
        'summary': 'Conflict',
    }

    EMAIL_TOKEN_ERROR = {
        'status_code': 400,
        'summary': 'Bad Request',
    }

    ACCESS_ERROR = {
        'status_code': 403,
        'summary': 'Forbidden',
    }

    CATALOG_ERROR = {
        'status_code': 404,
        'summary': 'Not Found',
    }

    PRODUCT_ERROR = {
        'status_code': 404,
        'summary': 'Not Found',
    }

    AVAILABLE_PRODUCT_ERROR = {
        'status_code': 400,
        'summary': 'Bad Request',
     }