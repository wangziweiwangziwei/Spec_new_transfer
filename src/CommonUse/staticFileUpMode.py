class staticFileUp:
    upload_mode=0  #0:shou dong #
    extract_m=1
    change_thres=10
    
    @classmethod 
    def getUploadMode(cls):
        return cls.upload_mode
    
    @classmethod 
    def getExtractM(cls):
        return cls.extract_m
    
    @classmethod 
    def getChangeThres(cls):
        return cls.change_thres
    
    @classmethod 
    def setUploadMode(cls,upload_mode):
        cls.upload_mode=upload_mode
    
    @classmethod 
    def setExtractM(cls,extractM):
        cls.extract_m=extractM
    
    @classmethod 
    def setChangeThres(cls,change_thres):
        cls.change_thres=change_thres 
        
    
    
    
    
    
    
    
    
    
