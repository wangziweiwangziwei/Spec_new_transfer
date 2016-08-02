#XuChuang
#2016.3.10
#Config FPGA Program for SPU2.0


from ctypes import *
import usb
import time






B200_VREQ_FPGA_START = 0x02;
B200_VREQ_FPGA_DATA = 0x12;
B200_VREQ_GET_COMPAT = 0x15;
B200_VREQ_SET_FPGA_HASH = 0x1C;
B200_VREQ_GET_FPGA_HASH = 0x1D;
B200_VREQ_SET_FW_HASH = 0x1E;
B200_VREQ_GET_FW_HASH = 0x1F;
B200_VREQ_LOOP = 0x22;
B200_VREQ_SPI_WRITE = 0x32;
B200_VREQ_SPI_READ = 0x42;
B200_VREQ_FPGA_CONFIG = 0x55;
B200_VREQ_FPGA_RESET = 0x62;
B200_VREQ_GPIF_RESET = 0x72;
B200_VREQ_GET_USB = 0x80;
B200_VREQ_GET_STATUS = 0x83;
B200_VREQ_AD9361_CTRL_WRITE = 0x90;
B200_VREQ_AD9361_CTRL_READ = 0x91;
B200_VREQ_FX3_RESET = 0x99;
B200_VREQ_EEPROM_WRITE = 0xBA;
B200_VREQ_EEPROM_READ = 0xBB;
B200_VREQ_FLUSH_DATA_EPS=0x31;




# get fx3 status
FX3_STATE_UNDEFINED = 0x00;
FX3_STATE_FPGA_READY = 0x01;
FX3_STATE_CONFIGURING_FPGA = 0x02;
FX3_STATE_BUSY = 0x03;
FX3_STATE_RUNNING = 0x04;
FX3_STATE_UNCONFIGURED = 0x05;
FX3_STATE_ERROR = 0x06;

def get_fx3_status():
    dev = usb.core.find(idVendor=0x04b4, idProduct=0x00f1)
    response = dev.ctrl_transfer(bmRequestType = 0xC0, #Read
                                     bRequest = B200_VREQ_GET_STATUS,  
                                     wValue = 0x00,
                                     wIndex = 0x00, 
                                     data_or_wLength = 1,
                                     timeout=1000
                                     )
    return response




def load_fpga (filename):
    dev = usb.core.find(idVendor=0x04b4, idProduct=0x00f1)
    transfer_size = 64
    out_buff=[]
    ntoread=transfer_size
    
    for i in range(512):
        out_buff.append(0)

    file_size = 0
    
   
    
    

    response = dev.ctrl_transfer(bmRequestType = 0xC0, #Read
                                     bRequest = B200_VREQ_LOOP,  
                                     wValue = 0x00,
                                     wIndex = 0x00, 
                                     data_or_wLength = ntoread,
                                     timeout=1000
                                     )
    bytes_to_xfer = 1
    for i in range(512):
        out_buff[i]=0

    

    response = dev.ctrl_transfer(  bmRequestType = 0x40, #Write
                                     bRequest = B200_VREQ_FPGA_CONFIG,  
                                     wValue = 0x00,
                                     wIndex = 0x00, 
                                     data_or_wLength = [0],
                                     timeout=1000
                                     )
    wait_count = 0
    
    while(1):
        fx3_state = get_fx3_status();

        if((wait_count >= 500) or (fx3_state[0] ==FX3_STATE_ERROR ) or (fx3_state[0] ==FX3_STATE_UNDEFINED )) :
            return fx3_state
        if(fx3_state[0] == FX3_STATE_FPGA_READY):
            
            break
        
        time.sleep(0.01)
        wait_count+=1
    response = dev.ctrl_transfer(  bmRequestType = 0x40, #Write
                                     bRequest = B200_VREQ_FPGA_START,  
                                     wValue = 0x00,
                                     wIndex = 0x00, 
                                     data_or_wLength = [0],
                                     timeout=1000
                                     )
        
    time.sleep(0.1)
    
    wait_count = 0
    while(1):
        fx3_state = get_fx3_status();

        if((wait_count >= 500) or (fx3_state[0] ==FX3_STATE_ERROR ) or (fx3_state[0] ==FX3_STATE_UNDEFINED )) :
            return fx3_state
        if(fx3_state[0] == FX3_STATE_CONFIGURING_FPGA):
            
            break
        
        else:
            time.sleep(0.01)
            wait_count+=1
    
    
    bytes_sent = 0
    bitfile = open(filename,'rb')
    
    while (1):
        
        out_buff=bitfile.read(transfer_size)
        if(len(out_buff)==0):
            break
        transfer_count = len(out_buff)
        

        #Send the data to the device
        response = dev.ctrl_transfer( bmRequestType = 0x40, #Write
                                     bRequest = B200_VREQ_FPGA_DATA,  
                                     wValue = 0x00,
                                     wIndex = 0x00, 
                                     data_or_wLength = out_buff,
                                     timeout=1000
                                     )
    bitfile.close()

    wait_count = 0
    while(1):
        fx3_state = get_fx3_status();

        if((wait_count >= 1000) or (fx3_state [0]==FX3_STATE_ERROR ) or (fx3_state[0] ==FX3_STATE_UNDEFINED )) :
            
            return fx3_state
        if(fx3_state [0]== FX3_STATE_RUNNING):
            
            break
        time.sleep(0.01)
        wait_count+=1

    try:
        dev.ctrl_transfer(bmRequestType = 0x40, #Write
                                     bRequest =B200_VREQ_FLUSH_DATA_EPS,  
                                     wValue = 0x00,
                                     wIndex = 0x00, 
                                     data_or_wLength = [0],
                                     timeout=1000
                                     )
    except Exception,e:
        pass
    
    return 0
    



















    



