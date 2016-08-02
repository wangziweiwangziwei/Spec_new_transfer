#coding=utf-8

import usb 

class staticVar:
    terminal_id=0x01
        #0x01
    outPoint=0
        #0x81 fft and ab
    inPointFFT=0
        #0x82 iq
    inPointIQ=0
        #0x83 query receive 
    inPointRecv=0
    
    sock=0
    sockFile=0
    
    #####  这个是用来记录心跳发过来的次数 ####
    count_heart_beat=0

    #####  记录接收增益 对于定频中的接收增益如果相同不进行第二次下发  #######
    recv_gain=7

    @classmethod
    def getRecvGain(cls):
        return cls.recv_gain

    @classmethod
    def setRecvGain(cls,recv_gain):
        cls.recv_gain=recv_gain

        
    @classmethod
    def getid(cls):
        return cls.terminal_id
    @classmethod
    def setid(cls,id_for):
        cls.terminal_id=id_for 
    @classmethod
    def initPort(cls):
        dev = usb.core.find(idVendor=0x04b4, idProduct=0x00f1)
        cfg=dev[0]
        intf=cfg[(0,0)]
        
        cls.outPoint=intf[0]
        cls.inPointFFT=intf[1]
        cls.inPointIQ=intf[3]
        cls.inPointRecv=intf[5]
    
    @classmethod
    def initSock(cls,sock):
        cls.sock=sock
    
    @classmethod 
    def initSockFile(cls,sockFile):
        cls.sockFile=sockFile
    @classmethod
    def getFreq(cls):
        ListFreq={0:(98,20),1:(947.5,25),2:(1842.5,75),3:(875,10),4:(1890,20),5:(2345,50), \
                       6:(2605,60),7:(2137.5,15),8:(2310,20),9:(2565,20),10:(2117.5,15),11:(2380,20),  \
                       12:(2645,20),13:(1865,30),14:(2157.5,25),15:(433.92,1.74),16:(915,26),  \
                       17:(2451.75,63.5),18:(5787.5,125)}
        
        return ListFreq
    @classmethod
    def getCentreFreq(cls):
        List=[u"FM调频广播频段",u"GSM下行频段1",u"GSM下行频段2",u"IS95 CDMA 下行频段",u"TD 3G频段",u"TD LTE 频段1",
        u"TD LTE 频段2",u"WCDMA 下行频段",u"联通TDLTE 频段1",u"联通TDLTE 频段2",u"CDMA 2000 下行频段",u"电信TDLTE频段1",
        u"电信TDLTE频段2",u"LTE FDD 频段1",u"LTE FDD 频段2",u"ISM 433M频段",u"ISM 工业频段",u"ISM科研频段",u"ISM医疗频段"]
        
        return List 
    @classmethod
    def getdictFreqPlan(cls):
        
        dictFreqPlan={1:u"固定",2:u"移动",3:u"无线电定位",4:u"卫星固定",5:u"空间研究",6:u"卫星地球探测",
              7:u"射电天文",8:u"广播",9:u"移动(航空移动除外)",10:u"无线电导航",11:u"航空无线电导航",
              12:u"水上移动",13:u"卫星移动",14:u"卫星间",15:u"卫星无线电导航",16:u"业余",17:u"卫星气象",18:u"标准频率和时间信号",
              19:u"空间操作",20:u"航空移动",21:u"卫星业余",22:u"卫星广播",23:u"航空移动(OR)",
              24:u"气象辅助",25:u"航空移动(R)",26:u"水上无线电导航",27:u"陆地移动",28:u"移动(航空移动(R)除外)",
              29:u"卫星无线电测定",30:u"卫星航空移动(R)",31:u"移动(航空移动(R)除外)",32:u"水上移动(遇险和呼叫)",
              33:u"水上移动(使用DSC的遇险和安全呼叫)",34:u"未划分"}
        return dictFreqPlan
    
    @classmethod
    def getDemodType(cls):
        List=["AM","FM",'DSB','LSB','USB','VSB','AM-FM','FMCW','FMICW','PM','2ASK','4ASK','2FSK','4FSK','BPSK','QPSK']
        
        return List 
    
    @classmethod
    def getSock(cls):
        return cls.sock 
    
    @classmethod
    def getSockFile(cls):
        
        return cls.sockFile        
    
    
if __name__=='__main__':
#     staticVar.setid(12) #初始化id
        
    print staticVar.getid()
    
    
    