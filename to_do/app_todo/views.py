from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def tasklist(requests):
    return HttpResponse('to do list')
