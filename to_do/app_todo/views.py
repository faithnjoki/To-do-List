from asyncio import tasks
from dataclasses import field
from multiprocessing import context
from pyexpat import model
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
# login view 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
# UserCreationForm is like a register form
from django.contrib.auth.forms import UserCreationForm

# login form
from django.contrib.auth import login

from .models import Task




# Create your views here.
class CustomLoginView(LoginView):
    template_name =  'app_todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    # the function overrides the success url am using
    def get_success_url(self):
        return reverse_lazy('tasks')

    
class RegisterPage(FormView):
    template_name = 'app_todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')



class TaskList( LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # User can only get their own data  by this:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()
        return context
    
       
    

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'

class TaskCreate(CreateView):
    model = Task
    fields = ['title','description', 'complete']
    # redirrect Value 
    success_url = reverse_lazy('tasks')
    
    # function ensures that we dont select user  using the drop down incase we have multiple users 
    def form_valid(self,form):
        # self.request.user  is the logined in used
        form.instance.user = self.request.user   
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')

class DeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
