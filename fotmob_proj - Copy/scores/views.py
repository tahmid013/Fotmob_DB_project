from django.shortcuts import render
from django.db import connection


# Create your views here.
def ScoresView(request):
    cursor = connection.cursor()
    sql = "SELECT * FROM TEAM"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []
    for r in result:
        Team_id = r[0]
        Team_name = r[1]
        Short_name = r[2]
        row = {'Team_id':Team_id, 'Team_name':Team_name, 'Short_name':Short_name}
        dict_result.append(row)
    
    cursor = connection.cursor()
    sql = "SELECT * FROM TEAM"
    cursor.execute(sql)
    result2 = cursor.fetchall()
    cursor.close()

    dict_result = []
    for r in result2:
        Team_id = r[0]
        Team_name = r[1]
        Short_name = r[2]
        row = {'Team_id':Team_id, 'Team_name':Team_name, 'Short_name':Short_name}
        dict_result.append(row)
        
        
        
        
    return render(request,'scores_page.html',{'scores' : dict_result})
def GoalsView(request):
    cursor = connection.cursor()
    sql = "SELECT P.FIRST_NAME||' '||P.LAST_NAME AS FULL_name, T.TEAM_NAME ,SUM(goals) as total_goal FROM SCORES S  JOIN PLAYER P ON (S.SCORING_ID = P.PLAYER_ID) JOIN TEAM T ON (S.TEAM_ID = T.TEAM_ID) GROUP BY S.SCORING_ID,P.FIRST_NAME||' '||P.LAST_NAME,T.TEAM_NAME ORDER BY total_goal DESC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []
    for r in result:
        Full_name = r[0]
        Team_name = r[1]
        total_goal = r[2]
        row = {'Full_name':Full_name, 'Team_name':Team_name, 'total_goal':total_goal}
        dict_result.append(row)
    return render(request,'goal_page.html',{'stats' : dict_result})

def AssistsView(request):
    cursor = connection.cursor()
    sql = "SELECT P.FIRST_NAME||' '||P.LAST_NAME AS FULL_name, T.TEAM_NAME ,SUM(assist) as total_goal FROM SCORES S  JOIN PLAYER P ON (S.SCORE_ID = P.PLAYER_ID) JOIN TEAM T ON (S.TEAM_ID = T.TEAM_ID) GROUP BY S.SCORING_ID,P.FIRST_NAME||' '||P.LAST_NAME,T.TEAM_NAME ORDER BY total_goal DESC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
  
    dict_result = []
    for r in result:
        Full_name = r[0]
        Team_name = r[1]
        total_assist = r[2]
        row = {'Full_name':Full_name, 'Team_name':Team_name, 'total_assist':total_assist}
        dict_result.append(row)
    return render(request,'assist_page.html',{'stats' : dict_result})

def RedView(request):
    cursor = connection.cursor()
    sql = "    SELECT P.FIRST_NAME||' '||P.LAST_NAME AS FULL_name, T.TEAM_NAME ,RED_CARD FROM PLAYER P  JOIN TEAM T ON (P.TEAM_ID = T.TEAM_ID) ORDER BY RED_CARD DESC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    dict_result = []
    for r in result:
        Full_name = r[0]
        Team_name = r[1]
        total_red = r[2]
        row = {'Full_name':Full_name, 'Team_name':Team_name, 'total_red':total_red}
        dict_result.append(row)
    return render(request,'red_page.html',{'stats' : dict_result})
def YellowView(request):
    cursor = connection.cursor()
    sql = "SELECT P.FIRST_NAME||' '||P.LAST_NAME AS FULL_name, T.TEAM_NAME ,YELLOW_CARD FROM PLAYER P  JOIN TEAM T ON (P.TEAM_ID = T.TEAM_ID) ORDER BY YELLOW_CARD DESC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    dict_result = []
    for r in result:
        Full_name = r[0]
        Team_name = r[1]
        total_yellow = r[2]
        row = {'Full_name':Full_name, 'Team_name':Team_name, 'total_yellow':total_yellow}
        dict_result.append(row)
    return render(request,'yellow_page.html',{'stats' : dict_result})
