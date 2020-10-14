import requests
import json
import re
import urllib.request
from urllib.parse import quote
from lxml import etree
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter
fp = open('./title.txt','a',encoding='utf-8')
base_url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit=20'

class spider:
	base_url=''
	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
	}
	def __init__(self, base_url):
		self.base_url=base_url

	def __del__(self):
		pass

	def getMoive(self,pages):
		#try
		jsons = requests.get(base_url,headers=self.headers).text
		dicts = json.loads(jsons)
		if(jsons==' 'or dicts==' '):
			return 0
		for i in range(0,len(dicts)):
			fp.writelines(dicts[i]['title']+'\n')
			print(dicts[i]['title'])
			print('    '+'国家:'+dicts[i]['regions'][0])
			print('    '+'评分:'+dicts[i]['rating'][0])
			print('    '+'上映日期:'+dicts[i]['release_date'])
			print(' ')
		#except


with PyCallGraph(output=GraphvizOutput()):  
	for j in range(1,30):
		for i in range(0,10):
			base_url='https://movie.douban.com/j/chart/top_list?type='+str(j)+'&interval_id=100%3A90&action=&start='+str(i*20)+'&limit=20'
			a=spider(base_url)
			if( a.getMoive(0) ):
				break;