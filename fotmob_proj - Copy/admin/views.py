from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse

from django.db import connection

# Create your views here.
def  AdminHomeView  (request):
        username = ""
        if request.session.has_key('member_id'):
                username = request.session['member_id']
        return render(request,  'adminoption_page.html',{'user':username});
def  InsertView  (request):
        return render(request,  'insert.html');
