from random import random, sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from sendler.forms import ClientForm, MessageForm, MailSettingsForm, MailSettingsModeratorForm
from sendler.models import MailSettings, Client, Message, Log


class IndexView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'sendler/index.html'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = MailSettings.objects.count()
        context['active_mailing'] = MailSettings.objects.filter(status='CREATE').count()
        context['unique_clients'] = Client.objects.values('email').distinct().count()
        all_posts = list(Blog.objects.filter(is_published=True))
        context['random_posts'] = Blog.objects.all().order_by('?')[:3]
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
    success_url = reverse_lazy('sendler:message_list')

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
        return reverse_lazy('sendler:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления сообщения"""

    model = Message
    success_url = reverse_lazy('sendler:message_list')


class MailSettingsCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания настройки рассылки"""

    model = MailSettings
    form_class = MailSettingsForm
    success_url = reverse_lazy('sendler:mail_settings_list')

    def form_valid(self, form):
        mail_settings = form.save()
        user = self.request.user
        mail_settings.owner = user
        mail_settings.save()
        return super().form_valid(form)


class MailSettingsListView(LoginRequiredMixin, ListView):
    """Контроллер списка настроек рассылки"""

    model = MailSettings

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('sendler.can_view_mail_settings'):
            return super().get_queryset()
        return super().get_queryset().filter(owner=user)


class MailSettingsDetailView(LoginRequiredMixin, DetailView):
    """Контроллер детального просмотра настройки рассылки"""

    model = MailSettings

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class MailSettingsUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования настройки рассылки"""

    model = MailSettings
    form_class = MailSettingsForm

    def get_success_url(self):
        return reverse_lazy('sendler:mail_settings_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailSettingsForm
        if user.has_perm("sendler.can_view_mail_settings") and user.has_perm("sendler.can_edit_mailsettings"):
            return MailSettingsModeratorForm
        raise PermissionDenied


class MailSettingsDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления настройки рассылки"""

    model = MailSettings
    success_url = reverse_lazy('sendler:mail_settings_list')


class LogListView(LoginRequiredMixin, ListView):
    """Контроллер списка попыток рассылки"""

    model = Log
    template_name = 'sendler/mailing_log_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        mail_settings_pk = self.kwargs.get('pk')
        queryset = queryset.filter(mail_settings__pk=mail_settings_pk)
        return queryset