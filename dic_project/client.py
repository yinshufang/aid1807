#!/usr/bin/env python3
#coding=utf-8
from socket import *
import  sys
import getpass


#单词操作
def do_query(s,name):
    data='Q '+name
    s.send(data.encode())

#查询历史记录
def do_history(s,name):
    data='H  '+name
    s.send(data.encode())
    data=s.recv(1024)
    print(data)

#注册判断
def do_register(s):
    while True:
        name=input('请输入用户名')
        password=getpass.getpass('请输入密码')
        password1=getpass.getpass('请确认密码')
        if password!=password1:
            print('密码不一致')
        if ' ' in password or ' ' in name:
            print('用户名和密码不能有空格')
            continue
        data='R {} {}'.format(name,password)
        s.send(data.encode())
        data=s.recv(128).decode()
        if data=='OK':
            return name
        elif data=='EXISTS':
            return 1
        else:
            return 2
#登录判断
def do_login(s):
    while True:
        name=input('请输入用户名')
        password=getpass.getpass('请输入密码')
        if ' ' in password or ' ' in name:
            print('用户名和密码不能有空格')
            continue
        data='L {} {}'.format(name,password)
        s.send(data.encode())
        data=s.recv(128).decode()
        if data=='OK':
            return name
        else:
            return 1       
#查词操作
def do_query(s,name):
    while True:
        word=input('请输入您要查的单词')
        if not word:
            break
        data='Q {} {}'.format(name,word)
        s.send(data.encode())
        data=s.recv(128).decode()
        if data=='NOT':
            print('sorry,单词不存在')
        else:
            print(word,':',data)
#登录操作
def login(s,name):
    while True:
        print('''
        1,查词
        2，查看历史记录
        3，退出
        ''')
        try:
            msg = int(input('请输入选项'))
        except Exception:
            print('输入错误')
            continue
        if msg==1:
            # print('查词')             
            do_query(s,name)
        elif msg==2:
            # print('获取历史')
            do_history(s,name)
        elif msg==3:
            return
        else:
            print('没有该命令')
            continue
def main():
    if len(sys.argv)<3:
        print('argv is error')
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)
    s=socket()
    s.connect(ADDR)
    while True:
        print('''
        1,注册
        2，登录
        3，退出
        ''')
        try:
            msg=int(input('请输入选项'))
        except Exception:
            print('输入错误')
            continue
        if msg==1:
            r=do_register(s)
            if r!=1:
                name=do_register(s)
                print('注册成功')
                login(s,name)
            elif r==1:
                print('用户存在')
            else:
                print('注册失败')
            #判断账号是否存在do_register(s)
            #界面二login(s,name)
        elif msg==2:

            name = do_login(s)
            if name != 1:
                print("登录成功！")
                login(s,name)
            else:
                print("登录失败！")
            #判断账号密码是否正确do_login(s)
            #界面二login(s,name)
        elif msg==3:
            s.send(b'E')
            sys.exit('谢谢使用')
        else:
            print('没有该命令')
            sys.stdin.flush()#清除标准输入
            continue
if __name__=='__main__':
    main()

