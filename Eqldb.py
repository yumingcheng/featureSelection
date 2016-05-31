#-*-coding:utf-8-*
import os
import json
from struct import*
from socket import *

def connect(*args,**kwargs):
    return Connection(*args,**kwargs)

def eqlInitialise(tcpCliSock,db):
    eqlSend(tcpCliSock,'SET OUTFORMAT json;\n\0')
    eqlRevc(tcpCliSock)
    usedb = 'use %s;\n\0'%db
    eqlSend(tcpCliSock,usedb)
    data = eqlRevc(tcpCliSock)
    data = data.replace('\n',' ')
#    print "[%s]%s/%s"%(data,data[101],data[100])
#    dbcheck = json.loads(data[:-1])
    dbcheck = CheckReJson(data)
    if dbcheck.get('code','-1001') != 1:
        raise ValueError,'connect error!'

def CheckReJson(jsonData):
    return json.loads(jsonData[:-1])

def eqlSend(tcpCliSock,data):
    print '[发送消息]',data,len(data)
    tcpCliSock.send(pack('i',htonl(len(data))))
    tcpCliSock.send(data)

def eqlRevc(tcpCliSock):
    lenContent = tcpCliSock.recv(4)        
    print len(lenContent)
    if not lenContent:
        return
    lenContent,  = unpack('I',lenContent)
    print 'lenContent',lenContent,ntohl(lenContent)
    curlen = 0
    data = ""
    while curlen < ntohl(lenContent):
        tempdata = tcpCliSock.recv(1024)
        data += tempdata
        print 'len tempdata',len(tempdata)
        curlen += len(tempdata)
    return data

class Connection(object):

    def __init__(self,*args,**kwargs):
        """
         host
           string, host to connect
           
         user
           string, user to connect as
 
         passwd
           string, password to use
 
         db
           string, database to use
 
         port
           integer, TCP/IP port to connect to
        """
        kwargs2 = kwargs.copy()
        if 'db' not in kwargs2:
           print "error 请填写连接db"
           raise NameError

        self.host = kwargs2.pop('host','127.0.0.1')
        self.user = kwargs2.pop('user','')
        self.passwd = kwargs2.pop('passwd','')
        self.port = kwargs2.pop('port',80)
        self.db = kwargs2.pop('db','')
        self.ADDR = (self.host,self.port)

        self.eqltcpCliSock = socket(AF_INET,SOCK_STREAM)
        self.eqltcpCliSock.connect(self.ADDR)
        eqlInitialise(self.eqltcpCliSock,self.db)
        
    def cursor(self):
        return Cursor(self.eqltcpCliSock) 

    def close(self):
        self.eqltcpCliSock.close()
        

class Cursor(object):

    def __init__(self,tcpCliSock):
        self.curIndex = 0;
        self.searchList = []
        self.totalDoc = 0
        self.realLimit = -1;
        self.tcpCliSock = tcpCliSock
        pass
    def execute(self,eql,limitMax='10000'):     
        self.curIndex = 0;
        self.searchList = []      
        self.totalDoc = 0
        self.realLimit = -1;

        if eql == '':
            return self.totalDoc
        eql = eql.replace(';',' ')
        eqlList = eql.split()
        if 'limit'  in eqlList:
            lindex = eqlList.index('limit')
            if len(eqlList) > (lindex+1) and eqlList[lindex+1].isdigit():
                if int(eqlList[lindex+1]) > limitMax:
                    self.realLimit = int(eqlList[lindex+1])
                    eqlList[lindex+1] = str(limitMax)

        useEql = '%s; \n\0'%(" ".join(eqlList));
        eqlSend(self.tcpCliSock,useEql)
        eqldata = CheckReJson(eqlRevc(self.tcpCliSock))
        if eqldata.get('code','-1001') != 1:
            return self.totalDoc     
#        if self.realLimit != -1 and eqldata.get('total',-1) < self.realLimit:
#           self.totalDoc =  eqldata.get('total',-1)

        countDoc = 0
        for dicData in eqldata['record']:
            tempList = []
            countDoc += 1
            for key,values in dicData.items():
                tempList.append(values.encode('UTF-8'))
            self.searchList.append(tempList)

        self.totalDoc = countDoc
        return countDoc
    
    def fetchone(self):
        print self.searchList
        index = self.curIndex 
        if index >= self.totalDoc:
            return None 
        self.curIndex += 1
        return self.searchList[index]
        
    def fetchmany(self,count = 1):
        index = self.curIndex
        if index >= self.totalDoc:
            return None
        end = self.curIndex + count
        self.curIndex = min(end,self.totalDoc)        
        print index,end,type(self.searchList),len(self.searchList)
        return self.searchList[index:end]

    def fetchall(self):
        index = self.curIndex
        if index >= self.totalDoc:
            return None
        self.curIndex = self.totalDoc     
        return self.searchList[index:]


    def scroll(self,value,mode='relative'):
        if mode == 'relative':
            r = self.curIndex + value
        elif mode == 'absolute':
            r = value
        else:
            return None
        if r < 0:
            r = 0
        elif r >= self.totalDoc:
            r = self.totalDoc - 1
        self.curIndex = r
       
        
if __name__ == "__main__":
    import Eqldb
    conn = Eqldb.connect(host='192.168.1.135',db='org_201404',port=30002)
    cursor = conn.cursor()
    count = cursor.execute('select doc_title,doc_datetime from tbl_sh2 where doc_content =\"10\" limit 10;')
    print '文档总数:',count

    #获取一条记录,每条记录做为一个元组返回  
    print "只获取一条记录:"  
    result = cursor.fetchone()  
    if result is not None:
        print 'title: %s   content: %s' % (result[0],result[1])  
  
    #获取5条记录，注意由于之前执行有了fetchone()，所以游标已经指到第二条记录了，也就是从第二条开始的所有记录  
    print "只获取5条记录:"  
    results = cursor.fetchmany(5)  
    if results is not None:
        for result in results:  
            print 'title: %s   content: %s' % (result[0],result[1])  

    print "获取所有结果:"  
    #重置游标位置，0,为偏移量，mode＝absolute | relative,默认为relative,  
    cursor.scroll(0,mode='absolute') 

    #获取所有结果  
    results = cursor.fetchall()  
    if results is not None:
        for result in results:  
            print 'title: %s   content: %s' % (result[0],result[1])  
    conn.close()  






              
