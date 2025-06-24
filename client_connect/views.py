from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Mailing, Message, Recipient, SendingAttempt


# CRUD Recipient
class RecipientCreateView(CreateView):
    """Представление отвечающее за создание получателя"""
    model = Recipient
    template_name = "client_connect/recipient/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("client_connect:_")


class RecipientDetailView(DetailView):
    """Представление отвечающее за детальную информацию о получателе"""
    model = Recipient
    template_name = "client_connect/recipient/recipient_detail.html"
    context_object_name = "recipient"


class RecipientUpdateView(UpdateView):
    """Представление отвечающее за редактирование получателя"""
    model = Recipient
    template_name = "client_connect/recipient/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("client_connect:_")


class RecipientDeleteView(DeleteView):
    """Представление отвечающее за удаление получателя"""
    model = Recipient
    template_name = "client_connect/recipient/recipient_confirm_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("client_connect:_")


# CRUD Message
class MessageCreateView(CreateView):
    """Представление отвечающее за создание сообщения"""
    model = Message
    template_name = "client_connect/message/message_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("client_connect:_")


class MessageDetailView(DetailView):
    """Представление отвечающее за детальную информацию о сообщения"""
    model = Message
    template_name = "client_connect/message/message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    """Представление отвечающее за редактирование сообщения"""
    model = Message
    template_name = "client_connect/message/message_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("client_connect:_")


class MessageDeleteView(DeleteView):
    """Представление отвечающее за удаление сообщения"""
    model = Message
    template_name = "client_connect/message/message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("client_connect:_")


# CRUD Mailing
class MailingCreateView(CreateView):
    """Представление отвечающее за создание рассылки"""
    model = Mailing
    template_name = "client_connect/mailing/mailing_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("client_connect:_")


class MailingDetailView(DetailView):
    """Представление отвечающее за детальную информацию о рассылки"""
    model = Mailing
    template_name = "client_connect/mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        """Добавление в контекст сообщение и получателей"""
        context = super().get_context_data(**kwargs)
        context["message"] = self.object.message
        context["recipients"] = self.object.recipient.all()
        return context


class MailingUpdateView(UpdateView):
    """Представление отвечающее за редактирование рассылки"""
    model = Mailing
    template_name = "client_connect/mailing/mailing_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("client_connect:_")


class MailingDeleteView(DeleteView):
    """Представление отвечающее за удаление рассылки"""
    model = Mailing
    template_name = "client_connect/mailing/mailing_confirm_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("client_connect:_")
