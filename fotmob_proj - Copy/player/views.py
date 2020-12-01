from django.shortcuts import render
from django.db import connection

# Create your views here.
def  SquadInfo(request,Team_id):
        cursor = connection.cursor()
        sql = "SELECT * FROM TEAM WHERE Team_id = %s"
        cursor.execute(sql,[Team_id])
        result1 = cursor.fetchall()
        cursor.close()

        dict1 = [] 
        for r in result1:
            Team_id = r[0]
            Team_name = r[1]
            short_name = r[2]
            row  = {'Team_id': Team_id,'Team_name': Team_name,'short_name':short_name}
            dict1.append(row);
    
        cursor = connection.cursor()
        sql = "SELECT COACH_ID,COACH_NAME FROM COACH WHERE COACH_id = %s" 
        cursor.execute(sql,[ Team_id])
        result1 = cursor.fetchall()
        cursor.close()

        coach= [] 
        for r in result1:
            coach_id = r[0]
            coach_name = r[1]
            
            row  = {'coach_id': coach_id,'coach_name': coach_name}
            coach.append(row);

        
        cursor = connection.cursor()
        sql = "SELECT POSITION FROM PLAYER WHERE Team_id = %s GROUP BY POSITION;"
        cursor.execute(sql,[Team_id])
        result2 = cursor.fetchall()
        cursor.close()
        pos =[]
        for p in result2:
                
                cursor = connection.cursor()
                sql = "SELECT FIRST_NAME || ' '|| LAST_NAME AS NAME ,PLAYER_ID  FROM PLAYER WHERE Team_id = %s and POSITION = %s ;"
                cursor.execute(sql,[Team_id,p[0]])
                result1 = cursor.fetchall()
                cursor.close()
                pl =[]
                for r in result1:
                    pl.append({'name':r[0],'id':r[1]})
                pos.append({
                'pos':p[0],
                'pl':pl
                })
        
        whole_content={'team_info':dict1,'coach':coach,'position':pos}
        return render(request,'Squad_info.html',{'squad_details' :whole_content});
        
        
def  CoachView(request,coach_id):
        cursor = connection.cursor()
        sql = "SELECT * FROM Coach WHERE Coach_id = %s"
        cursor.execute(sql,[ coach_id])
        result1 = cursor.fetchall()
        cursor.close()

        dict1 = [] 
        for r in result1:
            Coach_name = r[1]
            Leagues_won = r[2]
            Team_id = r[3]
            row  = {'Coach_name': Coach_name,'Leagues_won': Leagues_won}
            dict1.append(row);
        return render(request,'coach_info.html',{'coach_details' :dict1});
def  PlayerView(request,player_id):
        cursor = connection.cursor()
        sql = "SELECT * FROM PLAYER WHERE PLAYER_id = %s"
        cursor.execute(sql,[ player_id])
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
                'player_id':player_id,
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
        cursor.execute(sql,[ player_id])
        result2 = cursor.fetchall()
        cursor.close()
        goal = 0
        for r in result2:
                goal = r[0]
                
        dict2.append({'g': goal})
        dict3=[]
        cursor = connection.cursor()
        sql = "SELECT SUM(ASSIST) FROM SCORES  WHERE ASSIST_ID = %s GROUP BY ASSIST_ID"
        cursor.execute(sql,[ player_id])
        result3 = cursor.fetchall()
        cursor.close()
        asst = 0
        for r in result3:
                asst = r[0]
        dict3.append({'a': asst})
                
        return render(request,'player_info.html',{'player_details' :dict1,'goals':dict2,'assist':dict3});
