# -*- coding:utf-8 -*-
# author:f0ngf0ng

'''
去掉JSLinkFinder的日志里的静态文件路径，jpg,png,js,css,svg
'''
from urllib import parse
import re
rex = r'(^[1-9]\d*|0)(\s)(-)(\s)'

file_url1 = "test1"

file_url3 = "quchong" + file_url1

file = open(file_url1+'.txt',"r",encoding="utf-8",errors="ignore")
t1 = []
valid = set()

a = [".jpg",".png",".css",".svg"]
file.readline()
file.readline()
file.readline()
while True:
    insert_value = 1
    is_valid = 0
    mystr = file.readline()  # 表示一次读取一行

    mystr = mystr.strip('\n')
    mystr = parse.unquote(mystr)

    mystr = mystr.replace("&amp;","&").replace("&lt;","<").replace("&rt;",">")


    if mystr in valid:
        while True:

            mystr = file.readline()  # 表示一次读取一行
            mystr = mystr.strip('\n')
            mystr = parse.unquote(mystr)
            b = mystr.split("-")
            bbb = b[0].strip()
            bb = bbb.isnumeric()
            if bb == False:
                insert_value = 1
                break


    if "Valid URL" in mystr:
        is_valid = 1
        valid.add(mystr)

    for single_a in a:
        if is_valid == 1:
            break
        if single_a in mystr:
            insert_value = 0

    if insert_value == 1:
        t1.append(re.sub(rex,"",mystr.strip()))

    if not mystr:
    #读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
        break


file.close()

# print(valid)
# print(t1)

file2 = open(file_url3+'.txt',"w+",encoding="utf-8",errors="ignore")
# global list
list1 = list(t1)            #集合转列表，对列表的值递归写入
for i in range(len(list1)):
    # print(list1[i])
    file2.write(list1[i]+'\n')
file2.close()