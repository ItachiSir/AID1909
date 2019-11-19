"""
ftp文件服务，服务端
"""
from socket import *
from threading import Thread
import sys, os, time

# 设置全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)
FTP = '/home/tarena/FTP/'  # 文件库位置


# 定义类实现服务器处理客户端请求功能
class FTPServer(Thread):
    """
    查看列表，上传，下载，退出
    """

    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd

    # 服务端获取文件列表并发送给客户端
    def do_list(self):
        # 获取文件列表
        files = os.listdir(FTP)
        if not files:
            self.connfd.send('文件库为空'.encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        # 把列表里面的文件名用换行拼接
        filelist = ''
        for file in files:
            # 不显示文件库里面的隐藏文件和目录
            if file[0] != '.' and os.path.isfile(FTP + file):
                filelist += file + '\n'
        self.connfd.send(filelist.encode())

    # 用户下载文件时的操作
    def do_get(self, filename):
        try:
            f = open(FTP + filename, 'rb')
        except Exception:  # 打开文件失败
            self.connfd.send("不存在该文件".encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        # 发送文件
        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                return
            self.connfd.send(data)

    # 用户上传文件时的操作
    def do_put(self, filename):
        if os.path.exists(FTP + filename):
            self.connfd.send('已存在该文件'.encode())
            return
        else:
            self.connfd.send(b'OK')
            f = open(FTP + filename, 'wb')
        # 接收客户端上传文件
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    # 循环接收请求，分情况调用功能函数
    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if not data or data == 'Q':
                return  # 线程结束
            elif data == 'L':
                self.do_list()
            elif data[0] == 'G':
                filename = data.split()[1]
                self.do_get(filename)
            elif data[0] == 'P':
                filename = data.split()[-1]
                self.do_put(filename)


def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    print('Listen the port 8888...')

    # 循环等待客户端连接
    while True:
        try:
            connfd, addr = s.accept()
            print('connect from', addr)
        except KeyboardInterrupt:
            sys.exit('退出服务器')
        except Exception as e:
            print(e)
            continue
        # 创建线程处理请求
        client = FTPServer(connfd)
        client.setDaemon(True)
        client.start()  # 运行的是run方法


if __name__ == '__main__':
    main()
