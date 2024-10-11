from random import random, sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from blog.models import Blog
from sendler.models import MailSettings, Client


class IndexView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'sendler/index.html'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = MailSettings.objects.count()
        context['active_mailing'] = MailSettings.objects.filter(status='CREATE').count()
        context['unique_clients'] = Client.objects.distinct().count()
        all_posts = list(Blog.objects.filter(is_published=True))
        context['random_posts'] = sample(all_posts, min(len(all_posts), 3))
        return context


class ContactsView(View):
    """Контроллер страницы контактов"""

    def get(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f' {name} ({phone}): {message})')
        context = {
            'title': 'Контакты'
        }
        return render(request, 'sendler/contacts.html', context)




