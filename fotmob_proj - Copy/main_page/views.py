from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.db import connection

# Create your views here.
def  Res():
        cursor = connection.cursor()
        sql = "SELECT  GETRESULT(MATCH_ID) ,MATCH_ID FROM MATCH WHERE GETRESULT(MATCH_ID) <> 'NULL' ORDER BY DATE_ DESC;"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        whole_content = []
        
        for r in result2:
            
            score_list = r[0].split(',')
            print (score_list);
            match_date = score_list[0]
            h_path = score_list[1]
            h_name = score_list[2]
            h_id = score_list[3]
            h_goals = score_list[4]
            a_goals =score_list[5]
            
            a_name =score_list[6]
            a_path = score_list[7]
            a_id =score_list[8]
            m_id = r[1]
            row  = {'t1_id':h_id,'t2_id':a_id,'m_id':m_id,'m_date':match_date,'h_name':h_name,'h_goals':h_goals,'a_name':a_name,'a_goals':a_goals,'h_path':h_path,'a_path':a_path}
            whole_content.append(row);
        return whole_content;
def  HomepageView(request):
        username = ""
        if request.session.has_key('member_id'):
                username = request.session['member_id']
                
                
                
        
        whole_content = Res()
                
        

        return render(request, 'base.html',{'user':username,'matches':whole_content});
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
        whole_content = Res();
        return render(request, 'base.html',{'user':username,'matches':whole_content});

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
            request.session.set_expiry(1200)
            whole_content = Res();
            return render(request, 'base.html',{'user':username,'matches':whole_content});
            """return TemplateResponse(request, 'base.html', { 'user': username});"""
        else:
            return render(request, 'loginfailed.html');
    else:
        return render(request, 'loginPage.html');
def  TablePoint(request):
        cursor = connection.cursor()
        sql = "SELECT T.TEAM_ID,T.TEAM_NAME ,T.SHORT_NAME,Win(S.TEAM_ID) AS W,Draw(S.TEAM_ID) AS D,Lose(S.TEAM_ID) AS L,T.FLAG FROM TEAM T  LEFT JOIN SCORES S ON (S.TEAM_ID = T.TEAM_ID) GROUP BY S.TEAM_ID,T.TEAM_NAME,T.SHORT_NAME,T.FLAG,T.TEAM_ID ORDER BY W+D+L DESC"
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
            flag_path = r[6]
            row  = {'Team_id': Team_id,'Team_name': Team_name,'Short_name':Short_name,'Played':PL,'Point':Point,'Win':W,'Draw':D,'Lose':L,'flag_path':flag_path}
            dict.append(row);
        return render(request,'table_point.html',{'table' :dict});
def  TeamInfo(request ,Team_id):
        print(Team_id);
        cursor = connection.cursor()
        sql = "SELECT * FROM TEAM WHERE Team_id = %s;" 
        cursor.execute(sql,[Team_id])
        result = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        sql = "SELECT GetGoal3(%s,MATCH_ID),MATCH_ID FROM MATCH WHERE HOME_ID =%s or AWAY_ID =%s ORDER BY DATE_ DESC;"
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
        score_list=[]
        for r in result2:
            if(r[0] != "NULL"):
                score_list = r[0].split(',')
                match_date = score_list[0]
                h_name = score_list[1]
                h_id = score_list[2]
                h_goals = score_list[3]
                a_goals =score_list[4]
                
                a_name =score_list[5]
                a_id =score_list[6]
                wl = score_list[7]
                m_id = r[1]
            row  = {'t1_id':h_id,'t2_id':a_id,'m_id':m_id,'m_date':match_date,'h_name':h_name,'h_goals':h_goals,'a_name':a_name,'a_goals':a_goals,'wl':wl}
            dict2.append(row);
        
        
        
        
        whole_content={'team_info':dict1,'result':dict2,}

        return render(request,'Team_info.html',{'content' :whole_content});
def  Match_Dt_View(request,Team_1_id,Team_2_id,Matchid):

        cursor = connection.cursor()
        sql = "SELECT R.RC_NO, (SELECT FIRST_NAME||' '|| LAST_NAME FROM PLAYER WHERE PLAYER_ID =R.PL_ID)   FROM REDCARD R WHERE R.T_ID= %s AND R.MATCH_ID = %s;"
        cursor.execute(sql,[Team_1_id,Matchid])
        r_t1 = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        sql = "SELECT Y.YC_NO, (SELECT FIRST_NAME||' '|| LAST_NAME FROM PLAYER WHERE PLAYER_ID =Y.PL_ID)   FROM YELLOWCARD Y WHERE Y.T_ID= %s  AND Y.MATCH_ID = %s;"
        cursor.execute(sql,[Team_1_id,Matchid])
        y_t1 = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        sql = "SELECT R.RC_NO, (SELECT FIRST_NAME||' '|| LAST_NAME FROM PLAYER WHERE PLAYER_ID =R.PL_ID)   FROM REDCARD R WHERE R.T_ID= %s AND R.MATCH_ID = %s;"
        cursor.execute(sql,[Team_2_id,Matchid])
        r_t2 = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        sql = "SELECT Y.YC_NO, (SELECT FIRST_NAME||' '|| LAST_NAME FROM PLAYER WHERE PLAYER_ID =Y.PL_ID)   FROM YELLOWCARD Y WHERE Y.T_ID= %s  AND Y.MATCH_ID = %s;"
        cursor.execute(sql,[Team_2_id,Matchid])
        y_t2 = cursor.fetchall()
        cursor.close()
        
        t1_red_list=[]
        t2_red_list=[]
        t1_yel_list=[]
        t2_yel_list=[]
        
        for r in r_t1:
            Name = r[1]
            card_no = r[0]
            t1_red_list.append({'name':Name,'card_no':card_no})
        for r in r_t2:
            Name = r[1]
            card_no = r[0]
            t2_red_list.append({'name':Name,'card_no':card_no})
        for r in y_t1:
            Name = r[1]
            card_no = r[0]
            t1_yel_list.append({'name':Name,'card_no':card_no})
        for r in y_t2:
            Name = r[1]
            card_no = r[0]
            t2_yel_list.append({'name':Name,'card_no':card_no})
        
        cursor = connection.cursor()
        sql = "SELECT GetGoal3(%s,%s),(SELECT R.REFEREE_NAME FROM REFEREE R WHERE R.REFEREE_ID = M.REFEREE_ID) FROM MATCH M WHERE M.MATCH_ID = %s;"
        cursor.execute(sql,[Team_1_id,Matchid,Matchid])
        result2 = cursor.fetchall()
        cursor.close()
        
        whole_content = []
        dict2 = []
        for r in result2:
            if(r != "NULL"):
                score_list = r[0].split(',')
                match_date = score_list[0].split(' ')
                date = match_date[0]
                time = match_date[1]
                
                h_name = score_list[1]
                h_id = score_list[2]
                h_goals = score_list[3]
                a_goals =score_list[4]
                a_name =score_list[5]
                a_id =score_list[6]
                ref_name= r[1]
                row  = {'t1_id':h_id,'t2_id':a_id,'date':date,'time':time,'h_name':h_name,'h_goals':h_goals,'a_name':a_name,'a_goals':a_goals,'ref_name':ref_name}
                dict2.append(row);
        whole_content={'result':dict2}
        
        return render(request,'Match_details.html',{'content' :dict2,'t1_r':t1_red_list,'t2_r':t2_red_list,'t1_y':t1_yel_list,'t2_y':t2_yel_list});
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
            sql = "SELECT FIRST_NAME||' '||LAST_NAME,Position,Minutes_played,NVL((SELECT SUM(RC_NO) FROM REDCARD WHERE PL_ID = PLAYER_ID GROUP BY PL_ID ),0),NVL((SELECT SUM(YC_NO) FROM YELLOWCARD WHERE PL_ID = PLAYER_ID GROUP BY PL_ID ),0),COUNTRY FROM PLAYER WHERE PLAYER_id = %s"
            cursor.execute(sql,[ player1_id])
            result1 = cursor.fetchall()
            cursor.close()
            
           

            dict1 = [] 
            for r2 in result1:
                    Name = r2[0]
                    Position = r2[1]
                    Minutes_played = r2[2]
                    Red_Card = r2[3]
                    Yellow_card = r2[4]
                    Country = r2[5]
                    row ={
                    'Name':Name,
                    'Position':Position,
                    'Minutes_played':Minutes_played,
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
            sql = "SELECT FIRST_NAME||' '||LAST_NAME,Position,Minutes_played,NVL((SELECT SUM(RC_NO) FROM REDCARD WHERE PL_ID = PLAYER_ID GROUP BY PL_ID ),0),NVL((SELECT SUM(YC_NO) FROM YELLOWCARD WHERE PL_ID = PLAYER_ID GROUP BY PL_ID ),0),COUNTRY FROM PLAYER WHERE PLAYER_id = %s"
            cursor.execute(sql,[ player2_id])
            result1 = cursor.fetchall()
            cursor.close()
            
           

            dict1 = [] 
            for r2 in result1:
                    Name = r2[0]
                    Position = r2[1]
                    Munutes_played = r2[2]
                    Red_Card = r2[3]
                    Yellow_card = r2[4]
                    Country = r2[5]
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
       
        cursor = connection.cursor()
        sql = "SELECT * FROM REFEREE"
        cursor.execute(sql)
        result1 = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        sql = "SELECT FIRST_NAME,LAST_NAME,Position,Minutes_played,NVL((SELECT SUM(RC_NO) FROM REDCARD WHERE PL_ID = PLAYER_ID GROUP BY PL_ID ),0),NVL((SELECT SUM(YC_NO) FROM YELLOWCARD WHERE PL_ID = PLAYER_ID GROUP BY PL_ID ),0),COUNTRY,TEAM_ID FROM PLAYER WHERE PLAYER_id = %s"
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
                First_name = r2[0]
                Last_name = r2[1]
                Position = r2[2]
                Munutes_played = r2[3]
                Red_Card = r2[4]
                Yellow_card = r2[5]
                Country = r2[6]
                team_id = r2[7]
                row ={
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
