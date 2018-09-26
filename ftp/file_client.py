from socket import *
#开始页面
def show():
    print('''
        ********************
        |1:查看服务端文件  |
        |2:下载服务端文件  |
        |3:上传本地文件    |
        |4:退出            |
        *******************
        ''')
def main():
    #创建套接字
    sockfd=socket(AF_INET,SOCK_STREAM)
    server_addr=('127.0.0.1',7777)
    socket.connect(server_addr)
    while True:
        show()
        


if __name__=='__main__':
    main()