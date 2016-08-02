# -*- coding: utf-8 -*-
############ insert into the database ###############
import threading 
import sqlite3 
import time 
class InsertRouteThread(threading.Thread): 
    def __init__(self,mainframe):
        threading.Thread.__init__(self)
        self.event = threading.Event()  
        self.event.set()
        self.conn=sqlite3.connect('C:/DataBase/PortSRF.db', check_same_thread = False)
        
        self.queueRouteMap=mainframe.queueRouteMap
        
        self.count_for_execute=0

    
    def stop(self):
        self.event.clear()
        self.clear_database()
    
    def clear_database(self):
        self.conn.execute("delete from localroute where 1==1");
        self.conn.execute("delete from Status where 1==1");
        self.conn.commit()
        
        
    def total_rows(self):
        
        cursor=self.conn.execute('SELECT COUNT(*) FROM LocalRoute')
        count = cursor.fetchall()
        
#         print('\nTotal rows: {}'.format(count[0][0]))
        return count[0][0]
    
    def ready_for_insert(self):
        cursor=self.conn.cursor()
        count=0
        while(count<5):
            try:

                cursor.execute("select  statusInsert from Status")
                break
            except sqlite3.OperationalError,e:
                time.sleep(1)
                count+=1

        if(count==5):
            return 0
                
        # print cursor
        # print type(cursor)
        # for row in cursor:
        #     for each in row:
        #         print each,
        #         print

        a=cursor.fetchone()
        if(a==None):
            return 1

        elif(a[0]==0):
            return 2

        else:
            return 0

    def run(self):
        while(1):
            self.event.wait()
            status=self.ready_for_insert()
            if(status==1 or status==2):
                # print status
                while(not self.queueRouteMap.empty()):

                    Pos=self.queueRouteMap.get()
                    self.conn.execute("insert into LocalRoute(LONGITUDE,LATITUDE) VALUES \
                                       (?,?)",(Pos[0],Pos[1]));
                    self.count_for_execute+=1
                    if(self.count_for_execute==50):
                        self.count_for_execute=0

                        self.conn.commit()
                        # except sqlite3.OperationalError,e:
                            # print e /\
                        
                        if(status==1):
                            try:
                                self.conn.execute("insert into status(statusInsert)values(1)");
                                self.conn.commit()
                            except sqlite3.OperationalError,e:
                                time.sleep(0.1)
                                self.conn.execute("insert into status(statusInsert)values(1)");
                                self.conn.commit()
                        else:
                            try:
                                self.conn.execute("UPDATE Status set statusInsert=1")
                                self.conn.commit()
                            except sqlite3.OperationalError,e:
                                time.sleep(0.1)
                                self.conn.execute("UPDATE Status set statusInsert=1")
                                self.conn.commit()
                        
                        time.sleep(1)
                        break  ##此处不break就会继续执行conn.execute(),造成sqlite busy 问题
            elif(status==0):
                print 'wait'
                time.sleep(2)
                    
                    
                    

