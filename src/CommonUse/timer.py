
#coding=utf-8
from src.CommonUse.staticVar import staticVar
from src.CommonUse.connect import ServerCommunication
import struct 
import time 
import threading
import wx 

class Timer(threading.Thread):
    def __init__(self ,thread_upload ,thread_station):
        threading.Thread.__init__(self)
        
        self.count_heart=0
        
        self.thread_upload=thread_upload
        self.thread_station=thread_station

    
    def reConnect(self):
        '''stop all thread related to sock '''
        self.thread_upload.stop()
        self.thread_station.stop()
        
        
        staticVar.getSock().close()
        staticVar.getSockFile().close()
        
        self.thread_station.input1=[]
        staticVar.sock=0
        staticVar.sockFile=0
        
        serverCom=ServerCommunication() #实例化服务器连接对象
        while(1):
            try:
                serverCom.ConnectToServer(9000)
                staticVar.sock=serverCom.sock
                self.thread_station.sock=serverCom.sock 
                
                
            except Exception:
                wx.MessageBox('reConnect To Monitor Server Failure!', 
                           'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
            
   
            try:
                serverCom.ConnectToServer(9988)
                staticVar.sockFile=serverCom.sockFile
                self.thread_station.sockFile=serverCom.sockFile
                self.thread_upload.sockFile=serverCom.sockFile 
                break 
            except Exception:
                wx.MessageBox('reConnect To File Server Failure!', 
                           'Alert', wx.ICON_INFORMATION | wx.STAY_ON_TOP)
            time.sleep(5)
        
        self.thread_station.input1.append(staticVar.sock)
        self.thread_station.input1.append(staticVar.sockFile)
        
        
        ''' start all the thread '''
        
        self.thread_station.event.set()
        self.thread_upload.event.set()
        
          
          
    def run(self):
        while(1):
            print 'send heart_beat'
            staticVar.getSock().sendall(struct.pack("!B",0x55)) 
            staticVar.getSock().sendall(struct.pack("!B",0x66)) 
            time.sleep(15)
            
            if(staticVar.count_heat_beat>self.count_heart):
                self.count_heart+=1
                
                if(self.count_heart>10000):
                    self.count_heart=0
                staticVar.count_heat_beat=self.count_heart
            else:
                print 'not receive heart_beat'
                self.reConnect()
                
                
        


