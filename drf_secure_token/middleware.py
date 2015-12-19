from django.http import HttpResponse


class GenerateToken(object):
    def process_response(self, request, response):
        response['X-Token'] = "asdasd"
        return response

