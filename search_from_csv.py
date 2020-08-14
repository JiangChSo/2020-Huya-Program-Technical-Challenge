import csv
import jieba.analyse
import jieba
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import pypinyin
from search_online import extendcsv
import threading #导入多线程模块

'''
不带声调的拼音转换
'''
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s
'''
模糊匹配器
token_set_ratio——对字符串进行标记（tokenizes）并比较交集和余数 
匹配得分95则成功
'''
def fuzzyMatch(value, list):
    #设置匹配精度为95%
    result = process.extractOne(value, list, scorer= fuzz.token_sort_ratio, score_cutoff=95)
    return result


def search_from_csv(string,load):
    kWords = jieba.analyse.extract_tags(string, topK=10, withWeight=False, allowPOS=('n'))
    with open(load, "rt", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for kw in kWords:
                #if kw in row[3:-1]:
                #print(kw)
                kw = pinyin(kw)#准换为拼音
                if(fuzzyMatch(kw, row[3:-1])):
                    #print(row)
                    return row[2].strip('#\n\t').replace(' ','')
    return ''


def  last_search_func(string):
    search_result1 = search_from_csv(string, load='weibocut.csv')#查询微博热搜词库 微博热词前30
    if(search_result1 != ''):
        return search_result1

    search_result2 = search_from_csv(string, load='hupucut.csv')#查询虎扑新闻词库 包括NBA、CBA、世界足球、中国足球
    if(search_result2 != ''):
        return  search_result2
    search_result3 = search_from_csv(string, load='weibo_search_online.csv')#扩展词库
    if(search_result3 != ''):
        return search_result3
    #若上述三个词库均关键词模糊匹配失败，则扩展词库
    extendcsv(string)
    #对扩展之后的词库进行查询
    search_result4= search_from_csv(string, load='weibo_search_online.csv')
    if (search_result4 != ''):#原则上肯定不为空，避免程序崩溃
        return search_result4
    else:
        return ''




if __name__ == "__main__":
    string = '计算机科学'
    search_result = last_search_func(string)
    print(search_result)