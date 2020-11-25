from django.shortcuts import render
from django.db import connection

# Create your views here.
def  HomepageView(request):
        return render(request, 'base.html');
def  TablePoint(request):
        cursor = connection.cursor()
        sql = "SELECT S.TEAM_ID,T.TEAM_NAME ,T.SHORT_NAME,3*SUM(GOALS)+SUM(ASSIST) AS pt FROM SCORES S JOIN TEAM T ON (S.TEAM_ID = T.TEAM_ID) GROUP BY S.TEAM_ID,T.TEAM_NAME,T.SHORT_NAME ORDER BY pt desc"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        dict = [] 
        for r in result:
            Team_id = r[0]
            Team_name = r[1]
            Short_name = r[2]
            Point = r[3]
            row  = {'Team_id': Team_id,'Team_name': Team_name,'Short_name':Short_name,'Point':Point}
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
