from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView


# Create your views here.
class IndexView(CreateView):
    template_name = 'main_pages/index.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name, {})
