from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'sendler/index.html'
    extra_context = {
        'title': 'Главная страница'
    }
