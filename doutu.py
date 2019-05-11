import requests
import time
import urllib.request
import os
from lxml import etree
import random
'''
网址 https://www.doutula.com/
//div[@class='col-xs-6 col-sm-3']/img[@referrerpolicy='no-referrer']/@src

'''
def getUrls(start_page,end_page):
	urls_list = []
	for page in range(start_page,end_page + 1):
		url = 'https://www.doutula.com/article/list/?page='
		url += str(page)
		urls_list.append(url)
	return urls_list

def getImgSrc(page_list):
	print('正在获取所有图片信息')
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple'\
	'WebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36',
	}
	img_src_list = []
	img_name_list = []
	for url in page_list:
		print('正在获取%s信息' % url)
		response = requests.get(url=url,headers=headers)
		tree = etree.HTML(response.text)
		img_list = tree.xpath("//div[@class='col-xs-6 col-sm-3']/img[@referrerpolicy='no-referrer']/@data-original")
		name_list = tree.xpath("//div[@class='col-xs-6 col-sm-3']/img[@referrerpolicy='no-referrer']/@alt")
		img_src_list.extend(img_list)
		img_name_list.extend(name_list)
		time.sleep(random.random())
		print('%s信息获取完成' % url)
	print('图片信息获取完成')
	return img_src_list,img_name_list

def downloadImgs(img_src_list,img_name_list):
	if not os.path.exists(r'doutu'):
		os.mkdir('doutu')
	for src,name in zip(img_src_list,img_name_list): 
		#获取图片后缀
		print('正在下载...%s' % name)
		imghz = os.path.splitext(src)[1]
		filepath = 'doutu\\' + str(name) + str(imghz)
		try:
			urllib.request.urlretrieve(src,filepath)
		except:
			continue
		time.sleep(random.random())
		print('下载完成...%s' % name)

def main():
	start_page = int(input('请输入爬取起始页'))
	end_page = int(input('亲输入爬取结束页'))
	#获取所有爬取的页面
	page_list = getUrls(start_page,end_page)
	#获取所有的图片src
	img_src_list,img_name_list = getImgSrc(page_list)
	downloadImgs(img_src_list,img_name_list)


if __name__ == '__main__':
	main()
