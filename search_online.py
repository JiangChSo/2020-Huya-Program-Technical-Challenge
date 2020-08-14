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
def get_data(wordlist):
    #每一次爬取开始标记为0 并且重新计入表头['id', 'TopKeywords', 'context'] 不影响模糊匹配查询
    j = 0
    fp = open('weibo_search_online.csv', 'a', encoding='utf_8_sig', newline='')
    writer = csv.writer(fp)  # 获取文件“写笔”
    headers = ['id', 'TopKeywords', 'context']
    for i in range(10):
        headers.append('keyword' + str(i + 1))

    writer.writerow(headers)  # 写入一行记录

    for word in wordlist:
        print("正在爬取词："+word)
        url = "https://s.weibo.com/weibo?q="+ word +"&wvr=6&b=1&Refer=SWeibo_box"
        newcontent = requests.get(url=url, headers=get_header())

        newcontent.encoding = "utf-8"
        soup_list = BeautifulSoup(newcontent.text, 'html.parser')
        for news in soup_list.find_all("p", class_="txt"):
            j = j + 1
            # print(str(j)) 调试查看进度
            context = news.text
            # print(context)
            kWords = jieba.analyse.extract_tags(context, topK=10, withWeight=False, allowPOS=('n'))
            #print(news)
            topical_subject = word
            #print(topical_subject)
            values = [j, topical_subject, context]
            for kword in kWords:
                kword = pinyin(kword)  # 将关键词转换为拼音
                values.append(kword)
            writer.writerow(values)
    fp.close()
    # print(list_content)
    #print("end")
    #可直接在列表中添加词语或者句子，即将对应的搜索数据存入

'''
前三个search均为匹配则执行search_online.py中的extendcsv
'''
def  extendcsv(string):
    kWords = jieba.analyse.extract_tags(string, topK=10, withWeight=False, allowPOS=('n'))
    get_data(kWords)
    print("爬取结束")