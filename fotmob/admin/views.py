from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse

from django.db import connection

# Create your views here.
def  AdminHomeView  (request):
        username = ""
        if request.session.has_key('member_id'):
                username = request.session['member_id']
        cursor = connection.cursor()
        sql = "SELECT  GETRESULT(MATCH_ID),MATCH_ID FROM MATCH  ORDER BY DATE_ DESC;"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        whole_content = []
        
        for r in result2:
            if(r != "NULL"):
                score_list = r[0].split(',')
                match_date = score_list[0]
                h_name = score_list[1]
                h_id = score_list[2]
                h_goals = score_list[3]
                a_goals =score_list[4]
                
                a_name =score_list[5]
                a_id =score_list[6]
                m_id = r[1]
            row  = {'t1_id':h_id,'t2_id':a_id,'m_id':m_id,'m_date':match_date,'h_name':h_name,'h_goals':h_goals,'a_name':a_name,'a_goals':a_goals}
            whole_content.append(row);
        
        
        

        return render(request,  'adminoption_page.html',{'user':username,'matches':whole_content});
def  InsertView  (request):
        return render(request,  'insert.html');
