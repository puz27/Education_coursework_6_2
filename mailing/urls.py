from django.urls import path
from mailing.views import MessagesView, ClientsView, MainView, MessageCreate, TransmissionCreate, \
    TransmissionView, TransmissionDelete, MessageDelete, TransmissionCard, TransmissionUpdate, \
    MessageCard, MessageUpdate, ClientDelete, ClientCard, ClientCreate, ClientUpdate


app_name = "mailing"

urlpatterns = [
    path("", MainView.as_view(), name="main_page"),
    path("messages/", MessagesView.as_view(), name="messages"),
    path("message_create/", MessageCreate.as_view(), name="message_create"),
    path("message_delete/<slug:message_slug>", MessageDelete.as_view(), name="message_delete"),
    path("message_update/<slug:message_slug>", MessageUpdate.as_view(), name="message_update"),
    path("message_card/<slug:message_slug>", MessageCard.as_view(), name="message_card"),
    path("clients/", ClientsView.as_view(), name="clients"),
    path("client_create/", ClientCreate.as_view(), name="client_create"),
    path("client_delete/<slug:client_slug>", ClientDelete.as_view(), name="client_delete"),
    path("client_update/<slug:client_slug>", ClientUpdate.as_view(), name="client_update"),
    path("client_card/<slug:client_slug>", ClientCard.as_view(), name="client_card"),
    path("transmissions/", TransmissionView.as_view(), name="transmissions"),
    path("transmission_create/", TransmissionCreate.as_view(), name="transmission_create"),
    path("transmission_delete/<slug:transmission_slug>", TransmissionDelete.as_view(), name="transmission_delete"),
    path("transmission_update/<slug:transmission_slug>", TransmissionUpdate.as_view(), name="transmission_update"),
    path("transmission_card/<slug:transmission_slug>", TransmissionCard.as_view(), name="transmission_card"),
]
