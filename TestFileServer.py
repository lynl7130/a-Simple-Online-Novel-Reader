
# coding: utf-8

# In[1]:

import socket
import threading
import os


# In[2]:

def RetrFile(name, sock,path,addr,port): 
    
    filename = str(sock.recv(1024),encoding = 'utf-8')
    
    if filename[:5]=="open:":
        file = filename[5:]
        currentpg = 0
        if os.path.isfile(path+file):
            sock.send(bytes("OK"+ str(os.path.getsize(path+file)),encoding='utf-8'))
            datalist = []
            with open(path+file,'rb')as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    datalist.append(data)    
            f.close()
            sock.send(datalist[currentpg])
            
            
        else:
            sock.send(bytes("ERR",encoding='utf-8'))
            
    elif filename[:5]=="down:":
        file = filename[5:]
       
        if os.path.isfile(path+file):
            sock.send(bytes("OK"+ str(os.path.getsize(path+file)),encoding='utf-8'))
            userResponse = str(sock.recv(1024),encoding='utf-8')
            if userResponse == "OK":
                with open(path+file,'rb') as f:
                    while True:
                        bytesToSend = f.read(1024)
                        sock.send(bytesToSend)
                        if not bytesToSend:
                            break
                f.close()
        else:
            sock.send(bytes("ERR",encoding = 'utf-8'))
        
    elif filename[:5]=="back:":
        file = filename[5:]
        
        if os.path.isfile(path+file):
            sock.send(bytes("OK",encoding='utf-8'))
            currentpg = int(str(sock.recv(1024),encoding='utf-8'))-1
            datalist = []
            with open(path+file,'rb')as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    datalist.append(data)    
            f.close()
            sock.send(datalist[currentpg])            
        else:
            sock.send(bytes("ERR",encoding = 'utf-8'))
            
    elif filename[:5]=="next:":
        file = filename[5:]
        
        if os.path.isfile(path+file):
            sock.send(bytes("OK",encoding='utf-8'))
            sock.send(bytes(str(os.path.getsize(path+file)),encoding='utf-8'))
            currentpg = int(str(sock.recv(1024),encoding='utf-8'))-1
            datalist = []
            with open(path+file,'rb')as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    datalist.append(data)    
            f.close()
            sock.send(datalist[currentpg])
            
        else:
            sock.send(bytes("ERR",encoding = 'utf-8'))
    
    elif filename[:5]=="jump:":
        file = filename[5:]
        
        if os.path.isfile(path+file):
            sock.send(bytes("OK",encoding='utf-8'))
            currentpg = int(str(sock.recv(1024),encoding='utf-8'))-1
            datalist = []
            with open(path+file,'rb')as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    datalist.append(data)    
            f.close()
            sock.send(datalist[currentpg])
            
        else:
            sock.send(bytes("ERR",encoding = 'utf-8'))
    
    sock.close()


# In[5]:

def Main():

    path = ''               #modify！！
    addr = ''               #modify！！
    port = 9999
    
    s = socket.socket()
    s.bind((addr,port))
    
    s.listen(5)
    
    print("Server Started.")
    
    while True:
        c, addr = s.accept()
        print("client connected ip:<"+str(addr)+">")
        
        t = threading.Thread(target = RetrFile, args=("retrThread",c,path,addr,port))
        t.start()
    
    s.close()



if __name__ == "__main__":
    Main()





