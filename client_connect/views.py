from typing import Optional, Type

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.db.models import QuerySet
from django.forms.forms import BaseForm
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBase, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, Message, Recipient, SendingAttempt
from .services import AccessControlService, DecoratorsService, MailingService

# определяем декоратор кеширования, если кеш включен накладывает декоратор, если нет, отдает обычный результат класса
cache_decorator = DecoratorsService.get_cache_decorator()


class BaseLoginView(LoginRequiredMixin):
    """
    Базовый класс представления прав доступа к контролерам
    Атрибуты:
        request (HttpRequest): HTTP-запрос(Объявлен тип для IDE).
        kwargs (dict): Ключевые аргументы запроса(Объявлен тип для IDE).
        model (Type[models.Model]): Модель для обработки запросов.
        queryset (QuerySet): Набор данных для обработки запросов.
    Методы:
        get_queryset(self) -> QuerySet:
            Получение набора данных для обработки запроса.
            raise NotADirectoryError: Если в подклассе не указана модели или queryset
        get_object(self) -> models.Model:
            Получение объекта по первичному ключу из URL.
            raise Http404("pk не передан в URL")
        dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
            Проверка прав доступа перед обработкой запроса
        get_permission_name(self) -> str:
            Метод заполняемы в подклассе, для передачи названия доступа
            raise NotADirectoryError: Если в подклассе не реализован метод
    """

    # Объявлен тип для IDE
    request: HttpRequest
    kwargs: dict

    model: Type[models.Model] = None
    queryset: QuerySet = None

    def get_queryset(self) -> QuerySet:
        """
        Получение набора данных для обработки запроса.
        :return: Набор данных, если он задан, либо все объекты модели
        :raise NotADirectoryError: Если в подклассе не указана модели или queryset
        """
        if self.queryset is not None:
            return self.queryset
        if self.model is not None:
            return self.model.objects.all()
        else:
            raise NotADirectoryError("Укажите model либо queryset в подклассе")

    def get_object(self) -> models.Model:
        """
        Получение объекта по первичному ключу из URL.
        :return: Объект модели, соответствующий указанному pk.
        :raise Http404: Если pk не передан в URL или объект не найден.
        """
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
            user=user, obj=obj, permission_name=self.get_permission_name()
        )

        if access_response is not None:
            return access_response

        return super().dispatch(request, *args, **kwargs)

    def get_permission_name(self) -> str:
        """
        Метод заполняемы в подклассе, для передачи названия доступа
        :return: Название доступа
        :raise NotADirectoryError: Если в подклассе не реализован метод
        """
        raise NotADirectoryError("Подкласс должен реализовать метод get_permission_name")


class BaseCreateView(LoginRequiredMixin, CreateView):
    """
    Базовый класс представления прав доступа к контролерам создания.
    Атрибуты:
        request (HttpRequest): HTTP-запрос(Объявлен тип для IDE)
    Методы:
        dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
            Проверка прав доступа перед обработкой запроса
        get_permission_name(self) -> str:
            Метод заполняемы в подклассе, для передачи названия доступа
            raise NotADirectoryError: Если в подклассе не реализован метод
    """

    # Объявлен тип для IDE
    request: HttpRequest

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        """
        Проверка прав доступа на создание объекта.
        :param request: HTTP-запрос
        :param args: Позиционные аргументы
        :param kwargs: Ключевые аргументы
        :return: HttpResponse с результатом выполнения или доступом
        :return: HttpResponseForbidden, если доступ запрещен.
        """
        user = self.request.user
        if not AccessControlService.can_create_object(user=user, permission_name=self.get_permission_name()):
            return HttpResponseForbidden("У вас нет доступа к созданию объекта.")
        return super().dispatch(request, *args, **kwargs)

    def get_permission_name(self) -> str:
        """
        Метод заполняемы в подклассе, для передачи названия доступа
        :return: Название доступа
        :raise NotADirectoryError: Если в подклассе не реализован метод
        """
        raise NotADirectoryError("Подкласс должен реализовать метод get_permission_name")


class BaseListView(LoginRequiredMixin, ListView):
    """
    Базовый класс представления прав доступа к контролерам списков.
    Атрибуты:
        request (HttpRequest): HTTP-запрос(Объявлен тип для IDE)
    Методы:
        dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
            Проверка прав доступа перед обработкой запроса
        get_permission_name(self) -> str:
            Метод заполняемы в подклассе, для передачи названия доступа
            raise NotADirectoryError: Если в подклассе не реализован метод
    """

    # Объявлен тип для IDE
    request: HttpRequest

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        """
        Проверка прав доступа на создание объекта.
        :param request: HTTP-запрос
        :param args: Позиционные аргументы
        :param kwargs: Ключевые аргументы
        :return: HttpResponse с результатом выполнения или доступом
        :return: HttpResponseForbidden, если доступ запрещен.
        """
        user = self.request.user
        if not AccessControlService.can_create_object(user=user, permission_name=self.get_permission_name()):
            return HttpResponseForbidden("У вас нет доступа к списку объектов.")
        return super().dispatch(request, *args, **kwargs)

    def get_permission_name(self) -> str:
        """
        Метод заполняемы в подклассе, для передачи названия доступа
        :return: Название доступа
        :raise NotADirectoryError: Если в подклассе не реализован метод
        """
        raise NotADirectoryError("Подкласс должен реализовать метод get_permission_name")


# List: Recipients, Messages, Mailings, SendingAttempt
class RecipientsListViews(BaseListView, ListView):
    """
    Класс отвечающий за представление списка получателей.
    Отображает список получателей в шаблоне recipients_list.html.
    Порядок отображения получателей - email
    Методы:
        get_queryset(self) -> QuerySet:
            Переопределение метода get_queryset для получения списка получателей.
            Пользователь видит только своих получателей.
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView:
            "client_connect.can_list_recipients"
    """

    model = Recipient
    template_name = "client_connect/recipient/recipients_list.html"
    context_object_name = "recipients"
    ordering = ["email"]

    def get_queryset(self) -> QuerySet:
        """
        Переопределение метода get_queryset для получения списка получателей.
        Пользователь видит только своих получателей.
        :return: QuerySet получателей.
        """
        user = self.request.user
        if not (user.has_perm("client_connect.can_list_recipients") or user.is_superuser):
            recipients = Recipient.objects.filter(owner=user)
            return recipients
        return super().get_queryset()

    def get_permission_name(self) -> str:
        """
        Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.can_list_recipients
        """

        return "client_connect.can_list_recipients"


class MessagesListView(BaseListView, ListView):
    """
    Класс отвечающий за представление списка сообщений.
    Отображает список сообщений в шаблоне messages_list.html.
    Порядок отображения сообщений - subject
    Методы:
        get_queryset(self) -> QuerySet:
            Переопределение метода get_queryset для получения списка сообщений.
            Пользователь видит только свои сообщения.
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.can_list_messages"
    """

    model = Message
    template_name = "client_connect/message/messages_list.html"
    context_object_name = "messages"
    ordering = ["subject"]

    def get_queryset(self) -> QuerySet:
        """
        Переопределение метода get_queryset для получения списка сообщений.
        Пользователь видит только свои сообщения.
        :return: QuerySet сообщений.
        """
        user = self.request.user
        if not (user.has_perm("client_connect.can_list_messages") or user.is_superuser):
            messages = Message.objects.filter(owner=user)
            return messages
        return super().get_queryset()

    def get_permission_name(self) -> str:
        """
        Метод для передачи названия доступа в родительский класс BaseLoginView:
        "client_connect.can_list_messages
        """

        return "client_connect.can_list_messages"


class MailingsListView(BaseListView, ListView):
    """
    Класс отвечающий за представление списка рассылок.
    Отображает список рассылок в шаблоне mailings_list.html.
    Порядок отображения рассылок - end_time по убыванию
    Методы:
        get_queryset(self) -> QuerySet:
            Переопределение метода get_queryset для получения списка рассылок.
            Пользователь видит только свои рассылки.
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView:
            "client_connect.can_list_mailings"
    """

    model = Mailing
    template_name = "client_connect/mailing/mailings_list.html"
    context_object_name = "mailings"
    ordering = ["-end_time"]

    def get_queryset(self) -> QuerySet:
        """
        Переопределение метода get_queryset для получения списка рассылок.
        Пользователь видит только своих рассылок.
        :return: QuerySet рассылок.
        """
        user = self.request.user
        if not (user.has_perm("client_connect.can_list_mailings") or user.is_superuser):
            recipients = Mailing.objects.filter(owner=user)
            return recipients
        return super().get_queryset()

    def get_permission_name(self) -> str:
        """
        Метод для передачи названия доступа в родительский класс BaseLoginView:
        "client_connect.can_list_mailings
        """

        return "client_connect.can_list_mailings"


class SendingAttemptsListView(BaseListView, ListView):
    """
    Класс отвечающий за представление списка попыток рассылок.
    Отображает список рассылок в шаблоне sending_attempts_list.html.
    Порядок отображения рассылок - mailing и created_at по убыванию
    Методы:
        get_queryset(self) -> QuerySet:
            Переопределение метода get_queryset для получения списка попыток рассылок.
            Пользователь видит только свои рассылки
        get_context_data(self, **kwargs) -> dict:
            Добавления в контекст информации: всего попыток, удачных попыток, неудачных попыток и процентное содержание
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView:
            "client_connect.can_list_sending_attempts"
    """

    model = SendingAttempt
    template_name = "client_connect/sending_attempt/sending_attempts_list.html"
    context_object_name = "sending_attempts"
    ordering = ["mailing", "-created_at"]

    def get_queryset(self) -> QuerySet:
        """
        Переопределение метода get_queryset для получения списка рассылок.
        Пользователь видит только свои попытки рассылок.
        :return: QuerySet рассылок.
        """
        user = self.request.user
        if not (user.has_perm("client_connect.can_list_sending_attempts") or user.is_superuser):
            recipients = SendingAttempt.objects.filter(mailing__owner=user)
            return recipients
        return super().get_queryset()

    def get_context_data(self, **kwargs) -> dict:
        """
        Добавления в контекст информации: всего попыток, удачных попыток, неудачных попыток и процентное содержание
        """

        context = super().get_context_data(**kwargs)
        send_all = len(self.get_queryset().all())
        send_success = len(self.get_queryset().filter(status="success"))
        send_fail = len(self.get_queryset().filter(status="fail"))
        if send_success:
            success_rate = round((send_success / send_all * 100), 2)
        else:
            success_rate = 100
        if send_fail:
            fail_rate = round((send_fail / send_all * 100), 2)
        else:
            fail_rate = 100
        context.update(
            {
                "send_all": send_all,
                "send_success": send_success,
                "success_rate": success_rate,
                "send_fail": send_fail,
                "fail_rate": fail_rate,
            }
        )
        return context

    def get_permission_name(self) -> str:
        """
        Метод для передачи названия доступа в родительский класс BaseLoginView:
        "client_connect.can_list_sending_attempts"
        """

        return "client_connect.can_list_sending_attempts"


# CRUD Recipient
class RecipientCreateView(BaseCreateView):
    """
    Представление отвечающее за создание получателя
    Методы:
        form_valid(self, form: RecipientForm) -> HttpResponse:
            Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: 'client_connect.create_recipient'
    """

    model = Recipient
    form_class = RecipientForm
    template_name = "client_connect/recipient/recipient_form.html"
    success_url = reverse_lazy("client_connect:recipients_list")

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

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: 'client_connect.create_recipient'"""
        return "client_connect.create_recipient"


@cache_decorator
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
        get_success_url(self) -> HttpResponse:
            Перехож на страницу измененного получателя
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_recipient"
    """

    model = Recipient
    form_class = RecipientForm
    template_name = "client_connect/recipient/recipient_form.html"

    def get_success_url(self) -> HttpResponse:
        """Перехож на страницу измененного получателя"""
        return reverse_lazy("client_connect:recipient_detail", kwargs={"pk": self.object.pk})

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
    success_url = reverse_lazy("client_connect:recipients_list")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_recipient"""
        return "client_connect.delete_recipient"


# CRUD Message
class MessageCreateView(BaseCreateView):
    """
    Представление отвечающее за создание сообщения
    Методы:
        form_valid(self, form: MessageForm) -> HttpResponse:
            Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: 'client_connect.create_message'
    """

    model = Message
    form_class = MessageForm
    template_name = "client_connect/message/message_form.html"
    success_url = reverse_lazy("client_connect:messages_list")

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

    def get_permission_name(self):
        """Метод для передачи названия доступа в родительский класс BaseLoginView: 'client_connect.create_message'"""
        return "client_connect.create_message"


@cache_decorator
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
        get_success_url(self) -> HttpResponse:
            Перехож на страницу измененного сообщения
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_message"
    """

    model = Message
    form_class = MessageForm
    template_name = "client_connect/message/message_form.html"

    def get_success_url(self) -> HttpResponse:
        """Перехож на страницу измененного сообщения"""
        return reverse_lazy("client_connect:message_detail", kwargs={"pk": self.object.pk})

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
    success_url = reverse_lazy("client_connect:messages_list")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"""
        return "client_connect.delete_message"


# CRUD Mailing
class MailingCreateView(BaseCreateView):
    """
    Представление отвечающее за создание рассылки
    Методы:
        form_valid(self, form: MailingForm) -> HttpResponse:
            Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
        get_form(self, form_class: Optional[BaseForm] = None) -> BaseForm:
            Возвращает форму с фильтрованными полями message и recipients, по текущему пользователю
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: 'client_connect.create_mailing'
    """

    model = Mailing
    form_class = MailingForm
    template_name = "client_connect/mailing/mailing_form.html"
    success_url = reverse_lazy("client_connect:mailings_list")

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
        form.fields["message"].queryset = Message.objects.filter(owner=user)  # type: ignore
        form.fields["recipients"].queryset = Recipient.objects.filter(owner=user)  # type: ignore
        return form

    def get_permission_name(self):
        """Метод для передачи названия доступа в родительский класс BaseLoginView: 'client_connect.create_mailing'"""
        return "client_connect.create_mailing"


@cache_decorator
class MailingDetailView(BaseLoginView, DetailView):
    """
    Представление отвечающее за детальную информацию о рассылки
    Методы:
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"
    """

    model = Mailing
    template_name = "client_connect/mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.view_mailing"""
        return "client_connect.view_mailing"


class MailingUpdateView(BaseLoginView, UpdateView):
    """
    Представление отвечающее за редактирование рассылки
    Методы:
        get_success_url(self) -> HttpResponse:
            Перехож на страницу измененной рассылки
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_message"
        get_form(self, form_class: Optional[BaseForm] = None) -> BaseForm:
            Возвращает форму с фильтрованными полями message и recipients, по текущему пользователю
    """

    model = Mailing
    form_class = MailingForm
    template_name = "client_connect/mailing/mailing_form.html"

    def get_success_url(self) -> HttpResponse:
        """Перехож на страницу измененной рассылки"""
        return reverse_lazy("client_connect:mailing_detail", kwargs={"pk": self.object.pk})

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_mailing"""
        return "client_connect.change_mailing"

    def get_form(self, form_class: Optional[BaseForm] = None) -> BaseForm:
        """
        Возвращает форму с фильтрованными полями message и recipients, по текущему пользователю
        :param form_class: Класс формы, который нужно создать. Если None, используется класс по умолчанию.
        :return: Экземпляр формы с установленным queryset
        """
        form = super().get_form(form_class)
        user = self.request.user
        form.fields["message"].queryset = Message.objects.filter(owner=user)  # type: ignore
        form.fields["recipients"].queryset = Recipient.objects.filter(owner=user)  # type: ignore
        return form


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
    success_url = reverse_lazy("client_connect:mailings_list")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_mailing"""
        return "client_connect.delete_mailing"


class HomeViews(LoginRequiredMixin, TemplateView):
    """
    Представление для отображения информации о рассылках
    Методы:
        get_context_data(self, **kwargs) -> dict:
            Заносит в контекст все рассылки, рассылки со статусом 'запущено' и уникальных получателей.
            Для пользователя не входящего в группы и не являющего супер пользователем выводит только свои данные.
    """

    template_name = "client_connect/home.html"

    def get_context_data(self, **kwargs) -> dict:
        """Заносит в контекст все рассылки, рассылки со статусом 'запущено' и уникальных получателей"""

        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.groups.exists() and not user.is_superuser:
            mailings = Mailing.objects.filter(owner=user)
            start_mailings = Mailing.objects.filter(owner=user, status="launched")
            recipients = Recipient.objects.filter(owner=user).distinct()
        else:
            mailings = Mailing.objects.all()
            start_mailings = Mailing.objects.filter(status="launched")
            recipients = Recipient.objects.distinct()

        context.update(
            {
                "mailings": mailings,
                "start_mailings": start_mailings,
                "recipients": recipients,
            }
        )

        return context


class MailingSendView(BaseLoginView, View):
    """
    Представление отвечающее за отправку рассылки
    Методы:
        post(self, request: HttpRequest, pk: int) -> HttpResponse:
            Обработка пост запроса запуска рассылки.
        get_permission_name(self) -> str:
            Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_mailing
    """

    model = Mailing

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Обработка пост запроса запуска рассылки.
        :param request: HTTP-запрос
        :param pk: Первичный ключ рассылки
        :return: Переход на список рассылок
        """
        mailing = get_object_or_404(Mailing, pk=pk)  # получаем объект рассылки
        MailingService.update_status(mailing, "launched")
        message = get_object_or_404(Message, pk=mailing.message.pk)  # получаем объект сообщения из объекта рассылки
        recipients = mailing.recipients.all()  # получаем объекты получателей из объекта рассылки
        recipient_list = [recipient.email for recipient in recipients]
        if not recipient_list:
            return HttpResponse("Список получателей пуст")
        MailingService.send_messages(recipients=recipient_list, message=message, mailing=mailing)
        MailingService.update_status(mailing, "done")
        return redirect("client_connect:mailings_list")

    def get_permission_name(self) -> str:
        """Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_mailing"""
        return "client_connect.change_mailing"


class MailingSendDisableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Представление отвечающее за отключения рассылки
    Методы:
        post(self, request: HttpRequest, pk: int) -> HttpResponse:
            Обработка пост отключения рассылки
    """

    model = Mailing
    permission_required = "client_connect.can_disable_send"

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """
        Обработка пост запроса запуска рассылки.
        :param request: HTTP-запрос
        :param pk: Первичный ключ рассылки
        :return: Переход на список рассылок
        """
        mailing = get_object_or_404(Mailing, pk=pk)  # получаем объект рассылки
        MailingService.update_status(mailing, "disable")
        return redirect("client_connect:mailings_list")
