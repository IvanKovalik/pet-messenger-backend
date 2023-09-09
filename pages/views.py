from django.shortcuts import render
from django.views.generic import CreateView


# Create your views here.
class IndexView(CreateView):
    template_name = 'main_pages/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
