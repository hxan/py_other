import requests
from lxml import etree
from urllib import request

# 制作一个请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}
fp = open('./4399.txt','a',encoding='utf-8')
# 采集源码
def index():
    for page in range(2,17):
        base_url = 'http://www.4399.com/flash_fl/more_6_{}.htm'.format(page)
        # print(base_url)
        response = requests.get(base_url,headers=headers)
        response.encoding = 'gb2312'
        html = response.text
        # print(html)
        htmls = etree.HTML(html)  # 抓取到html源码处理成可以用xpath守则的格式
        clean(htmls)
# 清洗源码
def clean(htmls):
    gname_list = htmls.xpath('//ul[@class="list affix cf"]/li/a/img/@alt')
    pic_url = htmls.xpath('//ul[@class="list affix cf"]/li/a/img/@lz_src')
    # sto(gname_list)  # 调用信息保存模块
    download(pic_url) # 调用图片下载模块

# 信息保存
def sto(g_list):
    for name in g_list:
        print(name)
        fp.write(name + '\n')

# 图片下载
def download(pic_list):
    for url in pic_list:
        print('loading....',url)
        pic_name = url.split('/')[-1]
        request.urlretrieve(url,'./pic/'+pic_name)

if __name__ == '__main__':
    index()
    fp.close()