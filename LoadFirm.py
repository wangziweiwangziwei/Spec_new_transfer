#XuChuang
#2016.3.10
#Config FPGA Program for SPU2.0


import ctypes





def load_firmware(filename):
    loaddll=ctypes.windll.LoadLibrary('LoadFirmware.dll' )
    if(loaddll==None):
        return
    try:
        pStr = ctypes.c_char_p( )
        pStr.value = filename
        loaddll.LoadFirmware(pStr)
    except:
        pass
        
    return 0






    



