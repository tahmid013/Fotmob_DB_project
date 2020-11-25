from django.shortcuts import render
from django.db import connection

# Create your views here.
def  PlayerInfo(request,Team_id):
        cursor = connection.cursor()
        sql = "SELECT * FROM TEAM WHERE Team_id = +" + Team_id
        cursor.execute(sql)
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
        sql = "SELECT * FROM PLAYER WHERE Team_id = %s"
        cursor.execute(sql,[Team_id])
        result2 = cursor.fetchall()
        cursor.close()
        dict2 =[]
        for r2 in result2:
                player_id = r2[0]
                
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
                dict2.append(row)
        whole_content={'team_info':dict1,'player':dict2}
        return render(request,'Player_info.html',{'Player_details' :whole_content});
