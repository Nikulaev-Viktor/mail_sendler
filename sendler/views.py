from random import random, sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from sendler.forms import ClientForm, MessageForm
from sendler.models import MailSettings, Client, Message


class IndexView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'sendler/index.html'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = MailSettings.objects.count()
        context['active_mailing'] = MailSettings.objects.filter(status=['CREATE', 'LAUNCHED']).count()
        context['unique_clients'] = Client.objects.values('email').distinct().count()
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


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('sendler:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер списка клиентов"""
    model = Client

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Контроллер просмотра клиента"""
    model = Client

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy('sendler:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления клиента"""
    model = Client
    success_url = reverse_lazy('sendler:client_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер списка сообщений"""

    model = Message

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Контроллер детального просмотра сообщения"""

    model = Message

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования сообщения"""

    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления сообщения"""

    model = Message
    success_url = reverse_lazy('mailing:message_list')

