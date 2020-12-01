from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse

from django.db import connection
# Create your views here.
def  InsertView  (request):
    
        return render(request,  'insert.html');
def  PlayerInsView(request):
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
            
            cursor = connection.cursor()
            sql = 'SELECT FIRST_NAME, LAST_NAME FROM PLAYER;'
            cursor.execute(sql)
            player_data = cursor.fetchall()
            cursor.close()
            
            if(first_name == "" or last_name == "" or position == "" or min_played == "" or r_card == "" or y_card == "" or country == "" ):
                    flag = True
            
            for r  in player_data:
                if(r[0] == first_name and r[1] == last_name):
                    flag = True
                    break
            
            if(flag == False):
                cursor = connection.cursor()
                sql = 'INSERT INTO PLAYER(First_name,Last_name,Position,Minutes_played,Red_card,Yellow_card,Country,Team_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);'
                cursor.execute(sql,[first_name,last_name,position,min_played,r_card,y_card,country,team_id])
                connection.commit()
                cursor.close()
            name = 'player'
            if(flag == True):
                return render(request, 'ins/failed.html',{'type':name});
            if(flag == False):
                return render(request, 'ins/success.html',{'type':name});
        else:
            return render(request, 'ins/player.html');
def  MatchInsView(request):
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
                
                sql = 'INSERT INTO MATCH(Date_,Attendance,Referee_id,Stadium_id,Home_id,Away_id) VALUES (TO_DATE(%s,%s),%s,%s,%s,%s,%s);'
                cursor.execute(sql,[date,date_format,attendance,ref_id,st_id,h_id,a_id])
                connection.commit()
                cursor.close()
            name = 'match'
            if(flag == True):
                return render(request, 'ins/failed.html',{'type':name});
            if(flag == False):
                return render(request, 'ins/success.html',{'type':name});
        else:
            return render(request, 'ins/match.html');
        
def  ScoreInsView(request):
        if(request.method == 'POST'):
            goals = request.POST['goals']
            assist = request.POST['assist']
            scoring_name = request.POST['scoring_name']
            assist_name = request.POST['assist_name']
            team_name = request.POST['team_name']
            match_date = request.POST['match_date']
            stadium_name = request.POST['stadium_name']
            
            sc_id=-1
            as_id=-1
            t_id=-1
            m_id = -1
            
            cursor = connection.cursor()
            sql = "SELECT  PLAYER_ID FROM PLAYER WHERE (First_name||' '||Last_name = %s);"
            cursor.execute(sql,[scoring_name])
            result = cursor.fetchall()
            cursor.close()
   
            for r in result:
                sc_id = r[0]
            
            cursor = connection.cursor()
            sql = "SELECT  PLAYER_ID FROM PLAYER WHERE (First_name||' '||Last_name = %s);"
            cursor.execute(sql,[assist_name])
            result = cursor.fetchall()
            cursor.close()
   
            for r in result:
                as_id= r[0]
            
            cursor = connection.cursor()
            sql = 'SELECT  TEAM_ID FROM TEAM WHERE (SHORT_NAME = %s);'
            cursor.execute(sql,[team_name])
            result = cursor.fetchall()
            cursor.close()
   
            for r in result:
                t_id = r[0]            
            
            cursor = connection.cursor()
            date_format = 'yyyy-mm-dd hh24:mi:ss'
            sql = 'SELECT  MATCH_ID FROM MATCH M JOIN STADIUM S ON (M.STADIUM_ID = S.STADIUM_ID) WHERE (M.DATE_ = TO_DATE(%s,%s) and S.STADIUM_NAME = %s);'
            cursor.execute(sql,[match_date,date_format,stadium_name])
            result = cursor.fetchall()
            cursor.close()
   
            for r in result:
                m_id = r[0]
            
            flag = False;
            
           
            if( goals == "" or assist == ""  or sc_id==-1 or as_id==-1 or  t_id==-1 or m_id==-1):
                    flag = True
            
            if(goals == 0 and assist!=""):
                    flag = True
            if(goals == 0 and assist==""):
                    flag = False
            
            if(flag == False):
                if(goals != 0):
                    cursor = connection.cursor()
                    sql = 'INSERT INTO SCORES(GOALS,ASSIST,SCORING_ID,ASSIST_ID,MATCH_ID,TEAM_ID) VALUES(%s,%s,%s,%s,%s,%s);'
                    cursor.execute(sql,[goals,assist,sc_id,as_id,m_id,t_id])
                    connection.commit()
                    cursor.close()
                else:
                    cursor = connection.cursor()
                    sql = 'INSERT INTO SCORES(GOALS,ASSIST,SCORING_ID,MATCH_ID,TEAM_ID) VALUES(%s,%s,%s,%s,%s);'
                    cursor.execute(sql,[goals,assist,sc_id,m_id,t_id])
                    connection.commit()
                    cursor.close()
            name = 'scores_ins'
            if(flag == True):
                return render(request, 'ins/failed.html',{'type':name});
            if(flag == False):
                return render(request, 'ins/success.html',{'type':name});
        else:
            return render(request, 'ins/score.html');
def  TeamInsView(request):
        if(request.method == 'POST'):
            team_name = request.POST['t_name']
            short_name = request.POST['s_name']
            
            
            flag = True;
            
            cursor = connection.cursor()
            sql = 'SELECT TEAM_NAME, SHORT_NAME FROM TEAM;'
            cursor.execute(sql)
            team_data = cursor.fetchall()
            cursor.close()
            
            if(team_name == "" or short_name == "" ):
                    flag = True
            
            for r  in team_data:
                if(r[0] == team_name and r[1] == short_name):
                    flag = True
                    break
            
            if(flag == False):
                cursor = connection.cursor()
                sql = 'INSERT INTO TEAM(TEAM_NAME,SHORT_NAME) VALUES(%s,%s);'
                cursor.execute(sql,[team_name,short_name])
                connection.commit()
                cursor.close()
            name = 'team'
            if(flag == True):
                return render(request, 'ins/failed.html',{'type':name});
            if(flag == False):
                return render(request, 'ins/success.html',{'type':name});
        else:
            return render(request, 'ins/team.html');
        return render(request, 'ins/team.html');
def  CoachInsView(request):
       
        return render(request, 'ins/coach.html');
def  RefereeInsView(request):
       
        return render(request, 'ins/referee.html');
def  StadiumInsView(request):
       
        return render(request, 'ins/stadium.html');