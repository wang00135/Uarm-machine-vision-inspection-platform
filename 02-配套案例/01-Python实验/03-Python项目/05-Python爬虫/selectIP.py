# -*- coding:utf-8 -*-
import requests
import bs4
url = "http://www.ip138.com/ips138.asp"


def get_html_text(input_IP):
    try:
        params = {
            'ip': input_IP,
            "action": 2
        }
        r = requests.get(url, params=params,)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Failed!")


def getData(html):
    data=[]
    soup = bs4.BeautifulSoup(html, "html.parser")

    for tr in soup.find_all('tr'):
        if isinstance(tr, bs4.element.Tag):     # 过滤掉非标签类型;isinstance判断变量类型
            h1 = tr('h1')
            # print(h12)
            lis = tr('li')                      # 取出tr标签的li标签，若tr标签没有li标签，则lis为None
            if(lis!=None and h1 != None ):
                data += [i.string for i in h1]  # 去除标签，得到数据
                data+=[i.string for i in lis]   # 去除标签，得到数据
    return data


inputIP=input('请输入IP地址：')
html=get_html_text(inputIP)
data=getData(html)
for i in data:
    print(i)
