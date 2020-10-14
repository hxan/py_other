from urllib import request
for i in range(0,10):
	req=request.Request('https://tieba.baidu.com/f?kw=python&ie=utf-8&pn='+str(i*50),headers={'User-Agent':' '})
	response = request.urlopen(req)
	print(response.read().decode('utf-8'))