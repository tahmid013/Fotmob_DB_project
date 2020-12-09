from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def UpdateView  (request):
        return render(request,  'update.html');
def PlView (request,pl_id):
        if(request.method == 'POST'):
            first_name = request.POST['f_name']
            last_name = request.POST['l_name']
            position = request.POST['position']
            min_played = request.POST['min_played']
            r_card = request.POST['r_card']
            y_card = request.POST['y_card']
            country = request.POST['Country']
            team_sn = request.POST['team']
            
            cursor = connection.cursor()
            sql = 'SELECT SHORT_NAME ,TEAM_ID FROM TEAM;'
            cursor.execute(sql)
            check_team = cursor.fetchall()
            cursor.close()
            
            flag = True;
            team_id ="";
            for team in check_team:
                if(team[0] == team_sn):
                    team_id = team[1]
                    flag = False;
                    break;
            
            
            
            if(first_name == "" or last_name == "" or position == "" or min_played == "" or r_card == "" or y_card == "" or country == "" ):
                    flag = True
            
            
            
            if(flag == False):
                cursor = connection.cursor()
                sql = 'UPDATE PLAYER SET First_name =%s,Last_name=%s,Position=%s,Minutes_played=%s,Red_card=%s,Yellow_card=%s,Country=%s,Team_id=%s WHERE PLAYER_ID = %s;'
                cursor.execute(sql,[first_name,last_name,position,min_played,r_card,y_card,country,team_id,pl_id])
                connection.commit()
                cursor.close()
            name = 'player_d'
            if(flag == True):
                return render(request, 'upd/failed.html',{'type':name});
            if(flag == False):
                return render(request, 'upd/success.html',{'type':name});
        else:
            cursor = connection.cursor()
            sql = "SELECT * FROM PLAYER WHERE PLAYER_ID = %s ;"
            cursor.execute(sql,[pl_id])
            result2 = cursor.fetchall()
            cursor.close()
            player_id = ""
            First_name = ""
            Last_name = ""
            Position = ""
            Munutes_played = ""
            Red_Card = ""
            Yellow_card = ""
            Country = ""
            team_id = ""
            
            for r2 in result2:
                    
                    First_name = r2[1]
                    Last_name = r2[2]
                    Position = r2[3]
                    Munutes_played = r2[4]
                    Red_Card = r2[5]
                    Yellow_card = r2[6]
                    Country = r2[7]
                    team_id = r2[8]
            d = []
            cursor = connection.cursor()
            sql = "SELECT SHORT_NAME FROM TEAM WHERE TEAM_ID = %s ;"
            cursor.execute(sql,[team_id])
            res = cursor.fetchall()
            cursor.close()
            t_name = ""
            for r in res:
                t_name = r[0]
            
            row ={
            'First_name':First_name,
            'Last_name':Last_name,
            'Position':Position,
            'Minutes_played':Munutes_played,
            'Red_card':Red_Card,
            'Yellow_card':Yellow_card,
            'Country':Country,
            'Team_name':t_name
            }
                
            
            return render(request,  'upd/player.html',{'row': row});
def MtView(request,m_id):
        if(request.method == 'POST'):
            date = request.POST['date']
            attendance = request.POST['attendance']
            referee_name = request.POST['referee_name']
            stadium_name = request.POST['stadium_name']
            home_t = request.POST['home_t']
            away_t = request.POST['away_t']
            
            ref_id=-1
            st_id=-1
            h_id=-1
            a_id=-1
            
            cursor = connection.cursor()
            sql = 'SELECT  M.REFEREE_ID FROM MATCH M JOIN REFEREE R ON(M.REFEREE_ID = R.REFEREE_ID) WHERE R.REFEREE_NAME = %s;'
            cursor.execute(sql,[referee_name])
            result = cursor.fetchall()
            cursor.close()
   
            for r in result:
                ref_id = r[0]
            
            cursor = connection.cursor()
            sql = 'SELECT  M.STADIUM_ID FROM MATCH M JOIN STADIUM S ON(M.STADIUM_ID = S.STADIUM_ID) WHERE S.STADIUM_NAME = %s;'
            cursor.execute(sql,[stadium_name])
            result = cursor.fetchall()
            cursor.close()
   
            for r in result:
                st_id = r[0]
                
            cursor = connection.cursor()
            sql = 'SELECT  M.HOME_ID FROM MATCH M JOIN TEAM T ON(M.HOME_ID = T.TEAM_ID) WHERE T.SHORT_NAME = %s;'
            cursor.execute(sql,[home_t])
            result = cursor.fetchall()
            cursor.close()
   
            for r in result:
                h_id = r[0]
            
            cursor = connection.cursor()
            sql = 'SELECT  M.AWAY_ID FROM MATCH M JOIN TEAM T ON(M.AWAY_ID = T.TEAM_ID) WHERE T.SHORT_NAME = %s;'
            cursor.execute(sql,[away_t])
            result = cursor.fetchall()
            cursor.close()
   
            for r in result:
                a_id = r[0]
                        
                        
                        
            flag = False;
            
           
            if( date == "" or attendance == ""  or ref_id==-1 or st_id==-1 or  h_id==-1 or a_id==-1):
                    flag = True
            
            
            
            if(flag == False):
                date_format = 'yyyy-mm-dd hh24:mi:ss'
                cursor = connection.cursor()
                
                sql = 'UPDATE  MATCH SET Date_ =TO_DATE(%s,%s),Attendance=%s,Referee_id=%s,Stadium_id=%s,Home_id=%s,Away_id=%s WHERE MATCH_ID =%s;'
                cursor.execute(sql,[date,date_format,attendance,ref_id,st_id,h_id,a_id,m_id])
                connection.commit()
                cursor.close()
            name = 'match_d'
            if(flag == True):
                return render(request, 'ins/failed.html',{'type':name});
            if(flag == False):
                return render(request, 'ins/success.html',{'type':name});
        else:
            cursor = connection.cursor()
            sql = "SELECT TO_CHAR(M.DATE_,'yyyy-mm-dd hh24:mi:ss'),M.ATTENDANCE,(SELECT REFEREE_NAME FROM REFEREE WHERE REFEREE_ID = M.REFEREE_ID),(SELECT STADIUM_NAME FROM STADIUM WHERE STADIUM_ID = M.STADIUM_ID),(SELECT SHORT_NAME FROM TEAM WHERE TEAM_ID = M.HOME_ID),(SELECT SHORT_NAME FROM TEAM WHERE TEAM_ID = M.AWAY_ID) FROM MATCH M WHERE M.MATCH_ID = %s ;"
            cursor.execute(sql,[m_id])
            result2 = cursor.fetchall()
            cursor.close()
            date = ""
            attendance = ""
            r_name = ""
            s_name = ""
            h_name = ""
            a_name = ""
            
            for r2 in result2:
                    
                    date = r2[0]
                    attendance = r2[1]
                    r_name = r2[2]
                    s_name = r2[3]
                    h_name = r2[4]
                    a_name = r2[5]
                    
                    
            
            row ={
            'date':date,
            'attendance':attendance,
            'r_name':r_name,
            's_name':s_name,
            'h_name':h_name,
            'a_name':a_name
            
            }
            return render(request,  'upd/match.html',{'row': row});
      
def SView(request,s_id):
        return render(request,  'upd/player.html');
def RView(request,r_id):
        return render(request,  'upd/referee.html');
def CView(request,c_id):
        if(request.method == 'POST'):
            coach_name = request.POST['coach_name']
            league_won = request.POST['league_won']
            team_name = request.POST['team_name']
            
            flag = False;
            t_id = -1
            cursor = connection.cursor()
            sql = 'SELECT TEAM_ID FROM TEAM WHERE SHORT_NAME = %s;'
            cursor.execute(sql,[team_name])
            team_data = cursor.fetchall()
            cursor.close()
            
            
            
            if(team_name == "" or coach_name == "" or league_won == ""):
                    flag = True
            
            
            for r in team_data:
                t_id = r[0]
            if(flag == False):
                cursor = connection.cursor()
                sql = 'UPDATE COACH SET COACH_NAME =%s,LEAGUES_WON=%s,TEAM_ID=%s WHERE COACH_ID = %s;'
                cursor.execute(sql,[coach_name,league_won,t_id,c_id])
                connection.commit()
                cursor.close()
            name = 'coach_d'
            if(flag == True):
                return render(request, 'ins/failed.html',{'type':name});
            if(flag == False):
                return render(request, 'ins/success.html',{'type':name});
        else:
            cursor = connection.cursor()
            sql = "SELECT COACH_NAME,LEAGUES_WON,(SELECT SHORT_NAME FROM TEAM WHERE TEAM_ID = C.TEAM_ID) FROM COACH C WHERE C.COACH_ID = %s ;"
            cursor.execute(sql,[c_id])
            result2 = cursor.fetchall()
            cursor.close()
            name = ""
            lg_won = ""
            team_name = ""
            
            
            for r2 in result2:
                    
                    name = r2[0]
                    lg_won = r2[1]
                    team_name = r2[2]
            
            row ={
            'name':name,
            'lg_won':lg_won,
            'team_name':team_name,
            
            }
            return render(request,  'upd/coach.html',{'row': row});
def TView(request,t_id):
        return render(request,  'upd/player.html');
