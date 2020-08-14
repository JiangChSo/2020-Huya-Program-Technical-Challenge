import requests
from bs4 import BeautifulSoup
import random
import time
import csv
import jieba.analyse
import jieba
import pypinyin

# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

list_content = []
list_t = []


#代理
def get_header():
    header1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }
    header2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3868.400"
    }
    header3 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
    }
    header_list = [header1, header2, header3]
    index = random.randint(0, 1)
    return header_list[index]
    pass


# 从微博网站获取数据
def get_data(url):
    j = 0
    time_sleep = random.randint(0, 1)
    req = requests.get(url=url, headers=get_header())
    req.encoding = "utf-8"
    # print("响应码：", req.status_code)
    print("start")
    html = req.text
    # print(html)
    bf = BeautifulSoup(html, "lxml")
    # print(bf)
    div_content = bf.find_all("tr", class_="")
    t = 1
    fp = open('weibocut.csv', 'w', encoding='utf_8_sig', newline='')
    writer = csv.writer(fp)  # 获取文件“写笔”
    for item in div_content:
        time.sleep(time_sleep)
        # 去掉第一条信息
        if (t == 1):
            t = 0
            continue
        time.sleep(time_sleep)
        # 获取当前热搜主题
        topical_subject = item.select("td")[1].select("a")[0].string
        url = item.select("a")[0]["href"]
        # 获取当前热搜页面内容
        url = "https://s.weibo.com"+url
        print(url)#显示当前访问的热搜链接
        #print(topical_subject)

        #print("111111111111")
        #跳过反爬虫程序代码
        if(url == "https://s.weibo.comjavascript:void(0);"):
            continue
        newcontent = requests.get(url= url,headers=get_header())

        #print("2222222222")
        newcontent.encoding = "utf-8"
        soup_list = BeautifulSoup(newcontent.text, 'html.parser')
        #print(soup_list)

        headers = ['id', 'TopKeywords', 'context']
        for i in range(10):
             headers.append('keyword' + str(i + 1))

        writer.writerow(headers)  # 写入一行记录
        for news in soup_list.find_all("p",class_="txt"):
             j = j+1
             #print(str(j)) 调试查看进度
             context = news.text
             #print(context)
             kWords = jieba.analyse.extract_tags(context, topK=10, withWeight=False, allowPOS=('n'))
             values = [j, topical_subject, context]
             for kword in kWords:
                 kword = pinyin(kword)#将关键词转换为拼音
                 values.append(kword)
             writer.writerow(values)
    fp.close()
    # print(list_content)
    print("end")

if __name__ == '__main__':
    print("微博热搜爬取开始")
    # 获取微博热搜数据
    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    get_data(url)

    # 存储微博要闻数据
    #url = "https://s.weibo.com/top/summary/summary?cate=socialevent"
    #get_data(url)

    print("爬取结束")