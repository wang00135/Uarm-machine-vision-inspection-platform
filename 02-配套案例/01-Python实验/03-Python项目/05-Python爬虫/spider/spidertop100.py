import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
import os

"""
    爬虫示例程序，爬取猫眼电影榜单
    学习requests模块的使用，HTTP(GET, POST)
"""

# 添加请求头部信息, 一些网站会通过请求头部信息来区分是爬虫程序还是用户浏览
headers = {'Accept': 'text/html',
           'Host': 'maoyan.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/72.0.3626.119 Safari/537.36 '
           }

# 爬取的目标站点URL
URL = 'https://maoyan.com/board/4'


# 抓取一个页面
def getHtmlPage(url: str, page: dict) -> str:
    try:
        response = requests.get(url, params=page, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None



def parseHtmlPage(text):
    """
        使用正则表达式提取感兴趣的信息，这里需要自己分析HTML页面，并且会HTML基础
        如下正则表达式将提取如下信息
       { "index": "11", "img_src": "https://p1.meituan.net/movie/6bc004d57358ee6875faa5e9a1239140128550.jpg@160w_220h_1e_1c", 
       "title": "音乐之声", "actor": "朱莉·安德鲁斯,克里斯托弗·普卢默,埃琳诺·帕克", "time": "1965-03-02(美国)", "score": "90" }
    """
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?title="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
        r'.*?integer">(.*?).</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, text)
    for item in items:
        # 生成器
        yield {
            'index': item[0].strip(),
            'img_src': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


# 将感兴趣的信息序列化，保存到文件
def writeJsonFile(item):
    with open('./result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


def main(offset):
    page = {}
    page.update(offset=offset)
    html = getHtmlPage(URL, page)
    # print(html)
    for item in parseHtmlPage(html):
        writeJsonFile(item)
        print(item)


if __name__ == '__main__':
    # os.remove('./result.txt')
    # 多线程
    pool = Pool()
    pool.map(main, [i * 10 for i in range(0, 11)])
