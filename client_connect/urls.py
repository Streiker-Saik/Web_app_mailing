from django.urls import path

from client_connect.apps import ClientConnectConfig

from .views import (HomeViews, MailingCreateView, MailingDeleteView, MailingDetailView, MailingSendView,
                    MailingsListView, MailingUpdateView, MessageCreateView, MessageDeleteView, MessageDetailView,
                    MessagesListView, MessageUpdateView, RecipientCreateView, RecipientDeleteView, RecipientDetailView,
                    RecipientsListViews, RecipientUpdateView, SendingAttemptsListView)

app_name = ClientConnectConfig.name

urlpatterns = [
    path("", HomeViews.as_view(), name="home"),
    # адреса работы с получателями(Recipient)
    path("recipients/", RecipientsListViews.as_view(), name="recipients_list"),
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/<int:pk>/detail/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient/<int:pk>/edit/", RecipientUpdateView.as_view(), name="recipient_edit"),
    path("recipient/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    # адреса работы с сообщениями(Message)
    path("messages/", MessagesListView.as_view(), name="messages_list"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/detail/", MessageDetailView.as_view(), name="message_detail"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_edit"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    # адреса работы с рассылкой(Mailing)
    path("mailings/", MailingsListView.as_view(), name="mailings_list"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/detail/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_edit"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing/<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    # адреса работы с рассылкой(SendingAttempt)
    path("sending_attempts/", SendingAttemptsListView.as_view(), name="sending_attempts_list"),
]
