#!/usr/bin/env python3
#coding=utf-8
'''
name:yin
date:2018,.0.1
'''
from socket import *
import  sys
import  os
import time
import pymysql
import signal
#全局变量
DICT_TEXT='./dict.txt'
HOST='0.0.0.0'
PORT=7777
ADDR=(HOST,PORT)
#子进程处理请求
def do_child(c,db):
    while True:
        data=c.recv(128).decode()
        print(c.getpeername(),':',data)
        if (not data)or data[0]=='E':
            c.close()
            sys.exit(0)
        elif data[0]=='R':
            do_register(c,db,data)
        elif data[0]=='L':
            do_login(c,db,data)
        elif data[0]=='Q':
            do_query(c,db,data)
        elif data[0]=='H':
            do_history(c,db,data)
def do_history(c,db,data):
    l=data.split(' ')
    name=l[2]
    print(l)
    cursor=db.cursor()
    sql="select * from hist where name='%s'"%name
    cursor.execute(sql)
    # print(cursor.fetchone())
    r=cursor.fetchall()
    print(r)
    if r==None:
        c.send(b'NOT')
    else:
        for i in r:
            if not i:
                break
            c.send(str(i).encode())    
def do_query(c,db,data):
    print('查询单词')
    l=data.split(' ')
    name=l[1]
    word=l[2]
    cursor=db.cursor()
    sql="select interpret from word where word='%s'"%(word)
    cursor.execute(sql)
    r=cursor.fetchone()
    if r==None:
        c.send(b'NOT')
    else:
        c.send(r[0].encode())
        tm = time.ctime()
        sql = "insert into hist (name,word,time)values ('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
def do_login(c,db,data):
    print('登录')
    l=data.split(' ')
    name=l[1]
    password=l[2]
    cursor=db.cursor()
    sql="select * from user where name='%s' and password='%s'"%(name,password)
    cursor.execute(sql)
    r=cursor.fetchone()
    if r!=None:
        c.send(b'OK')
        return
    else:
        c.send(b'ERROR')

def do_register(c,db,data):
    print('注册')
    l=data.split(' ')
    name=l[1]
    password=l[2]
    cursor=db.cursor()
    sql="select * from user where name='%s'"%name
    cursor.execute(sql)
    r=cursor.fetchone()
    if r!=None:
        c.send(b'EXISTS')
        return
    #用户不存在 插入用户
    sql="insert into user (name,password)  values('%s','%s')"%(name,password)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FALL')
        return
    else:
        print("%s注册成功"%name)
def main():
    db=pymysql.connect('localhost','root','123456','dict')

    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    #忽略子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr=s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        #创建子进程
        pid=os.fork()
        if pid==0:
            s.close()
            #处理请求
            do_child(c,db)
        else:
            c.close()
            continue

if __name__=='__main__':
    main()
