from . import views,login_and_sign_up

class LogUserMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        login_and_sign_up.log_user(request=request)

        return response