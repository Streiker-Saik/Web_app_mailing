from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.forms.forms import BaseForm
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseBase
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from config import settings

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, Message, Recipient, SendingAttempt
from .services import AccessControlService


class BaseLoginView(LoginRequiredMixin):
    """Базовый класс представления прав доступа к контролерам"""
    # Объявлен тип для IDE
    request: HttpRequest
    kwargs: dict

    model = None
    queryset = None

    def get_queryset(self):
        """"""
        if self.queryset is not None:
            return self.queryset
        if self.model is not None:
            return self.model.objects.all()
        else:
            raise NotADirectoryError("Укажите model либо queryset в подклассе")

    def get_object(self):
        """"""
        pk = self.kwargs.get("pk")
        if pk is None:
            raise Http404("pk не передан в URL")
        return get_object_or_404(self.get_queryset(), pk=pk)

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        """
        Проверка прав доступа перед обработкой запроса
        :param request: HTTP-запрос
        :param args: Позиционные аргументы
        :param kwargs: Ключевые аргументы, включая "pk" получателя
        :return: HttpResponse с результатом выполнения или доступом.
        """
        obj = self.get_object()
        user = self.request.user

        access_response = AccessControlService.authorize_access(
            user=user,
            obj=obj,
            permission_name=self.get_permission_name()
        )

        if access_response is not None:
            return access_response

        return super().dispatch(request, *args, **kwargs)

    def get_permission_name(self) -> str:
        """Метод заполняемы в подклассе, для передачи названия доступа"""
        raise NotADirectoryError("Подкласс должен реализовать метод get_permission_name")

# CRUD Recipient
class RecipientCreateView(LoginRequiredMixin, CreateView):
    """
    Представление отвечающее за создание получателя
    Методы:
        form_valid(self, form: RecipientForm) -> HttpResponse:
            Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
    """

    model = Recipient
    form_class = RecipientForm
    template_name = "client_connect/recipient/recipient_form.html"
    success_url = reverse_lazy("client_connect:_")

    def form_valid(self, form: RecipientForm) -> HttpResponse:
        """
        Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
        :param form: Форма, содержащая данные для создания нового получателя
        :return: При успешном создании перенаправляет на success_url
        """
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientDetailView(BaseLoginView, DetailView):
    """
    Представление отвечающее за детальную информацию о получателе.
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.view_recipient"
    """

    model = Recipient
    template_name = "client_connect/recipient/recipient_detail.html"
    context_object_name = "recipient"

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.view_recipient"""
        return "client_connect.view_recipient"


class RecipientUpdateView(BaseLoginView, UpdateView):
    """
    Представление отвечающее за редактирование получателя.
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_recipient"
    """

    model = Recipient
    form_class = RecipientForm
    template_name = "client_connect/recipient/recipient_form.html"
    success_url = reverse_lazy("client_connect:_")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_recipient"""
        return "client_connect.change_recipient"


class RecipientDeleteView(BaseLoginView, DeleteView):
    """
    Представление отвечающее за удаление получателя
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_recipient"
    """

    model = Recipient
    template_name = "client_connect/recipient/recipient_confirm_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("client_connect:_")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_recipient"""
        return "client_connect.delete_recipient"

# CRUD Message
class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Представление отвечающее за создание сообщения
    Методы:
        form_valid(self, form: MessageForm) -> HttpResponse:
            Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
    """

    model = Message
    form_class = MessageForm
    template_name = "client_connect/message/message_form.html"
    success_url = reverse_lazy("client_connect:_")

    def form_valid(self, form: MessageForm) -> HttpResponse:
        """
        Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
        :param form: Форма, содержащая данные для создания нового сообщения
        :return: При успешном создании перенаправляет на success_url
        """
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageDetailView(BaseLoginView, DetailView):
    """
    Представление отвечающее за детальную информацию о сообщения
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.view_message"
    """

    model = Message
    template_name = "client_connect/message/message_detail.html"
    context_object_name = "message"

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.view_message"""
        return "client_connect.view_message"


class MessageUpdateView(BaseLoginView, UpdateView):
    """
    Представление отвечающее за редактирование сообщения
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_message"
    """

    model = Message
    form_class = MessageForm
    template_name = "client_connect/message/message_form.html"
    success_url = reverse_lazy("client_connect:_")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_message"""
        return "client_connect.change_message"


class MessageDeleteView(BaseLoginView, DeleteView):
    """
    Представление отвечающее за удаление сообщения
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"
    """

    model = Message
    template_name = "client_connect/message/message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("client_connect:_")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"""
        return "client_connect.delete_message"


# CRUD Mailing
class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Представление отвечающее за создание рассылки
    Методы:
        form_valid(self, form: MailingForm) -> HttpResponse:
            Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
        get_form(self, form_class: Optional[BaseForm] = None) -> BaseForm:
            Возвращает форму с фильтрованными полями message и recipients, по текущему пользователю
    """

    model = Mailing
    form_class = MailingForm
    template_name = "client_connect/mailing/mailing_form.html"
    success_url = reverse_lazy("client_connect:mailing_create")

    def form_valid(self, form: MailingForm) -> HttpResponse:
        """
        Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
        :param form: Форма, содержащая данные для создания новой рассылки
        :return: При успешном создании перенаправляет на success_url
        """
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)

    def get_form(self, form_class: Optional[BaseForm] = None) -> BaseForm:
        """
        Возвращает форму с фильтрованными полями message и recipients, по текущему пользователю
        :param form_class: Класс формы, который нужно создать. Если None, используется класс по умолчанию.
        :return: Экземпляр формы с установленным queryset
        """
        form = super().get_form(form_class)
        user = self.request.user
        form.fields["message"].queryset = Message.objects.filter(owner=user) # type: ignore
        form.fields["recipients"].queryset = Recipient.objects.filter(owner=user) # type: ignore
        return form


class MailingDetailView(BaseLoginView, DetailView):
    """
    Представление отвечающее за детальную информацию о рассылки
    Методы:
        get_context_data(self, **kwargs) -> dict:
            Добавление в контекст сообщение и получателей
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"
    """

    model = Mailing
    template_name = "client_connect/mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs) -> dict:
        """Добавление в контекст сообщение и получателей"""
        context = super().get_context_data(**kwargs)
        context["message"] = self.object.message
        context["recipients"] = self.object.recipient.filter(owner=self.request.user)
        return context

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.view_mailing"""
        return "client_connect.view_mailing"

class MailingUpdateView(BaseLoginView, UpdateView):
    """
    Представление отвечающее за редактирование рассылки
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_message"
    """

    model = Mailing
    form_class = MailingForm
    template_name = "client_connect/mailing/mailing_form.html"
    success_url = reverse_lazy("client_connect:_")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_mailing"""
        return "client_connect.change_mailing"


class MailingDeleteView(BaseLoginView, DeleteView):
    """
    Представление отвечающее за удаление рассылки
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"
    """

    model = Mailing
    template_name = "client_connect/mailing/mailing_confirm_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("client_connect:_")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_mailing"""
        return "client_connect.delete_mailing"

class HomeViews(TemplateView):
    """Представление для отображения информации о рассылках"""

    template_name = "client_connect/home.html"

    def get_context_data(self, **kwargs):
        """Заносит в контекст все рассылки, рассылки со статусом 'запущено' и уникальных получателей"""
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "mailings": Mailing.objects.all(),
                "start_mailings": Mailing.objects.filter(status="launched"),
                "recipients": Recipient.objects.distinct(),
            }
        )
        return ctx


class SendingAttemptCreateView(CreateView):
    """Представление отвечающее за создание попытки рассылки"""

    model = SendingAttempt
    template_name = "client_connect/sending_attempt/sending_attempt_create.html"


class MailingSendView(View):
    """Представление отвечающее за отправку рассылки"""

    def post(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, mailing_id)
        message = get_object_or_404(Message, mailing.message.id)
        recipients = mailing.recipient.all()
        recipient_list = [recipient.email for recipient in recipients]
        try:
            subject = message.subject
            message = message.body
            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, recipient_list)
        except Exception as exc_info:
            SendingAttempt.object.create(status="fail", answer=str(exc_info), mailing=mailing)
        else:
            SendingAttempt.object.create(status="suc", answer="Сообщение успешно отправлено", mailing=mailing)
