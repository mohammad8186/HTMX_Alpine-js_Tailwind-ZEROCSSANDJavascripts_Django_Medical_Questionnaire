

from django.conf import settings

class CustomSessionMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        if request.user.is_superuser:
            request.session.set_expiry(20 * 60)  
       
        elif request.user.is_authenticated:
            request.session.set_expiry(20 * 60) 

        response = self.get_response(request)
        return response
