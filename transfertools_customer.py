#coding:utf-8
import socket
import time
ip = '192.168.0.117'
port = 8000
#创建套接字
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def sendFile(filename):
    with open(filename,'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sock.send(data)
        time.sleep(1)
        sock.send('EOF')

def recvFile(filename):
    with open(filename,'wb') as f:
        while True:
            recvData = sock.recv(1024)
            if recvData == 'EOF':
                break
            f.write(recvData)

def confirm(command):
    sock.send(command)
    data = sock.recv(1024)
    if data == 'ok':
        return True
try:
    #连接
    sock.connect((ip,port))
    #发送数据
    while True:
        command = raw_input('Please Enter(upload file or download file,q\Q exit):')
        if command == 'q' or command == 'Q':
            print 'Bye'
            break
        elif not command:
            continue
        action,filename = command.split()
        if action == 'upload':
            if confirm(command):
                sendFile(filename)
        elif action == 'download':
            if confirm(command):
                recvFile(filename)
        else:
            print 'check command...'

except socket.error,e:
    print 'Error:',e
finally:
    sock.close()