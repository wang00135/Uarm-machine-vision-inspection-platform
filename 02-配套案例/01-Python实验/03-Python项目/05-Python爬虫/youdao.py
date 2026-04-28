#！ /usr/bin evn python3
# -*- coding:utf-8 -*-
import requests


def youdao_translate(value):
    if value == '':
        print('输入内容为空@_@')
        return False
    else:

        # Request URL
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

        # 待提交准备Post给url的Data:定义为dict
        data = {
            'i': value
            , 'from': 'AUTO'
            , 'to': 'AUTO'
            , 'smartresult': 'dict'
            , 'client': 'fanyideskweb'
            , 'salt': '15450970848938'
            , 'sign': '1013a7a1416565e32eb3092d219eebf2'
            , 'ts': '1545097084893'
            , 'bv': 'b33a2f3f9d09bde064c9275bcb33d94e'
            , 'doctype': 'json'
            , 'version': '2.1'
            , 'keyfrom': 'fanyi.web'
            , 'action': 'FY_BY_REALTIME'
            , 'typoResult': 'false'
        }
        # 使用urlencode方法转换标准格式　
        r = requests.post(url, data=data)
        print(r.url);

        target = r.json();
        print("翻译结果：")
        print(target['translateResult'][0][0]['tgt'])
        print()

        return True


if __name__ == '__main__':
    try:
        while True:
            word = input('请输入待翻译的单词或句子:\n').strip()
            youdao_translate(word)
    except KeyboardInterrupt:
        print('\a手动退出!欢迎再来')
