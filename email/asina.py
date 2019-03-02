#! python3
# -*- coding:utf-8 -*- 
import re
import sys
import time
import datetime
import random
import requests
from datetime import date
from bs4 import BeautifulSoup as bs


def download(url, proxy=None, num_retries=2):
	headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
	print ("Downloading: "+url+"...")
	try:
		response = requests.get(url=url, headers=headers)
		time.sleep(random.random())  # sleep for [0, 1) second.
		html = response.text
	except requests.exceptions.RequestException as e:
		print ("Download Error: " + str(e.args))
		html = None
		if num_retries > 0:
			if 500 <= response.status_code < 600:
				return download(url, num_retries-1)
	return html


def get_html():
	# USEFUL_URL = [
	# 	"https://asina.me/"
	# 	"https://asina.vip/",
	# 	"https://gzxy.me/",
	# ]
	HTML = ''
	url = "https://asina.me/page/1"
	html = download(url)
	if html == None:
		print(u"page not exist...")
		return None
	soup = bs(html, 'lxml')
	article_list = soup.find_all('article')
	del article_list[0]  # 删除首页公告
	
	for i,j in enumerate(article_list):
		string = j.find('time').string
		date_ = time.strptime(string, '%Y-%m-%d')
		article_date = date(date_[0], date_[1], date_[2])
		target_date = date.today() - datetime.timedelta(2)
		if article_date == target_date:
			article_list = article_list[:i]
	img_list = _get_info(article_list, tag_name = 'img', attr = 'src')
	link_list = _get_info(article_list, tag_name = 'a', attr = 'href')
	time_list = _get_info(article_list, tag_name = 'time')
	title_list = _get_info(article_list, tag_name = 'h2')
	href_list, pass_list = _get_bd_link(link_list)
	list = [link_list, title_list, time_list, img_list, href_list, pass_list]
	HTML += _generate_html(list)
	print('Finally got '+str(len(article_list))+' links.')
	return "<!DOCTYPE html>\n<html>\n<body>\n" + HTML + "</body>\n</html>"


def _get_info(article_list, tag_name = None, attr = None):
	list = []
	for tag in article_list:
		if tag.find('img') == None:
			continue
		if attr == None:
			list.append(tag.find(tag_name).string)
		else:
			list.append(tag.find(tag_name)[attr])
	return list

	
def _get_bd_link(link_list):
	href_list = []
	pass_list = []
	for link in link_list:
		html = download(link)
		soup = bs(html, 'lxml')
		try:
			str = soup.find('meta',content=re.compile('pan.baidu'))['content']
			href = re.search("(https|http)[\\S]+", str).group()
			password = re.search("提取码: [\\w]{4}", str).group()[-4:]
		except:
			print ("can't parse the BaiduDisk Link")
			href = ""
			password = ""
		href_list.append(href)
		pass_list.append(password)
		
	return href_list, pass_list

	
def _generate_html(list):
	html = ''
	print(list)
	for i in range(len(list[0])):
		html += (u'''
		<article>
			<header>
				<h2><a target="_blank" href=''' + list[0][i] + '''>''' + list[1][i] + '''</a></h2>
				<div> 
				<p>''' + list[2][i] + '''</p>
				</div>
			</header>
			<p style="text-align:center">
				<img src="''' + list[3][i] + '''"/>
			</p>
			<footer> 
				<p style="text-align: right"><a href="''' + list[4][i] + '''">''' + list[5][i] + '''</a></p>
			</footer>
		</article>
		''')
	
	return html


if __name__ == '__main__':
	html = get_html()
	fout = open('output.html', 'w') 
	fout.write(html)
	fout.close()
	
	
