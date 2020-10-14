import urllib.request
from urllib.parse import quote
import json
import http.cookiejar
import time
import math
import random
import pandas as pd
from lxml import etree
import csv


headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
link_name = []
next_url_list = []
total_dict=pd.DataFrame()
def writePage(html, filename):
    # 把文本保存在本地
    # filename 表示文本的路径，操作文本的方式权限
    with open(filename, "a",encoding='utf-8') as f:
        f.write(html)
        f.write('\n')



def loadNextLink(url,path):
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    content = etree.HTML(response.read().decode("utf-8"))
    link_movie=content.xpath(path)
    return link_movie
def loadInfo(url,filename):
    list_title = ['片名','导演', '编剧', '主演', '类型', '制片国家/地区','语言', '上映时间', '片长', '又名', 'IMDB链接']
    dict = {}
    url=url+"/"
    link_movie=loadNextLink(url,"//div[@class='mod movie-list']/dl/dd/a/@href")
    for movie in link_movie:
        name=loadNextLink(movie,"//div[@id='info']/span/span")
        num=0
        title=loadNextLink(movie,"//span[@property='v:itemreviewed']/text()")[0]
        dict[list_title[num]] = title
        num+=1
        for i in name:
            link=i.xpath("a/text()")
            if(link!=[]):
                dict[list_title[num]]="/".join(link)
                num+=1
        types=loadNextLink(movie,"//div/span[@property='v:genre']/text()")
        dict[list_title[num]]="/".join(types)
        num+=1
        country=loadNextLink(movie,"//span[text()='制片国家/地区:']/following::text()")[0]
        dict[list_title[num]] = country
        num+=1
        language=loadNextLink(movie,'//span[text()="语言:"]/following::text()')[0]
        dict[list_title[num]]=language
        num+=1
        date=loadNextLink(movie,"//span[@property='v:initialReleaseDate']/text()")
        dict[list_title[num]]="/".join(date)
        num+=1
        times=loadNextLink(movie,"//span[@property='v:runtime']/text()")
        dict[list_title[num]] = times
        num+=1
        another_name=loadNextLink(movie,"//span[text()='又名:']/following::text()")[0]
        dict[list_title[num]] = another_name
        num+=1
        imdb=loadNextLink(movie,"//span[text()='IMDb链接:']/following::a/text()")[0]
        dict[list_title[num]] = imdb

        dataframe=pd.DataFrame(dict)
        total_dict.append(dataframe)


def find_index():
    url = "http://www.douban.com/"
    #获取电影分类的url
    movie_name = loadNextLink(url, "//div[@class='mod']/div[@class='tags list']/ul/li/a/@href")
    for i in movie_name:
        i = i[29:]
        #转码
        next_url = url + 'tag/' + quote(i)+"/movie?start="
		#选择前30页
        for num in range(30):
            next_url=next_url+str(num*15)
            loadInfo(next_url,i+".txt")
     #写进CSV文件
    total_dict.to_csv("movie.csv",index=False,header=False)

if __name__=='__main__':
    find_index()