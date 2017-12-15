
# coding: utf-8

# In[1]:

import socket
from tkinter import *
import os


# In[2]:

def pop_error(title,context):
    from tkinter.messagebox import showerror
    showerror(title,context)


# In[3]:

def pop_info(title,context):
    from tkinter.messagebox import showinfo
    showinfo(title,context)


# In[4]:

def pop_okcancel(title,context):
    from tkinter.messagebox import askokcancel
    result = askokcancel(title,context)
    return result


# In[5]:

def pop_directory():
    from tkinter.filedialog import askdirectory
    filedir = askdirectory()
    return filedir


# In[51]:

def openfile():
    global file
    global currentpg
    global maxpg
    global addr
    global port
    
    
    #flush whats in the text
    #text.delete(1.0,END)
    currentpg=1
    
    
    s = socket.socket()
    s.connect((addr,port))
    cfile = file
    file = str(e1.get())#e1是一个输入框的实例，从e1接收含路径的filename
    
    filename = bytes("open:"+file,encoding = 'utf-8')
    s.send(filename)
    
    message = str(s.recv(1024),encoding='utf-8')
    
    if message[:2]=="OK":
        
        text.delete(1.0,END) 
        
        global b3
        global b4
        
        global b5
        global myCombox
        
        b3=Button(topFrame, text="上一页",command=backpg)
        b3.grid(row=0, column=4,padx=5,sticky=W)

        b4=Button(topFrame, text="下一页",command=nextpg)
        b4.grid(row=0, column=5, padx=5, sticky=W)
        
        maxpg = int(int(message[2:])/1024)
        pgs=[]
        from tkinter import ttk
        for i in range(maxpg):
            pgs.append("第"+str(i+1)+"页")
        myCombox = ttk.Combobox(topFrame, values=pgs )
        myCombox.grid(row=0, column=6,sticky=W)
        myCombox.current(0)
        
        
        b5=Button(topFrame, text="跳页",command=jumppg)
        b5.grid(row=0,column=7,padx=5,sticky=W)
                       
        f = open('C:\\Users\\LynL\\Desktop\\temp_' + file, 'wb')
        
        data = s.recv(1024)
        f.write(data)
        f.close()
        
        with open('C:\\Users\\LynL\\Desktop\\temp_' + file,encoding='gb18030',errors='ignore') as f:
            for each_line in f:
                text.insert(INSERT,each_line) #text是一个文本框的实例，按行插 
        os.remove('C:\\Users\\LynL\\Desktop\\temp_' + file)
        
        
    else:
        pop_error('打开提示','文件'+file+'不存在!')
        #text.delete(1.0,END) 
        file=cfile
        #b3.grid_forget()
        #b4.grid_forget()
        #b5.grid_forget()
        #myCombox.grid_forget()
        
    s.close()


# In[7]:

def backpg():
    global file
    global currentpg
    global addr
    global port

    if file =="":
        pop_info('后退提示','没有打开文件！')
        return;
    if currentpg==1:
        pop_info('后退提示','已经是第一页！')
        return;
    
    
    s=socket.socket()
    s.connect((addr,port))
    
   
    filename = bytes("back:"+file,encoding="utf-8")
    s.send(filename)
    
    message = str(s.recv(1024),encoding='utf-8')
 
    
    if message == "OK":
        text.delete(1.0,END) 
            
        currentpg =currentpg-1
        s.send(bytes(str(currentpg),encoding='utf-8'))
        myCombox.current(currentpg-1)
  
        f = open('C:\\Users\\LynL\\Desktop\\temp_' + file, 'wb')
        
        data = s.recv(1024)
        f.write(data)
        f.close()
        
        with open('C:\\Users\\LynL\\Desktop\\temp_' + file,encoding='gb18030',errors='ignore') as f:
            for each_line in f:
                text.insert(INSERT,each_line) #text是一个文本框的实例，按行插 
        os.remove('C:\\Users\\LynL\\Desktop\\temp_' + file)
    else:
        pop_error('后退提示','当前文件丢失')
    s.close()


# In[8]:

def nextpg():
    global file
    global currentpg
    global addr
    global port

    if file =="":
        pop_info('前进提示','没有打开文件！')
        return;
      
    s=socket.socket()
    s.connect((addr,port))

    filename = bytes("next:"+file,encoding="utf-8")
    s.send(filename)
    
    message = str(s.recv(1024),encoding='utf-8')
    
    if message == "OK":
        pgnum = int(int(str(s.recv(1024),encoding='utf-8'))/1024)
       
        if currentpg==pgnum:
            pop_info('前进提示','已经是最后一页！')
            return;
        
        text.delete(1.0,END)
        
        currentpg+=1
        s.send(bytes(str(currentpg),encoding='utf-8'))
        myCombox.current(currentpg-1)
        
        f = open('C:\\Users\\LynL\\Desktop\\temp_' + file, 'wb')
        
        data = s.recv(1024)
        f.write(data)
        f.close()
        
        with open('C:\\Users\\LynL\\Desktop\\temp_' + file,encoding='gb18030',errors='ignore') as f:
            for each_line in f:
                text.insert(INSERT,each_line) #text是一个文本框的实例，按行插 
        os.remove('C:\\Users\\LynL\\Desktop\\temp_' + file)
    else:
        pop_error('前进提示','当前文件丢失')
    s.close()


# In[9]:

def jumppg():
    global file
    global currentpg
    global addr
    global port
    
    rawnum = myCombox.get()
    jpnum = rawnum[1:-1]
    
    s = socket.socket()
    s.connect((addr,port))
    
    filename = bytes("jump:"+file,encoding = "utf-8")
    s.send(filename)
    
    message = str(s.recv(1024),encoding='utf-8')
    if message[:2]=="OK":
        text.delete(1.0,END)
        currentpg = int(jpnum)
        
        s.send(bytes(jpnum,encoding='utf-8'))
        f = open('C:\\Users\\LynL\\Desktop\\temp_' + file, 'wb')
        
        data = s.recv(1024)
        f.write(data)
        f.close()
        
        with open('C:\\Users\\LynL\\Desktop\\temp_' + file,encoding='gb18030',errors='ignore') as f:
            for each_line in f:
                text.insert(INSERT,each_line) #text是一个文本框的实例，按行插 
        os.remove('C:\\Users\\LynL\\Desktop\\temp_' + file)
    else:
        pop_error('跳转提示','当前文件丢失')
    s.close()


# In[10]:

def downfile():
    global addr
    global port
    
    s = socket.socket()
    s.connect((addr,port))
    file = str(e1.get())
    
    filename = bytes("down:"+file,encoding = "utf-8")
    s.send(filename)
    
    message = str(s.recv(1024),encoding='utf-8')
    if message[:2]=="OK":
        size = int(message[2:])
        result = pop_okcancel("下载提示","文件共"+str(size)+"字节，是否下载？")
        if result:
            s.send(bytes("OK",encoding='utf-8'))
            directory = pop_directory()
           
            while os.path.isfile(directory+"/"+file):
                file=str('副本')+file
            f = open(directory+"/"+file,'wb')
            data = s.recv(1024)
            totalRecv = len(data)
            f.write(data)
            while totalRecv<size:
                data = s.recv(1024)
                totalRecv+=len(data)
                f.write(data)
            f.close()
            pop_info('下载提示','下载完毕！')            
    else:
        pop_error("下载提示","没有找到文件！")
        
    file = ""
    s.close()


# In[50]:

#tkinter main window

#全局参数
currentpg = 0
file =""
maxpg = 0
addr = '10.147.108.23'
port = 9999
    
#创建主窗口
root=Tk()
root.title('小说阅读器')#窗口名字
root.geometry('604x500')#设置主窗口大小
root.resizable(False,True)#第一个参数表示是否允许最大化最小化
#第二个参数表示是否允许手动缩放
    
topFrame = Frame(root,bd=1, relief=SUNKEN)#relief表示如何凹凸，bd表示按钮边框宽
topFrame.pack(fill=BOTH)#fill=BOTH表示widget在X、Y两方向随窗体大小变化

bottomFrame = Frame(root,bd=1, relief=SUNKEN)
bottomFrame.pack(fill=BOTH)

label=Label(topFrame,text="文件名：")#label表示在topFrame上显示字
label.grid(row=0,column=0, sticky=W)#sticky=W紧靠左，=E紧靠右

#创建一个输入框
v1=StringVar()
e1=Entry(topFrame,textvariable=v1)
e1.grid(row=0,column=1,sticky=W)

b1=Button(topFrame,text="打开",command=openfile)
b1.grid(row=0,column=2,padx=5,sticky=W)

b2=Button(topFrame, text="下载",command=downfile)
b2.grid(row=0, column=3,padx=5,sticky=W)




text = Text(bottomFrame, height=600,width=83)
text.pack(side=LEFT)


sc = Scrollbar(bottomFrame)
sc.pack(side=RIGHT,fill=Y)

sc.config(command=text.yview)
text.config(yscrollcommand=sc.set)

mainloop()


# In[ ]:




# In[ ]:



