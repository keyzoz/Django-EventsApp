from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from eventProject import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib import messages

import redis
import json

from eventApp.utils import DataMixin
from eventApp.forms import *
from eventApp.models import *
from eventApp.tasks import send_email_task

redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)



class EventHome(DataMixin, ListView):
    model = Event
    template_name = 'eventApp/index.html'
    context_object_name = 'events'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        return dict(list(context.items())+list(c_def.items())) 
    
    def get_queryset(self):
        return Event.objects.filter(is_published=True).select_related('category')
    
class AddEvent(LoginRequiredMixin,DataMixin,CreateView):
    form_class = AddEventForm
    template_name = 'eventApp/add_event.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add a new event')
        return dict(list(context.items())+list(c_def.items())) 
    
class AddCategory(LoginRequiredMixin,DataMixin,CreateView):
    form_class = AddCategoryForm
    template_name = 'eventApp/add_category.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add a new category')
        return dict(list(context.items())+list(c_def.items())) 

class LoginUser(DataMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'eventApp/login.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return dict(list(context.items())+list(c_def.items())) 

    def get_success_url(self):
        return reverse_lazy('home')

def userLogout(request):
    logout(request)
    return redirect('login')

class RegisterUser(DataMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'eventApp/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Register')
        return dict(list(context.items())+list(c_def.items())) 
    
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('home')

class EventDetail(DataMixin,DeleteView):
    model = Event
    template_name = 'eventApp/event.html'
    slug_url_kwarg = 'event_slug'
    context_object_name = 'event'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["event"])
        return dict(list(context.items())+list(c_def.items())) 

class EventCategory(DataMixin,ListView):
    model = Event
    template_name = 'eventApp/index.html'
    context_object_name = 'events'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(slug = self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category ' + str(cat.name),
                                      cat_selected = cat.pk)
        res = dict(list(context.items())+list(c_def.items())) 
        return dict(list(context.items())+list(c_def.items())) 
    
    def get_queryset(self) :
        return Event.objects.filter(category__slug=self.kwargs['cat_slug'],is_published=True).select_related('category')

class SendMail(DataMixin, FormView):
    template_name = 'eventApp/send_mail.html'
    form_class = SendMailForm
    success_url = reverse_lazy('home')
    
    def get_recipient_list(self):
        recipient_list_json = redis_conn.get('recipient_list')
        if recipient_list_json:
            recipient_list = json.loads(recipient_list_json)
        else:
            recipient_list = [user.email for user in User.objects.all()]
            redis_conn.set('recipient_list', json.dumps(recipient_list))
        return recipient_list
    
    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        recipient_list = self.get_recipient_list()
        redis_conn.sadd('emails', *recipient_list)
        send_email_task.delay(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return super(SendMail, self).form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return dict(list(context.items())+list(c_def.items())) 

    
