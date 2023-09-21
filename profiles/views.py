from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView

# Create your views here.
class ProfileView(CreateView):
    template_name = ''
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    