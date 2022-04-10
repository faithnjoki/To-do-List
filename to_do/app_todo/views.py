from asyncio import tasks
from dataclasses import field
from multiprocessing import context
from pyexpat import model
from urllib import request
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

# Login view 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# UserCreationForm is like a register form
from django.contrib.auth.forms import UserCreationForm

# Login form
from django.contrib.auth import login

from .models import Task


# Create your views here.
class CustomLoginView(LoginView):
    template_name =  'app_todo/login.html'
    fields = '__all__'

    # The function overrides the success URL
    def get_success_url(self):
        return reverse_lazy('tasks')

    
class RegisterPage(FormView):
    template_name = 'app_todo/register.html'
    # Inbuilt django form
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        # Saves user 
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super (RegisterPage,self).form_valid(form)

    # A logged in user cannot be registered again 
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect ('tasks')
        return super (RegisterPage, self).get( *args, **kwargs)


class TaskList( LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # User can only get their own data through this
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        # Arranges incomplete tasks to the top
        context['count'] = context['tasks'].filter(complete = False).count()
        return context


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreate(CreateView):
    model = Task
    fields = ['title','description','complete']
    # Redirect value 
    success_url = reverse_lazy('tasks')
    
    # Ensure we don't select user using dropdown incase of multiple users 
    def form_valid(self,form):
        # self.request.user is the logged in user
        form.instance.user = self.request.user   
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
