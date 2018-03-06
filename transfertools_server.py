#coding:utf-8
import SocketServer
import time
import os
import model
class MyServer(SocketServer.BaseRequestHandler):
    def setup(self):
        print 'Server is start...'
    def recvFile(self,filename):        
        file_path = '/home/lizheng/cloud_storage/' + filename
        with open(file_path,'wb') as f:
            self.request.send('ok')
            while True:
                recvData = self.request.recv(1024)
                if recvData == 'EOF':
                    break
                f.write(recvData)
        mysql = model.FileInfo()
        mysql.filename = filename
        mysql.filepath = '/home/lizheng/cloud_storage'
        mysql.filesize = os.path.getsize(file_path)
        mysql.action = 'update'
        mysql.time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        mysql.save()
    def sendFile(self,filename):        
        file_path = '/home/lizheng/cloud_storage/' + filename.split('\\')[-1]
        with open(file_path,'rb') as f:
            self.request.send('ok')
            while True:
                sendData = f.read(1024)
                if not sendData:
                    break
                self.request.send(sendData)
            time.sleep(1)
            self.request.send('EOF')
        mysql = model.FileInfo()
        mysql.filename = filename.split('\\')[-1]
        mysql.filepath = '\\'.join(filename.split('\\')[0:-1])
        mysql.filesize = os.path.getsize(file_path)
        mysql.action = 'download'
        mysql.time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        mysql.save()

    def handle(self):
        print '%s:%s is connected...'%self.client_address
        while True:
            try:
                data = self.request.recv(1024)
                print time.strftime('%Y-%m-%d %H:%M:%s',time.localtime()) + ':' + data
                if not data:
                    break
                else:
                    action,filename = data.split()
                    if action == 'upload':
                        filename = filename.split('\\')[-1]
                        self.recvFile(filename)
                    elif action == 'download':
                        self.sendFile(filename)
                    else:
                        print 'check command...'
            except Exception,e:
                print 'Error:',e
    def finish(self):
        print 'Server is stop'

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('',8000),MyServer)
    #开启一个TCP协议的多线程
        #第一个双元素元祖 服务的IP和端口
        #第二个参数为开启的对象
    server.serve_forever() #开启服务的函数

