from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import config.settings
from mailing.models import Messages, Clients, Transmission
from mailing.services import sendmail
from mailing.forms import TransmissionCreateForm, Statistic, ClientCreateForm, MessageCreateForm
from blog.models import Blog
from django.core.cache import cache


class MainView(LoginRequiredMixin, ListView):
    """Main page with blog and statistic"""
    model = Messages
    template_name = "mailing/main.html"

    def get_queryset(self):
        """Execute blog part cash on main page"""
        if config.settings.CACHE_ENABLED:
            key = 'main_blog'
            cache_data = cache.get(key)
            if cache_data is None:
                cache_data = Blog.objects.order_by('?')[:3]
                cache.set(key, cache_data)
        else:
            cache_data = Blog.objects.order_by('?')[:3]
        return cache_data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Main"
        # show blogs
        context["Blog"] = self.get_queryset()
        # show statistic
        context["all_transmissions"] = len(Transmission.objects.all())
        context["active_transmissions"] = len(Transmission.objects.filter(is_published=True))
        context["all_clients"] = len(Clients.objects.all())
        context["unique_clients"] = len(Clients.objects.all().values('email').distinct())
        return context


class ClientsView(ListView):
    """Show all clients for owner / moderator / admin"""
    model = Clients
    template_name = "mailing/clients.html"

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Clients"
        context["Clients"] = self.get_queryset()
        return context


class ClientCard(DetailView):
    """Show all information about client"""
    model = Clients
    template_name = "mailing/client_card.html"
    slug_url_kwarg = "client_slug"

    def get_object(self, queryset=None):
        one_client = super().get_object()
        return one_client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Client Full Information"
        context["Client"] = self.get_object()
        return context


class ClientCreate(CreateView):
    """Create client"""
    model = Clients
    form_class = ClientCreateForm
    template_name = "mailing/client_create.html"

    def get_context_data(self, *, object_list=None, context_object_name=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Add New Client"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:clients')

    def form_valid(self, form):
        # save owner of user
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdate(UpdateView):
    """Update client"""
    model = Clients
    fields = ["full_name", "comment", "email"]
    template_name = "mailing/client_update.html"
    slug_url_kwarg = "client_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update Client"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:clients')

    def form_valid(self, form):
        return super().form_valid(form)


class ClientDelete(DeleteView):
    """Delete client"""
    model = Clients
    template_name = "mailing/delete.html"
    slug_url_kwarg = "client_slug"

    def get_context_data(self, *, object_list=None, context_object_name=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Client"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:clients')


class MessagesView(ListView):
    """Show all message for owner / moderator / admin"""
    model = Messages
    template_name = "mailing/messages.html"

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Messages"
        context["Messages"] = self.get_queryset
        return context


class MessageCard(DetailView):
    """Show all information about message"""
    model = Messages
    template_name = "mailing/message_card.html"
    slug_url_kwarg = "message_slug"

    def get_object(self, queryset=None):
        one_message = super().get_object()
        return one_message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Message Full Information"
        context["Message"] = self.get_object()
        return context


class MessageCreate(CreateView):
    """Create message"""
    model = Messages
    template_name = "mailing/message_create.html"
    form_class = MessageCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Create Message Template"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:messages')

    def form_valid(self, form):
        # save owner of message
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdate(UpdateView):
    """Update message"""
    model = Messages
    fields = ["theme", "body"]
    template_name = "mailing/message_update.html"
    slug_url_kwarg = "message_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update Message"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:messages')

    def form_valid(self, form):
        return super().form_valid(form)


class MessageDelete(DeleteView):
    """Delete message"""
    model = Messages
    template_name = "mailing/delete.html"
    slug_url_kwarg = "message_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Message"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:messages')


class TransmissionCard(DetailView):
    """Show all information about transmission"""
    model = Transmission
    template_name = "mailing/transmission_card.html"
    slug_url_kwarg = "transmission_slug"

    def get_object(self, queryset=None):
        one_transmission = super().get_object()
        return one_transmission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Transmission Full Information"
        current_object = self.get_object()
        context["Transmission"] = current_object
        context["Statistic"] = current_object.get_statistic()
        return context


class TransmissionView(ListView):
    """Show all transmissions for owner / moderator / admin"""
    model = Transmission
    template_name = "mailing/transmissions.html"

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Transmissions"
        context["Transmissions"] = self.get_queryset()
        return context


class TransmissionCreate(CreateView):
    """Create transmission"""
    model = Transmission
    form_class = TransmissionCreateForm
    template_name = "mailing/transmission_create.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Create New Transmission"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:transmissions')

    def form_valid(self, form):

        # Create default statistic for transmission
        current_transmission = self.object
        self.object = form.save()

        # save owner of transmission
        self.object.owner = self.request.user
        self.object.save()

        # Set default data for created transmission
        Statistic.objects.create(transmission_id=self.object.pk)

        # Executing send message
        schedule_transmission_time = self.object.time
        current_time = datetime.now().time()
        if schedule_transmission_time <= current_time:
            message_data = self.object.message.get_info()
            sendmail(self.object.pk, self.object.clients.all(), message_data[0], message_data[1])
            self.object.status = "FINISHED"
            self.object.save()

        return super().form_valid(form)


class TransmissionDelete(DeleteView):
    """Delete transmission"""
    model = Transmission
    template_name = "mailing/delete.html"
    slug_url_kwarg = "transmission_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Transmission"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:transmissions')


class TransmissionUpdate(UpdateView):
    """Update transmission"""
    model = Transmission
    fields = ["title", "time", "frequency", "message", "clients", "is_published"]
    template_name = "mailing/transmission_update.html"
    slug_url_kwarg = "transmission_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update Transmission"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:transmissions')

    def form_valid(self, form):
        # check send time
        schedule_transmission_time_update = form.cleaned_data["time"]
        current_time = datetime.now().time()
        self.object.status = "CREATED"
        self.object.save()
        if schedule_transmission_time_update <= current_time and self.object.is_published is True:
            message_data = self.object.message.get_info()
            sendmail(self.object.pk, self.object.clients.all(), message_data[0], message_data[1])
            self.object.status = "FINISHED"
            self.object.save()

        return super().form_valid(form)
