from django.shortcuts import render


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):
        if isinstance(exception, ValueError):
            return render(request, status=400, context={'exception_message': exception})
        else:
            return render(request, status=500)