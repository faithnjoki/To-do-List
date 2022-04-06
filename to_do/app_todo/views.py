from asyncio import tasks
from dataclasses import field
from pyexpat import model
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy
# login view 
from django.contrib.auth.views import LoginView

from .models import Task




# Create your views here.
class CustomLogiView(LoginView):
    template_name =  'templates/app_todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = 'True'

    # the function overrides the success url am using
    def get_success_ulrs(self):
        return reverse_lazy('tasks')




class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    # redirrect Value 
    success_url = reverse_lazy('tasks')

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class DeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
