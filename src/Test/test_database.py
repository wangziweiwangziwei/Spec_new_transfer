import sqlite3
import time 
import random
conn=sqlite3.connect('C:/DataBase/PortSRF.db')
print"connect database successfully"

# print '-------------------------------------------------'
# for i in range(3):
#     conn.execute("INSERT INTO  ELEC_DISTRIBUTION    \
#             (TERMINALID,CENTERFREQUENCY ,BANDWIDTH ,COUNTS,INTERVALTIME, \
#             NX ,NY ,DLETA,DTIME,LONGITUDE, LATITUDE ,HEIGHT ,TRANSFERPOWER ,TRANSINDEX ) \
#             VALUES (1234,900,25,3,1,  \
#              0.01,0.01,0.01,'2016-5-4-19-11-04',114.420239, 30.515488, \
#             29,50,0.01)");
#
# conn.commit()
# print "Records created successfully-elec_distribute";

#
# cursor = conn.execute("SELECT * from ELEC_DISTRIBUTION ")
# for row in cursor:
#     for each in row :
#         print each,
#     print
#
# print '-------------------------------------------------'

#
# conn.execute("INSERT INTO  ROUTE    \
#             (TERMINALID,CENTERFREQUENCY ,BANDWIDTH ,DTIME, \
#             LONGITUDE, LATITUDE ,HEIGHT ,RECEIVEDPOWER ) \
#             VALUES (1234,900,25,'2016-2-27-19-12-09',114.420239, 30.515488,29,50)"
#             );
#
# conn.commit()
#
# print "Records created successfully-route";

#


cursor=conn.execute("select  statusInsert from Status")
# conn.commit()

for row in cursor:
    for each in row :
        print each,
    print

cursor=conn.execute("select  * from localroute")
# conn.commit()

for row in cursor:
    for each in row :
        print each,
    print


def ready_for_insert():
    cursor=conn.execute("select  statusInsert from Status")
    
    a=cursor.fetchone()
    if(a==None):
        return 1
                  
    elif(a[0]==0):
        return 2

    else:
        return 0

#
# count=0
# a=114.420239
# b=30.515488
# while(count<200):
#
#     status=ready_for_insert()
#     if(status==1 or status==2):
#
#         try:
#             for i in range(500):
#                 x=random.uniform(0.01,0.04)
#                 y=random.uniform(0.003,0.03)
#                 a=a+x*i
#                 b=b+y*i
#                 a=a%150
#                 b=b%130
#                 conn.execute("insert into Localroute(Longitude,Latitude)values(?,?)",(a,b));
#
#             conn.commit()
#
#         except sqlite3.OperationalError,e:
#             print e
#             time.sleep(0.001)
#             conn.commit()
#
#
#         if(status==1):
#             conn.execute("insert into status(statusInsert)values(1)");
#             conn.commit()
#         else:
#             conn.execute("UPDATE Status set statusInsert=1")
#             conn.commit()
#     elif(status==0):
#         print 'wait'
#         time.sleep(0.4)
#
#     count+=1

# conn.execute("Delete from Status where 1==1");
# conn.commit()
# cursor = conn.execute("SELECT * from LocalRoute")
# for row in cursor:
#     for each in row :
#         print each,
#     print
# conn.execute("insert into status(statusInsert)values(1)");
# conn.commit()
# cursor = conn.execute("SELECT statusInsert from Status")
# print cursor.fetchall()
#    

print '-------------------------------------------------'
#
#
# conn.execute("INSERT INTO  ABNORMAL    \
# (ABNORMALID ,BELONGING,LONGITUDE,LATITUDE,  \
# HEIGHT,CENTERFREQUENCY,BANDWIDTH,PARAMETER, \
# MODULATIONMODE,TRANSPOWER ,TRANSINDEX ,ACTIVITYDEGREE , \
# SERVICEATTRIBUTE,ISILLEGAL) \
# VALUES (1234, 'chinaNet',114.420239, 30.515488,29,900,25,1,1,50,0.01,0.1,11,1)");
#
#
# conn.commit()
# print "Records created successfully-ab";
#
#
# cursor = conn.execute("SELECT * from ABNORMAL")
# for row in cursor:
#     for each in row :
#         print each,
#     print
#
#
#
# print '-------------------------------------------------'
#
#
# for i in range(3):
#     conn.execute("INSERT INTO  REGISTEREDSTATION    \
#     (STATIONID,BELONGING,LONGITUDE, LATITUDE,HEIGHT,  \
#     STARTFREQ,ENDFREQ ,MAXTRANSPOWER,BANDWIDTH ,MODULATIONMODE, \
#     PARAMETER ,SERVICEATTRIBUTE,COVERAGERADIUS,ACTIVITYDEGREE) \
#     VALUES (1234,'hust',114.420239, 30.515488,29,100,900,50,25,1,1,1,4,0.1)");
#
# conn.commit()
# print "Records created successfully-registerStation";
#
#
# cursor = conn.execute("SELECT * from REGISTEREDSTATION ")
# for row in cursor:
#     for each in row :
#         print each,
#     print
#
#
# print '-------------------------------------------------'
#
#
# conn.execute("INSERT INTO  STATIONPROPERTY    \
# (STATIONID,BELONGING,LONGITUDE, LATITUDE,HEIGHT,  \
#  CENTERFREQUENCY,TRANSPOWER,TRANSINDEX,BANDWIDTH,MODULATIONMODE,\
#  PARAMETER,SERVICEATTRIBUTE,ACTIVITYDEGREE,ISILLEGALWORKING) \
# VALUES (1234,'hust',114.420239, 30.515488,29,900,50,0.01,25,1,1,1,0.1,1)");
#
# conn.commit()
# print "Records created successfully-curPro";
#
#
# cursor = conn.execute("SELECT * from STATIONPROPERTY ")
# for row in cursor:
#     for each in row :
#         print each,
#     print
#
# print '-------------------------------------------------'
#
#

conn.close()




