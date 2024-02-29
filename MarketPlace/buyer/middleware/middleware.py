from django.http import JsonResponse

from Exceptions import TokenError


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(exception):
        error_data = exception.args[0]
        if isinstance(exception, TokenError):
            return JsonResponse(
                status=error_data['error_type']['status'],
                data={
                    'description': exception.args[0]['description'],
                    'summary': error_data['error_type']['summary'],
                }
            )
