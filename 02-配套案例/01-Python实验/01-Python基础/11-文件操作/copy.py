#!/usr/bin/env python3
# -*- coding:UTF8 -*-
"""
一个文本复制程序,附带编码格式的转化
"""

def _read_txt(src='./test.txt', encoding='UTF8'):
    try:
        f = open(src, 'r', encoding=encoding)
    except IOError as e: 
        print("文件不能查找！")
        raise
    txt = f.read()
    f.close()
    return txt

def _write_txt(dst='./test.txt', text="", encoding='UTF8'):
    f = open(dst, 'w', encoding=encoding)
    f.write(text.decode(encoding))
    f.flush()
    f.close()

def copy(src, dst):
    # 读取一个GBK编码的文件,并将其已utf8格式保存
    _write_txt(dst, _read_txt(src, encoding='GBK').encode('utf8'), encoding='utf8')

def main():
    copy('./src.txt', './dst.txt')
    print('复制完成')
if __name__ == '__main__':
    main()

