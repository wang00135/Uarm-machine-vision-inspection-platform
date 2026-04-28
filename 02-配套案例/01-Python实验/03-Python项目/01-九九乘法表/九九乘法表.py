#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#把1-9的数值依次赋值给num；右边为range
for num in range(1,10):
#把range(1,num+1)赋值给x；当num = 1，x=(1,2),此时x 的取值就是1；
    for x in range(1,num+1):
#假如num=1,x=1，这句的意思是1*1=(1*1),end=' '表示不换行以空格为分隔符,还可以用\t制表符方式分割;

        print('%d*%d=%2d' % (num, x, num * x), end=' ')
# print()表示换行
    print()

