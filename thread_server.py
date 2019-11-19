"""
基于threading的多线程网络并发

实现步骤
1. 创建监听套接字
2. 循环接收客户端连接请求
3. 当有新的客户端连接创建线程处理客户端请求
4. 主线程继续等待其他客户端连接
5. 当客户端退出,则对应分支线程退出
"""
from socket import *
from threading import Thread
import sys
import signal

#设置全局变量
HOST='0.0.0.0'
PORT=8888
ADDR=(HOST,PORT)

#创建套接字
s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

print('Listen the port 8888...')
#处理客户端请求
def handle(c):
    while True:
        data,addr=c.recv(1024)
        if not data:
            break
        print(data.decode())
        c.send(b'OK')
    c.close()

#循环等待客户端连接
while True:
    try:
        c,addr=s.accept()
        print('connect from',addr)
    except KeyboardInterrupt:
        sys.exit('退出服务器')
    except Exception as e:
        print(e)
        continue
    #创建线程处理请求
    t=Thread(target=handle,args=(c,))
    t.setDaemon(True)
    t.start()
