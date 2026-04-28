#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
"""
python包在初始化时会自动调用这个py文件
__init__.py这个文件的作用
        1. 声明一个python包
        2. 做一些初始化的工作
        3. 内容可以为空，但一定要用一个__init__.py文件
"""

# 一些初始化的工作


if __name__ == '__main__':
    print('作为主程序运行')
else:
    print('python_package 初始化')