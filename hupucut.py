import requests
from bs4 import BeautifulSoup
import csv
import jieba.analyse

import pypinyin

# 不带声调的拼音转换函数
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

endpage = 80 #记录爬取的最多页数为 endpage，修改这个值可以爬取到更多的数据 注：endpage>=2


'''
NBA新闻爬取
'''
url ='https://voice.hupu.com/nba/1'
j=0
reslist = requests.get(url)
reslist.encoding = 'utf-8'
soup_list = BeautifulSoup(reslist.text, 'html.parser')

    # 列表写入
    # 设置记录标题(列表)和记录值(一个嵌套元组集或列表集的列表)
headers = ['id', 'title', 'context']
for i in range(10):
    headers.append('keyword'+str(i+1))
fp = open('hupucut.csv', 'w', encoding='utf_8_sig', newline='')
writer = csv.writer(fp)  # 获取文件“写笔”
writer.writerow(headers)  # 写入一行记录
print(str(1))#记录爬取到第一页
for news in soup_list.select('li'):  # 首页
    if len(news.select('h4')) > 0:
        j=j+1
        # 标题
        title = news.find('h4').text
        href=news.find('h4').a['href']
        reslist = requests.get(href)
        reslist.encoding = 'utf-8'
        soup = BeautifulSoup(reslist.text, 'html.parser')
        context=soup.select('div .artical-main-content')[0].text
        #allowPOS=(‘ns’, ‘n’, ‘vn’, ‘v’)
        kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
        values = [j,title,context]
        for kword in kWords:
            kword = pinyin(kword)
            values.append(kword)
        # 使用open函数时设置参数encoding以防止乱码

        writer.writerow(values)  # 写入多行记录，传入的参数为列表结构
        #print("文章标题：" + title)
        #print(context)
        # print('https://voice.hupu.com/nba/%s' %i)
# 后面的页数
#endpage
for i in range(2, endpage + 1):
    pages = i;
    print(i)
    nexturl = 'https://voice.hupu.com/nba/%s' % (pages)
    # nexturl = '%s%s%s' % (head, pages, tail)
    newcontent = requests.get(nexturl)
    newcontent.encoding = 'utf-8'
    soup_list = BeautifulSoup(newcontent.text, 'html.parser')
    for news in soup_list.select('li'):
        if len(news.select('h4')) > 0:
            j = j + 1
            # print(j)
            # 标题
            title = news.find('h4').text
            href = news.find('h4').a['href']
            reslist = requests.get(href)
            reslist.encoding = 'utf-8'
            soup = BeautifulSoup(reslist.text, 'html.parser')
            context = soup.select('div .artical-main-content')[0].text

            kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
            values = [j,title,context]
            for kword in kWords:
                kword = pinyin(kword)#将关键词转换为拼音
                values.append(kword)
            writer.writerow(values)
            #print("文章标题：" + title)
print('NBA新闻爬取finish')

'''
开始爬取国际足球新闻
'''

url ='https://voice.hupu.com/soccer'

reslist = requests.get(url)
reslist.encoding = 'utf-8'
soup_list = BeautifulSoup(reslist.text, 'html.parser')

    # 列表写入
    # 设置记录标题(列表)和记录值(一个嵌套元组集或列表集的列表)


print(str(1))#记录爬取到第一页
for news in soup_list.select('li'):  # 首页
    if len(news.select('h4')) > 0:
        j=j+1
        # 标题
        title = news.find('h4').text
        href=news.find('h4').a['href']
        reslist = requests.get(href)
        reslist.encoding = 'utf-8'
        soup = BeautifulSoup(reslist.text, 'html.parser')
        context=soup.select('div .artical-main-content')[0].text
        #allowPOS=(‘ns’, ‘n’, ‘vn’, ‘v’)
        kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
        values = [j,title,context]
        for kword in kWords:
            kword = pinyin(kword)
            values.append(kword)
        # 使用open函数时设置参数encoding以防止乱码

        writer.writerow(values)  # 写入多行记录，传入的参数为列表结构
        #print("文章标题：" + title)
        #print(context)
        # print('https://voice.hupu.com/nba/%s' %i)
# 后面的页数

for i in range(2, endpage + 1):
    pages = i;
    print(i)
    nexturl = 'https://voice.hupu.com/soccer/%s' % (pages)
    # nexturl = '%s%s%s' % (head, pages, tail)
    newcontent = requests.get(nexturl)
    newcontent.encoding = 'utf-8'
    soup_list = BeautifulSoup(newcontent.text, 'html.parser')
    for news in soup_list.select('li'):
        if len(news.select('h4')) > 0:
            j = j + 1
            # print(j)
            # 标题
            title = news.find('h4').text
            href = news.find('h4').a['href']
            reslist = requests.get(href)
            reslist.encoding = 'utf-8'
            soup = BeautifulSoup(reslist.text, 'html.parser')
            context = soup.select('div .artical-main-content')[0].text

            kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
            values = [j,title,context]
            for kword in kWords:
                kword = pinyin(kword)#将关键词转换为拼音
                values.append(kword)
            writer.writerow(values)
            #print("文章标题：" + title)
print('国际足球新闻爬取finish')


'''
开始爬取CBA新闻
'''

url ='https://voice.hupu.com/cba'

reslist = requests.get(url)
reslist.encoding = 'utf-8'
soup_list = BeautifulSoup(reslist.text, 'html.parser')

    # 列表写入
    # 设置记录标题(列表)和记录值(一个嵌套元组集或列表集的列表)


print(str(1))#记录爬取到第一页
for news in soup_list.select('li'):  # 首页
    if len(news.select('h4')) > 0:
        j=j+1
        # 标题
        title = news.find('h4').text
        href=news.find('h4').a['href']
        reslist = requests.get(href)
        reslist.encoding = 'utf-8'
        soup = BeautifulSoup(reslist.text, 'html.parser')
        context=soup.select('div .artical-main-content')[0].text
        #allowPOS=(‘ns’, ‘n’, ‘vn’, ‘v’)
        kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
        values = [j,title,context]
        for kword in kWords:
            kword = pinyin(kword)
            values.append(kword)
        # 使用open函数时设置参数encoding以防止乱码

        writer.writerow(values)  # 写入多行记录，传入的参数为列表结构
        #print("文章标题：" + title)
        #print(context)
        # print('https://voice.hupu.com/nba/%s' %i)
# 后面的页数

for i in range(2, endpage + 1):
    pages = i;
    print(i)
    nexturl = 'https://voice.hupu.com/cba/%s' % (pages)
    # nexturl = '%s%s%s' % (head, pages, tail)
    newcontent = requests.get(nexturl)
    newcontent.encoding = 'utf-8'
    soup_list = BeautifulSoup(newcontent.text, 'html.parser')
    for news in soup_list.select('li'):
        if len(news.select('h4')) > 0:
            j = j + 1
            # print(j)
            # 标题
            title = news.find('h4').text
            href = news.find('h4').a['href']
            reslist = requests.get(href)
            reslist.encoding = 'utf-8'
            soup = BeautifulSoup(reslist.text, 'html.parser')
            context = soup.select('div .artical-main-content')[0].text

            kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
            values = [j,title,context]
            for kword in kWords:
                kword = pinyin(kword)#将关键词转换为拼音
                values.append(kword)
            writer.writerow(values)
            #print("文章标题：" + title)
print('CBA新闻爬取finish')

'''
开始爬取中国足球新闻
'''

url ='https://voice.hupu.com/china'

reslist = requests.get(url)
reslist.encoding = 'utf-8'
soup_list = BeautifulSoup(reslist.text, 'html.parser')

    # 列表写入
    # 设置记录标题(列表)和记录值(一个嵌套元组集或列表集的列表)


print(str(1))#记录爬取到第一页
for news in soup_list.select('li'):  # 首页
    if len(news.select('h4')) > 0:
        j=j+1
        # 标题
        title = news.find('h4').text
        href=news.find('h4').a['href']
        reslist = requests.get(href)
        reslist.encoding = 'utf-8'
        soup = BeautifulSoup(reslist.text, 'html.parser')
        context=soup.select('div .artical-main-content')[0].text
        #allowPOS=(‘ns’, ‘n’, ‘vn’, ‘v’)
        kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
        values = [j,title,context]
        for kword in kWords:
            kword = pinyin(kword)
            values.append(kword)
        # 使用open函数时设置参数encoding以防止乱码

        writer.writerow(values)  # 写入多行记录，传入的参数为列表结构
        #print("文章标题：" + title)
        #print(context)
        # print('https://voice.hupu.com/nba/%s' %i)
# 后面的页数

for i in range(2, endpage + 1):
    pages = i;
    print(i)
    nexturl = 'https://voice.hupu.com/china/%s' % (pages)
    # nexturl = '%s%s%s' % (head, pages, tail)
    newcontent = requests.get(nexturl)
    newcontent.encoding = 'utf-8'
    soup_list = BeautifulSoup(newcontent.text, 'html.parser')
    for news in soup_list.select('li'):
        if len(news.select('h4')) > 0:
            j = j + 1
            # print(j)
            # 标题
            title = news.find('h4').text
            href = news.find('h4').a['href']
            reslist = requests.get(href)
            reslist.encoding = 'utf-8'
            soup = BeautifulSoup(reslist.text, 'html.parser')
            context = soup.select('div .artical-main-content')[0].text

            kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
            values = [j,title,context]
            for kword in kWords:
                kword = pinyin(kword)#将关键词转换为拼音
                values.append(kword)
            writer.writerow(values)
            #print("文章标题：" + title)
print('中国足球新闻爬取finish')



'''
开始爬取综合足球新闻
'''

url ='https://voice.hupu.com/sports'

reslist = requests.get(url)
reslist.encoding = 'utf-8'
soup_list = BeautifulSoup(reslist.text, 'html.parser')

    # 列表写入
    # 设置记录标题(列表)和记录值(一个嵌套元组集或列表集的列表)


print(str(1))#记录爬取到第一页
for news in soup_list.select('li'):  # 首页
    if len(news.select('h4')) > 0:
        j=j+1
        # 标题
        title = news.find('h4').text
        href=news.find('h4').a['href']
        reslist = requests.get(href)
        reslist.encoding = 'utf-8'
        soup = BeautifulSoup(reslist.text, 'html.parser')
        context=soup.select('div .artical-main-content')[0].text
        #allowPOS=(‘ns’, ‘n’, ‘vn’, ‘v’)
        kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
        values = [j,title,context]
        for kword in kWords:
            kword = pinyin(kword)
            values.append(kword)
        # 使用open函数时设置参数encoding以防止乱码

        writer.writerow(values)  # 写入多行记录，传入的参数为列表结构
        #print("文章标题：" + title)
        #print(context)
        # print('https://voice.hupu.com/nba/%s' %i)
# 后面的页数
endpagecom = 16
for i in range(2, endpagecom + 1):
    pages = i;
    print(i)
    nexturl = 'https://voice.hupu.com/sports/%s' % (pages)
    # nexturl = '%s%s%s' % (head, pages, tail)
    newcontent = requests.get(nexturl)
    newcontent.encoding = 'utf-8'
    soup_list = BeautifulSoup(newcontent.text, 'html.parser')
    for news in soup_list.select('li'):
        if len(news.select('h4')) > 0:
            j = j + 1
            # print(j)
            # 标题
            title = news.find('h4').text
            href = news.find('h4').a['href']
            reslist = requests.get(href)
            reslist.encoding = 'utf-8'
            soup = BeautifulSoup(reslist.text, 'html.parser')
            context = soup.select('div .artical-main-content')[0].text

            kWords = jieba.analyse.extract_tags(context, topK=10,withWeight=False,allowPOS = ('n'))
            values = [j,title,context]
            for kword in kWords:
                kword = pinyin(kword)#将关键词转换为拼音
                values.append(kword)
            writer.writerow(values)
            #print("文章标题：" + title)
print('综合新闻爬取finish')




fp.close()