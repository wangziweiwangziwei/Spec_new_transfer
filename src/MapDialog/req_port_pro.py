from src.Package.package import Query,FrameHeader,FrameTail
from src.CommonUse.staticVar import staticVar


class QueryPort:
    ###############################
    tail=FrameTail(0,0,0xAA)

        
    @classmethod
    def query_port(cls,parent,func):
        id_for=staticVar.getid()
        lowid=id_for&0x00FF
        highid=id_for>>8
    
        query=Query()
        query.CommonHeader=FrameHeader(0x55,func,lowid,highid)
        query.CommonTail=cls.tail
        for i in bytearray(query):
            print i,
             
        # staticVar.getSock().sendall(bytearray(query))

        parent.queueRequest.put(query)
