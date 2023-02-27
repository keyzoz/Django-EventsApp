from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView


from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,logout

from .forms import *

from .models import *


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
