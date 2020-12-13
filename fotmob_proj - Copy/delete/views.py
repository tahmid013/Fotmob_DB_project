from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.db import connection

# Create your views here.
def  DeleteView  (request):
        return render(request,  'delete.html');
def  PlayerDelView(request):
        cursor = connection.cursor()
        sql = "SELECT P.PLAYER_ID,P.FIRST_NAME,P.LAST_NAME,P.POSITION,P.MINUTES_PLAYED,P.COUNTRY,(SELECT TEAM_NAME FROM TEAM T WHERE T.TEAM_ID = P.TEAM_ID ) FROM PLAYER P ;"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        dict=[]
        for r2 in result2:
                player_id = r2[0]
                First_name = r2[1]
                Last_name = r2[2]
                Position = r2[3]
                Minutes_played = r2[4]
                Country = r2[5]
                team_name = r2[6]
                row ={
                'player_id':player_id,
                'First_name':First_name,
                'Last_name':Last_name,
                'Position':Position,
                'Minutes_played':Minutes_played,
                
                'Country':Country,
                'Team_name':team_name
                }
                
                dict.append(row)
                name = 'PLAYER'
                list={'name':name}
                cont={'list':list,'type':dict}
       
        return render(request,  'del/player.html',{'cont': cont});
def  MatchDelView(request):
        cursor = connection.cursor()
        sql = "SELECT * FROM MATCH ;"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        dict=[]
        for r2 in result2:
                match_id = r2[0]
                date_ = r2[1]
                attendance = r2[2]
                
                row ={
                'match_id':match_id,
                'date_':date_,
                'attendance':attendance
                }
                
                dict.append(row)
                name = 'MATCH'
                list={'name':name}
                cont={'list':list,'type':dict}
       
        return render(request,  'del/match.html',{'cont': cont});
def  ScoreDelView(request):
        cursor = connection.cursor()
        sql = "SELECT S.SCORE_ID,S.GOALS,S.ASSIST,P1.FIRST_NAME ,P2.FIRST_NAME FROM SCORES S JOIN PLAYER P1 ON(S.SCORING_ID=P1.PLAYER_ID) JOIN PLAYER P2 ON(S.ASSIST_ID=P2.PLAYER_ID);"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        dict=[]
        for r2 in result2:
                score_id = r2[0]
                goals = r2[1]
                assist = r2[2]
                scorer_name = r2[3]
                assist_name = r2[4]
                row ={
                'score_id':score_id,
                'goals':goals,
                'assist':assist,
                'scorer_name':scorer_name,
                'assist_name':assist_name
                }
                
                dict.append(row)
                name = 'SCORES'
                list={'name':name}
                cont={'list':list,'type':dict}
       
        return render(request,  'del/score.html',{'cont': cont});
def  TeamDelView(request):
        cursor = connection.cursor()
        sql = "SELECT TEAM_ID,TEAM_NAME,SHORT_NAME FROM TEAM;"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        dict=[]
        for r2 in result2:
                id = r2[0]
                name = r2[1]
                s_name = r2[2]
                
                row ={
                'team_id':id,
                'team_name':name,
                's_name':s_name
                
                }
                
                dict.append(row)
                name = 'TEAM'
                list={'name':name}
                cont={'list':list,'type':dict}
       
        return render(request,  'del/team.html',{'cont': cont});
       
def  CoachDelView(request):
        cursor = connection.cursor()
        sql = "SELECT C.COACH_ID,C.COACH_NAME,C.LEAGUES_WON,T.TEAM_NAME FROM COACH C JOIN TEAM T ON (C.TEAM_ID = T.TEAM_ID)"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        dict=[]
        for r2 in result2:
                id = r2[0]
                name = r2[1]
                league_won = r2[2]
                t_name = r2[3]
                
                row ={
                'coach_id':id,
                'coach_name':name,
                'league_won' : league_won,
                'team_name':t_name
                
                }
                
                dict.append(row)
                name = 'COACH'
                list={'name':name}
                cont={'list':list,'type':dict}
       
        return render(request,  'del/coach.html',{'cont': cont});

def  UtilDelView  (request,x,y):
        if(x=='PLAYER'):
            
            cursor = connection.cursor()
            
            cursor.execute("call Pl_del_prc(%s)",[y])
            connection.commit()
            cursor.close()
            return render(request,  'del/success.html',);
        if(x=='MATCH'):
            cursor = connection.cursor()
            sql = "DELETE  FROM MATCH WHERE MATCH_ID = %s;"
            """
            sql = "DELETE FROM REDCARD WHERE MATCH_ID = %s;DELETE FROM YELLOWCARD WHERE MATCH_ID = %s;DELETE FROM SCORES WHERE MATCH_ID= %s;DELETE FROM MATCH WHERE MATCH_ID= %s;"
            """
            cursor.execute(sql,[y])
            connection.commit()
            cursor.close()
            return render(request,  'del/success.html',);
        if(x=='TEAM'):
            cursor = connection.cursor()
            sql = "DELETE  FROM TEAM WHERE TEAM_ID = %s;"
            """
            sql ="DELETE REDCARD WHERE T_ID = %s;DELETE YELLOWCARD WHERE T_ID = %s;DELETE SCORES WHERE TEAM_ID = %s;DELETE MATCH WHERE (HOME_ID = %s or AWAY_ID =%s);DELETE PLAYER WHERE TEAM_ID = %s;DELETE COACH WHERE TEAM_ID = %s;DELETE TEAM WHERE TEAM_ID = %s;"
            """

            cursor.execute(sql,[y])
            connection.commit()
            cursor.close()
            return render(request,  'del/success.html',);
        if(x=='COACH'):
            cursor = connection.cursor()
            sql = "DELETE  FROM COACH WHERE COACH_ID = %s;"
            cursor.execute(sql,[y])
            connection.commit()
            cursor.close()
            return render(request,  'del/success.html',);
        if(x=='SCORES'):
            cursor = connection.cursor()
            sql = "DELETE  FROM SCORES WHERE SCORE_ID = %s;"
            cursor.execute(sql,[y])
            connection.commit()
            cursor.close()
            return render(request,  'del/success.html',);
        else :
            return render(request,  'delete.html');
