# from io import BytesIO
from django.http import HttpRequest, QueryDict
from .models import APILog

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        request_copy = self.copy_request(request)
        response = self.get_response(request)
        # self.log_request(request_copy)
        # self.log_response(request_copy, response)
        return response
    def copy_request(self, request):
        # request_copy = HttpRequest()
        # request_copy.method = request.method
        # request_copy.path = request.path
        # request_copy.headers = request.headers.copy()
        # request_copy.encoding = request.encoding
        # request_copy.GET = request.GET.copy()
        # request_copy.POST = request.POST.copy()
        # request_copy._body = request.body
        # return request_copy
        pass
    def log_request(self, request):
        # headers = dict(request.headers)
        body = ""
        try:
            # body_bytes = request.body
            # body = body_bytes.decode("utf-8")
            pass
        except UnicodeDecodeError:
            pass
        data = QueryDict('', mutable=True)
        if request.method == "GET":
            data = request.GET.copy()
        elif request.method == "POST":
            data = request.POST.copy()
        APILog.objects.create(
            request_method=request.method,
            request_path=request.path,
            # request_headers=headers,
            request_body=body,
            request_data=data
        )
    def log_response(self, request, response):
        APILog.objects.filter(
            # request_method=request.method,
            request_path=request.path
        ).update(
            response_status=response.status_code,
            response_body=response.content.decode("utf-8")
        )
