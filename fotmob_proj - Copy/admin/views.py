from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse

from django.db import connection

# Create your views here.
def  AdminHomeView  (request,user):
        return render(request,  'adminoption_page.html',{'user':user});
def  InsertView  (request):
        return render(request,  'insert.html');
