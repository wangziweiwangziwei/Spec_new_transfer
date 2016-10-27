# -*- coding: utf-8 -*-

from src.Package.package import *
from src.CommonUse.staticVar import staticVar

###########下面是接收字节转结构体对象###########

class ByteToPackage():
    def __init__(self):
        self.inPointFFT=staticVar.inPointFFT
        self.inPointRecv=staticVar.inPointRecv
        self.inPointIQ=staticVar.inPointIQ
    def ReceiveFFT(self):
        li=list(self.inPointFFT.read(2000,100))
        # if(li[1]==82 and len(li)!=1564):
        #     print len(li)


        if (not len(li) == 1564):
            if (len(li) == 80):
                poa_data_obj = self.ByteToPoaData(li)
                return poa_data_obj
            
            else:
                return 0
        specObj=SpecDataRecv()
        specObj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        specObj.LonLatAlti=LonLatAltitude(li[4],li[5],li[6],li[7],li[8]>>7, \
                                        li[8]&0x7F,li[9],li[10],li[11]>>7,  \
                                        li[11]&0x7F,li[12])
       
        specObj.Time_=TimeNoZero(li[13],li[14]>>4,li[14]&0x0F,li[15]>>3,  \
                            li[15]&0x07,li[16]>>2,li[16]&0x03,li[17])
        specObj.SweepRecvMode=li[18]>>6
        specObj.FileUploadMode=(li[18]&0x30)>>4
        specObj.SpecChangeFlag=li[18]&0x0F
        specObj.SweepSectionTotalNum=li[19]
        specObj.CurSectionInTotal=li[20]
        specObj.CurSectionNo=li[21]
        specObj.CommonTail=FrameTail(li[1558],li[1559],li[1560])
        i=0
        while(i<512):
            specObj.AllFreq[i]=TwoFreq(li[22+i*3]>>4,li[22+i*3]&0x0F, \
                li[23+i*3],li[24+i*3])
            i=i+1


        '''
        print " specObj.SweepRecvMode",specObj.SweepRecvMode
        print "specObj.FileUploadMode",specObj.FileUploadMode
        print  "specObj.SpecChangeFlag",specObj.SpecChangeFlag
        print "specObj.SweepSectionTotalNum",specObj.SweepSectionTotalNum
        print "specObj.CurSectionNo", specObj.CurSectionNo

        i=0
        while(i<512):
            print 'freq  '+str(i)+"--" +str(li[22+i*3]>>4)+"--"+str(li[22+i*3]&0x0F)+"--"+str(li[23+i*3])+"--"+str(li[24+i*3])
            i=i+1
        '''
        return specObj


    def ReceivePoaData(self):
        li = list(self.inPointFFT.read(100, 100))
        if (not len(li) == 78):
            return 0
        poa_data_obj=self.ByteToPoaData(li)

        return poa_data_obj
    def ByteToPoaData(self,li):
        poa_data_obj = PoaData()
        poa_data_obj.CommonHeader = FrameHeader(li[0], li[1], li[2], li[3])
        poa_data_obj.LonLatAlti = LonLatAltitude(li[4], li[5], li[6], li[7], li[8] >> 7, \
                                                 li[8] & 0x7F, li[9], li[10], li[11] >> 7, \
                                                 li[11] & 0x7F, li[12])

        poa_data_obj.Time = TimeNoZero(li[13], li[14] >> 4, li[14] & 0x0F, li[15] >> 3, \
                                       li[15] & 0x07, li[16] >> 2, li[16] & 0x03, li[17])

        for i in range(4):
            poa_data_obj.SecondCount[i] = li[18 + i]
        poa_data_obj.AbNum = li[22]
        poa_data_obj.SweepTotalNum = li[23]
        poa_data_obj.CurSectionNo = li[24]

        poa_data_obj.CommonTail = FrameTail(0, 0, 0xAA)
        for i in range(10):
            for j in range(5):
                poa_data_obj.AbBlock[i].AbPoint[j] = li[25 + 5 * i + j]

        return poa_data_obj


    def ReceiveAb(self):
        li=list(self.inPointFFT.read(2000,100))

        if(not len(li)==56):
            return 0
        abObj=AbFreqRecv()
        abObj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        abObj.LonLatAlti=LonLatAltitude(li[4],li[5],li[6],li[7],li[8]>>7, \
                                    li[8]&0x7F,li[9],li[10],li[11]>>7,  \
                                    li[11]&0x7F,li[12])
   
        abObj.Time_=TimeNoZero(li[13],li[14]>>4,li[14]&0x00F,li[15]>>3,  \
                        li[15]&0x07,li[16]>>2,li[16]&0x03,li[17])
        
        abObj.CurSectionNo=li[18]
        abObj.AbFreqNum=li[19]
        abObj.CommonTail=FrameTail(li[50],li[51],li[52])

        i=0
        while(i< li[19]):
            abObj.AllAbFreq[i]=AbFreq(li[20+i*3]>>4,li[20+i*3]&0x0F,  \
                li[21+i*3],li[22+i*3])
            i=i+1
        return abObj
    
    def ReceiveRecv(self):
        li=0
        try:
            li=list(self.inPointRecv.read(260,100))
            if(not len(li)==56):
                if(len(li)==260):
                    return li

                return 0
        except Exception,e:
            print e
            pass
        '''
        if(li[1]==0x21):
            obj=self.ByteToSweepRange(li)
        elif(li[1]==0x22):
            obj=self.ByteToIQFreq(li)
        elif(li[1]==0x23):
            obj=self.ByteToPressFreq(li)
        elif(li[1]==0x24):
            obj=self.ByteToRecvGain(li)
        elif(li[1]==0x25):
            obj=self.ByteToSendWeak(li)
        elif(li[1]==0x26):
            obj=self.ByteToThres(li)
        elif(li[1]==0x27):
            obj=self.ByteToIQPara(li)
        elif(li[1]==0x28):
            obj=self.ByteToPressPara(li)
        elif(li[1]==0x29):
            obj=self.ByteToAccessWay(li)
        elif(li[1]==0x2A):
            obj=self.ByteToTransferOpen(li)
        elif(li[1]==0x2B):
            obj=self.ByteToTransferClose(li)
        elif(li[1]==0x2C):
            obj=self.ByteToWorkMode(li)
        elif(li[1]==0x2D):
            obj=self.ByteToCorrGain(li)
        elif(li[1]==0x2E):
            obj=self.ByteToAntGain(li)
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])

        return obj
        '''
        return li
    def ByteToCorrGain(self,li):

        obj=GainTable()
        obj.AntType[0]=li[4]
        obj.AntType[1]=li[5]
        for i in range(12):
            obj.Freq[i]=li[6+i]
        for i in range(237):
            obj.CorrValue[i]=li[18+i]
        obj.CommonTail=FrameTail(li[-3],li[-2],li[-1])
        return obj 
    def ByteToAntGain(self,li):
        obj=self.ByteToCorrGain(li)
        return obj 
            
    def ByteToSweepRange(self,li):
        obj=SweepRangeSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.SweepRecvMode=li[4]>>2
        obj.FileUploadMode=li[4]&0x03
        obj.SweepSectionTotalNum=li[5]
        obj.SweepSectionNo=li[6]

        obj.StartSectionNo=li[7]
        obj.HighStartFreq=li[8]
        obj.LowStartFreq=li[9]

        obj.EndSectionNo=li[10]
        obj.HighEndFreq=li[11]
        obj.LowEndFreq=li[12]
        obj.SpecChangeFlag=li[13]>>6
        obj.ExtractM=li[13]&0x3F
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
    def ByteToIQFreq(self,li):
        obj=IQFreqSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.FreqNum=li[4]
        for i in range(3):
            obj.FreqArray[i]=CentreFreq(li[5+3*i],li[6+3*i]>>6, \
                li[6+3*i]&0x3F,li[7+3*i])
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
         
    def ByteToPressFreq(self,li):
        obj=PressFreqSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.PressNum=li[4]
        for i in range(2):
            obj.FreqArray[i]=CentreFreq(li[5+3*i],li[6+3*i]>>6,  \
                li[6+3*i]&0x3F,li[7+3*i])
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj


    def ByteToRecvGain(self,li):
        obj=RecvGainSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.RecvGain=li[4]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
        
    def ByteToSendWeak(self,li):
        obj=SendWeakSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.SendWeak=li[4]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj

    def ByteToThres(self,li):
        obj=ThresSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.ThresMode=li[4]
        obj.AdaptThres=li[5]
        obj.HighFixedThres=li[6]
        obj.LowFixedThres=li[7]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
    def ByteToIQPara(self,li):
        obj=IQParaSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.BandWidth=li[4]>>4
        obj.DataRate=li[4]&0x0F
        obj.UploadNum=li[5]
        obj.Time=TimeSet(li[6],li[7]>>4,li[7]&0x0F,li[8]>>3,  \
                            li[8]&0x07,li[9]>>2,li[9]&0x03,li[10])
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj

    def ByteToPressPara(self,li):
        obj=PressParaSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.PressMode=li[4]
        obj.PressSignal=li[5]>>4
        obj.PressSignalBandWidth=li[5]&0x0F
        obj.HighT1=li[6]
        obj.LowT1=li[7]
        obj.HighT2=li[8]
        obj.LowT2=li[9]
        obj.HighT3=li[10]
        obj.LowT3=li[11]
        obj.HighT4=li[12]
        obj.LowT4=li[13]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
        
    def ByteToAccessWay(self,li):
        obj=AccessWaySet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.AccessWay=li[4]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
        
    def ByteToTransferOpen(self,li):
        obj=TransferSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.CommonTail=FrameTail(li[4],li[5],li[6])
        return obj
        
    def ByteToTransferClose(self,li):
        obj=TransferSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.CommonTail=FrameTail(li[4],li[5],li[6])
        return obj
        
    def ByteToWorkMode(self,li):
        obj=IsConnectResponse()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.IsConnect=li[4]
        obj.TerminalType=li[5]
        obj.LonLatAlti=LonLatAltitude(li[6],li[7],li[8],li[9],li[10]>>7, \
                                        li[10]&0x7F,li[11],li[12],li[13]>>7,  \
                                        li[13]&0x7F,li[14])
        obj.CommonTail=FrameTail(li[15],li[16],li[17])
        return obj        
        
    def ReceiveIQ(self):
        li=list(self.inPointIQ.read(7000,100))
        if(not len(li)==6028):
            return 0

        print "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC%d" %(len(li))
        obj=IQData()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.LonLatAlti=LonLatAltitude(li[4],li[5],li[6],li[7],li[8]>>7, \
                                        li[8]&0x7F,li[9],li[10],li[11]>>7,  \
                                        li[11]&0x7F,li[12])

        
        obj.Time_=TimeNoZero(li[13],li[14]>>4,li[14]&0x0F,li[15]>>3,  \
                            li[15]&0x07,li[16]>>2,li[16]&0x03,li[17])
        
        obj.Param=IQDataPartHead(li[18],li[19]>>6,li[19]&0x3F,li[20],li[21]>>4, \
                                  li[21]&0x0F,li[22])
        obj.CurBlockNo=li[23]
        for i in xrange(2000):
            obj.IQDataAmp[i]=FreqIQ(li[24+3*i]>>4,li[24+3*i]&0x0F,li[25+3*i],li[26+3*i])

        obj.CommonTail=FrameTail(li[6024],li[6025],li[6026])
        return obj

    def ReceiveTdoa(self):
        li = list(self.inPointIQ.read(7000, 100))
        if (not len(li) == 6032):
            
            return 0
        #print li[18],li[19],li[20],li[21]
       
        #print "tdoa-------%d" % (len(li))
        obj = TdoaData()
        obj.CommonHeader = FrameHeader(li[0], li[1], li[2], li[3])
        obj.LonLatAlti = LonLatAltitude(li[4], li[5], li[6], li[7], li[8] >> 7, \
                                        li[8] & 0x7F, li[9], li[10], li[11] >> 7, \
                                        li[11] & 0x7F, li[12])

        obj.Time = TimeNoZero(li[13], li[14] >> 4, li[14] & 0x0F, li[15] >> 3, \
                               li[15] & 0x07, li[16] >> 2, li[16] & 0x03, li[17])

        for i in range(4):
            obj.SecondCount[i] = li[18 + i]

        obj.Param = IQDataPartHead(li[22], li[23] >> 6, li[23] & 0x3F, li[24], li[25] >> 4, \
                                   li[25] & 0x0F, li[26])
        obj.CurBlockNo = li[27]
        for i in xrange(2000):
            obj.IQDataAmp[i] = FreqIQ(li[28 + 3 * i] >> 4, li[28 + 3 * i] & 0x0F, li[29 + 3 * i], li[30 + 3 * i])

        obj.CommonTail = (0,0,0xAA)
        return obj


    def ReceiveTDOAData(self):
        li = list(self.inPointIQ.read(7000, 100))
        if (not len(li) == 6014):
            return 0

        obj = TdoaData()
        obj.CommonHeader = FrameHeader(li[0], li[1], li[2], li[3])
        obj.LonLatAlti = LonLatAltitude(li[4], li[5], li[6], li[7], li[8] >> 7, \
                                        li[8] & 0x7F, li[9], li[10], li[11] >> 7, \
                                        li[11] & 0x7F, li[12])

        obj.Time= TimeNoZero(li[13], li[14] >> 4, li[14] & 0x0F, li[15] >> 3, \
                               li[15] & 0x07, li[16] >> 2, li[16] & 0x03, li[17])

        for i in range(4):
            obj.SecondCount[i]=li[18+i]


        obj.Param = IQDataPartHead(li[22], li[23] >> 6, li[23] & 0x3F, li[24], li[25] >> 4, \
                                   li[25] & 0x0F, li[26])
        obj.CurBlockNo = li[27]
        for i in xrange(2000):
            obj.IQDataAmp[i] = FreqIQ(li[28 + 3 * i] >> 4, li[28 + 3 * i] & 0x0F, li[29 + 3 * i], li[30 + 3 * i])

        obj.CommonTail = FrameTail(0,0,0xAA)
        return obj



