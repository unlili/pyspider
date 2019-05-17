'''
爬取指定贴吧，指定页面的所有高清图片
'''
import requests
import time
import re
import os
import urllib.request
import random
from lxml import etree

class TiebaSpider:

	def __init__(self,kw,start,end):

		#贴吧名
		self.kw = kw
		#爬取的开始页
		self.start = start
		#爬取的结束也
		self.end = end
		self.url = 'http://tieba.baidu.com/f?kw={0}&ie=utf-8&pn={1}'
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple'\
			'WebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'}	

	def startCrawl(self):
		allUrl = self._getAllUrl()
		detailed = self._getDetailed(allUrl)
		allSrc = self._getAllSrc(detailed)
		self._downLoad(allSrc)

	def _count(self):
		for x in range(1,1000000):
			yield x

	def _getAllUrl(self):
		# 0 50 100 150 200
		#50(I-1)
		# 1 2  3  4  5
		allUrl = []
		print('-------------正在合成所有爬取页面的url-------------')
		for i in range(self.start,self.end+1): 
			page = str(50*(i-1))
			url = self.url.format(self.kw,page)
			allUrl.append(url)
		print('-------------url合成ok-------------')
		return allUrl

	def _getDetailed(self,allUrl):
		print('-------------正在获取每一楼详细url-------------')
		detailed = []
		for i in range(len(allUrl)):
			print('---获取 %s 中' % allUrl[i])
			r = requests.get(url=allUrl[i],headers=self.headers)
			pattern = re.compile(r'<a rel="noreferrer" href="(.*?)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>')
			ret = pattern.findall(r.text)
			detailed += ret
			time.sleep(random.random())
			print('---获取 %s 完成' % allUrl[i])
		#print(detailed)
		print('-------------所有楼层url获取完成-------------')
		return detailed

	def _getAllSrc(self,detailed):
		allSrc = []
		print('-------------正在获取所有src-------------')
		for ur in detailed:
			url = 'http://tieba.baidu.com'
			url += ur
			print('---正在获取%s的所有src' % url)
			#print('正在爬取{0}----'.format(url))
			r = requests.get(url=url,headers=self.headers)
			r.encoding = 'utf8'
			tree = etree.HTML(r.text)
			ret = tree.xpath("//div/img[@class='BDE_Image']/@src")
			allSrc += ret
			time.sleep(random.random())
			print('---%s的所有src获取完成' % url)
		print('-------------所有src获取完成-------------')
		return allSrc

	def _downLoad(self,allSrc):
		print('-------------开始下载图片-------------')
		if not os.path.exists(self.kw):
			os.mkdir(self.kw)
		name = self._count()
		for src in allSrc:
			na = next(name)
			imghz = os.path.splitext(src)[1]
			filepath = self.kw + '\\' + str(na) + imghz
			try:
				print('---正在下载第%d张' % na)
				urllib.request.urlretrieve(src,filepath)
				#程序员何苦为难程序员
				time.sleep(random.random()*2)
				print('---第%d张下载完成' % na)
			except:
				continue
		print('-------------图片下载完成-------------')

#--------------------------------------------------------
# qbhn = TiebaSpider('桥本环奈',1,1)
# qbhn.startCrawl()
# #--------------------------------------------------------
# b = TiebaSpider('bilibili',1,1)
# b.startCrawl()
# #--------------------------------------------------------
# #--------------------------------------------------------
# b = TiebaSpider('后宫动漫',1,1)
# b.startCrawl()
# #--------------------------------------------------------

b = TiebaSpider('后宫动漫',1,2)
b.startCrawl()
		