from socket import *
import os,sys
import signal
#创建套接字
s=socket(AF_INET,SOCK_STREAM)
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('',7777))
s.listen(4)
while True:
    try:
        c,addr=s.accept()
    except KeyboardInterrupt:
        sys.exit('服务器退出')
