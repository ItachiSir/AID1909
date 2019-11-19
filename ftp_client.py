"""
ftp文件服务，客户端
"""
import sys, time
from socket import *

# 全局变量
ADDR = ('127.0.0.1', 8888)


# 客户端文件处理类
class FTPClient:
    """
    文件查询，上传，下载，退出
    """

    def __init__(self, sockfd):
        self.sockfd = sockfd

    # 获取文件库中文件列表
    def do_list(self):
        self.sockfd.send(b'L')  # 发送请求
        # 等到服务端回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            # 一次接收文件字符串
            data = self.sockfd.recv(4096)
            print(data.decode())
        else:
            print(data)

    # 退出操作
    def do_exit(self):
        self.sockfd.send(b'Q')  # 向服务端发送退出请求
        self.sockfd.close()
        sys.exit("谢谢使用")

    # 下载文件操作
    def do_get(self, filename):
        # 将要下载的文件名称发送给服务端
        self.sockfd.send(('G ' + filename).encode())
        # 等待服务端的回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            # 下载接收文件
            f = open(filename, 'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    print('下载完毕')
                    break
                f.write(data)
            f.close()
        # 下载文件失败
        else:
            print(data)

    # 上传文件操作
    def do_put(self, filename):
        # 判断客户端是否存在该文件
        try:
            f = open(filename, 'rb')
        except Exception:
            print("不存在该文件")
            return
        # 如果客户端输入的是文件的路径
        filename = filename.split('/')[-1]

        # 把要上传的文件路径发给服务器
        self.sockfd.send(('P ' + filename).encode())
        # 接收服务端的反馈
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    print("上传完毕")
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)


def main():
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print(e)
        return
    # 实例化一个对象，用来调用方法处理请求
    ftp = FTPClient(sockfd)
    # 循环输入命令
    while True:
        print('\n =======命令选项===========')
        print('|         list            |')
        print('|        get file         |')
        print('|        put file         |')
        print('|          exit           |')
        print(' ==========================')
        try:
            cmd = input("请输入命令")
        except KeyboardInterrupt:
            sys.exit("\n谢谢使用")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd.strip() == 'exit':
            ftp.do_exit()
        elif cmd.strip()[:3] == 'get':
            filename = cmd.split()[1]
            ftp.do_get(filename)
        elif cmd.strip()[:3] == 'put':
            filename = cmd.split()[1]
            ftp.do_put(filename)
        else:
            print("请输入正确的指令")


if __name__ == '__main__':
    main()
