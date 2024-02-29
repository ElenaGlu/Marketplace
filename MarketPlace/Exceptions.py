class MyException(Exception):
    pass


class TokenError(MyException):
    pass


class ErrorTypes:
    TOKEN_ERROR = {
        'status': 403,
        'summary': 'Ошибка токена',
    }

