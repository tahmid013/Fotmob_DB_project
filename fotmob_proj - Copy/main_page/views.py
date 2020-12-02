from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.db import connection

# Create your views here.
def  HomepageView(request):
        username = ""
        if request.session.has_key('member_id'):
                username = request.session['member_id']
        return render(request, 'base.html',{'user':username});
def  InsertView  (request):
        return render(request,  'insert.html');
def  LogoutView(request):
        try:
            del request.session['member_id']
        except:
            pass
        username = ""
        if request.session.has_key('member_id'):
            username = request.session['member_id']
        return render(request, 'base.html',{'user':username});

def  LoginView(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        cursor = connection.cursor()
        sql = "SELECT Username, Password FROM ADMIN"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        matched = False
        
        for r in result:
            if r[0]==username and r[1]==password:
                matched=True
                break
        dict ={'user' : username,'matched' : matched}
      
        if matched:
            request.session['member_id'] = username
            request.session.set_expiry(600)
            return TemplateResponse(request, 'base.html', { 'user': username});
        else:
            return render(request, 'loginfailed.html');
    else:
        return render(request, 'loginPage.html');
def  TablePoint(request):
        cursor = connection.cursor()
        sql = "SELECT S.TEAM_ID,T.TEAM_NAME ,T.SHORT_NAME,Win(S.TEAM_ID),Draw(S.TEAM_ID),Lose(S.TEAM_ID) FROM SCORES S JOIN TEAM T ON (S.TEAM_ID = T.TEAM_ID) GROUP BY S.TEAM_ID,T.TEAM_NAME,T.SHORT_NAME "
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        dict = [] 
        for r in result:
            Team_id = r[0]
            Team_name = r[1]
            Short_name = r[2]
            Point = 3*r[3]+r[4]
            W = r[3]
            D = r[4]
            L = r[5]
            PL =(W+L+D)
            row  = {'Team_id': Team_id,'Team_name': Team_name,'Short_name':Short_name,'Played':PL,'Point':Point,'Win':W,'Draw':D,'Lose':L}
            dict.append(row);
        return render(request,'table_point.html',{'table' :dict});
def  TeamInfo(request ,Team_id):
        cursor = connection.cursor()
        sql = "SELECT * FROM TEAM WHERE Team_id = +" + Team_id
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        sql = "SELECT GetGoal(%s,MATCH_ID) FROM MATCH WHERE HOME_ID =%s or AWAY_ID =%s ORDER BY DATE_ DESC;"
        cursor.execute(sql,[Team_id,Team_id,Team_id])
        result2 = cursor.fetchall()
        cursor.close()
        whole_content = []
        dict1 = [] 
        for r in result:
            Team_id = r[0]
            Team_name = r[1]
            short_name = r[2]
            row  = {'Team_id': Team_id,'Team_name': Team_name,'short_name':short_name}
            dict1.append(row);
        dict2 = [] 
        for r in result2:
            if(r != "NULL"):
                score = r[0]
            row  = {'score': score}
            dict2.append(row);
        
        
        
        whole_content={'team_info':dict1,'result':dict2}

        return render(request,'Team_info.html',{'content' :whole_content});
def  CompareUtilView(request):
        
        return render(request,'compare.html');
def  CompareView(request):
        if request.method=='POST':
            player_1=[]
            player_2=[]
            player1_id =-1
            player2_id =-1
            
            player1_n = request.POST['player1']
            player2_n = request.POST['player2']
            
            
            cursor = connection.cursor()
            sql = "SELECT PLAYER_ID FROM PLAYER WHERE (FIRST_NAME||' '||LAST_NAME = %s);"
            cursor.execute(sql,[player1_n])
            result = cursor.fetchall()
            cursor.close()
            for r in result:
                player1_id =r[0]
            
            cursor = connection.cursor()
            sql = "SELECT PLAYER_ID FROM PLAYER WHERE (FIRST_NAME||' '||LAST_NAME = %s);"
            cursor.execute(sql,[player2_n])
            result = cursor.fetchall()
            cursor.close()
            for r in result:
                player2_id =r[0]    
            
            
            cursor = connection.cursor()
            sql = "SELECT * FROM PLAYER WHERE PLAYER_id = %s"
            cursor.execute(sql,[ player1_id])
            result1 = cursor.fetchall()
            cursor.close()
            
           

            dict1 = [] 
            for r2 in result1:
                    Name = r2[1]+' '+r2[2]
                    Position = r2[3]
                    Munutes_played = r2[4]
                    Red_Card = r2[5]
                    Yellow_card = r2[6]
                    Country = r2[7]
                    row ={
                    'Name':Name,
                    'Position':Position,
                    'Minutes_played':Munutes_played,
                    'Red_card':Red_Card,
                    'Yellow_card':Yellow_card,
                    'Country':Country,
                    }
                    dict1.append(row);
            dict2=[]
            cursor = connection.cursor()
            sql = "SELECT SUM(GOALS) FROM SCORES  WHERE SCORING_ID = %s GROUP BY SCORING_ID"
            cursor.execute(sql,[ player1_id])
            result2 = cursor.fetchall()
            cursor.close()
            goal = 0
            for r in result2:
                    goal = r[0]
                    
            dict2.append({'g': goal})
            dict3=[]
            cursor = connection.cursor()
            sql = "SELECT SUM(ASSIST) FROM SCORES  WHERE ASSIST_ID = %s GROUP BY ASSIST_ID"
            cursor.execute(sql,[ player1_id])
            result3 = cursor.fetchall()
            cursor.close()
            asst = 0
            for r in result3:
                    asst = r[0]
            dict3.append({'a': asst})
            player1 ={'player_details' :dict1,'goals':goal,'assist':asst}
            
            cursor = connection.cursor()
            sql = "SELECT * FROM PLAYER WHERE PLAYER_id = %s"
            cursor.execute(sql,[ player2_id])
            result1 = cursor.fetchall()
            cursor.close()
            
           

            dict1 = [] 
            for r2 in result1:
                    Name = r2[1]+' '+r2[2]
                    Position = r2[3]
                    Munutes_played = r2[4]
                    Red_Card = r2[5]
                    Yellow_card = r2[6]
                    Country = r2[7]
                    row ={
                    'Name':Name,
                    'Position':Position,
                    'Minutes_played':Munutes_played,
                    'Red_card':Red_Card,
                    'Yellow_card':Yellow_card,
                    'Country':Country,
                    }
                    dict1.append(row);
            dict2=[]
            cursor = connection.cursor()
            sql = "SELECT SUM(GOALS) FROM SCORES  WHERE SCORING_ID = %s GROUP BY SCORING_ID"
            cursor.execute(sql,[ player2_id])
            result2 = cursor.fetchall()
            cursor.close()
            goal = 0
            for r in result2:
                    goal = r[0]
                    
            dict2.append({'g': goal})
            dict3=[]
            cursor = connection.cursor()
            sql = "SELECT SUM(ASSIST) FROM SCORES  WHERE ASSIST_ID = %s GROUP BY ASSIST_ID"
            cursor.execute(sql,[ player2_id])
            result3 = cursor.fetchall()
            cursor.close()
            asst = 0
            for r in result3:
                    asst = r[0]
            dict3.append({'a': asst})
            player2 ={'player_details' :dict1,'goals':goal,'assist':asst}
            if (player1_id ==-1 or player2_id ==-1):
                
                return render(request,'compare.html',{'safe':False});
            else:
                return render(request,'compare.html',{'safe':True,'player1' :player1,'player2' :player2});
        else:
            return render(request,'compare.html',{'safe':False});

def  Infostats (request):
        # cursor = connection.cursor()
        # sql = "INSERT INTO JOBS VALUES(%s,%s,%s,%s)"
        # cursor.execute(sql,['NEW_JOB','Something New',4000,8000])
        # connection.commit()
        # cursor.close()

        cursor = connection.cursor()
        sql = "SELECT * FROM REFEREE"
        cursor.execute(sql)
        result1 = cursor.fetchall()
        cursor.close()

        # cursor = connection.cursor()
        # sql = "SELECT * FROM JOBS WHERE MIN_SALARY=%s"
        # cursor.execute(sql,[4000])
        # result = cursor.fetchall()
        cursor = connection.cursor()
        sql = "SELECT * FROM PLAYER "
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()

        dict_both =[]
        dict_result1 = []
        dict_result2 = []

        for r in result1:
            referee_id = r[0]
            referee_name = r[1]
            match_controlled = r[2]
            row = {'referee_id':referee_id, 'referee_name':referee_name, 'match_controlled':match_controlled}
            dict_result1.append(row)
            
        for r2 in result2:
                player_id = r2[0]
                First_name = r2[1]
                Last_name = r2[2]
                Position = r2[3]
                Munutes_played = r2[4]
                Red_Card = r2[5]
                Yellow_card = r2[6]
                Country = r2[7]
                team_id = r2[8]
                row ={
                'player_id':player_id,
                'First_name':First_name,
                'Last_name':Last_name,
                'Position':Position,
                'Minutes_played':Munutes_played,
                'Red_card':Red_Card,
                'Yellow_card':Yellow_card,
                'Country':Country,
                'Team_id':team_id
                }
                dict_result2.append(row)
        dict_ch={'referee':dict_result1,'player':dict_result2}
            

        #return render(request,'list_jobs.html',{'jobs' : Job.objects.all()})
        return render(request,'list_referee.html',{'main_' : dict_ch})
