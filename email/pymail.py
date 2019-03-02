#! python3
#coding:utf-8 
import os
import sys 
import options
import smtplib 
import datetime
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText    

import asina


def add_image(src, img_name):
	image = MIMEImage(open(src, 'rb').read(), _subtype='jpg')
	image.add_header('Content-Disposition', 'attachment', filename = img_name)
	return image


def today():
	"""
	return 今天的日期，形如 '2019-03-02'
	"""
	# date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
	# year = date.year
	# month = date.month
	# day = date.day
	return datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")  # string


def send_mail(user, password, receiver):
	# 构造邮件头
	mail = MIMEMultipart("mixed")  
	mail['From'] = user
	mail['To'] = "鱼丸粗面" 
	mail['Subject'] = Header('福利','utf-8')
	# 邮件体
	message = MIMEText("老板，这两天的福利", 'plain', 'utf-8')
	mail.attach(message)
	if flush in ['y', 'Y', 'yes']:
		html = asina.get_html()
	elif os.path.exists(CACHE_FILE):
		html = open(CACHE_FILE, 'r').read()
		print("The cache ready exists.")
	else:
		html = asina.get_html()
	HTML = MIMEText(html, _subtype='html', _charset='utf-8')
	mail.attach(HTML)
	#mail.attach(add_image(r'cat.jpg', 'cat'))

	try:  
		smtp = smtplib.SMTP_SSL()
		smtp.connect(mail_host, 465)
		smtp.login(user, password)
		smtp.sendmail(user, receiver, mail.as_string())
		smtp.quit()
		print("Send mail success.")
		if save in ['y', 'Y', 'yes']:
			f = open(CACHE_FILE, 'w')
			f.write(html)
			f.close()
			print("Flushed the cache.")
		elif save in ['n', 'N', 'no']:
			print("No save or refresh cache.")
		else:
			print("Error 'Save' option. No save or refresh cache.")
	except (smtplib.SMTPException, TimeoutError) as e:
		print(e)

if __name__ == "__main__":
	# host
	SINA = "yuwancumiana@sina.cn"
	GMAIL = "yuwancumian666@gmail.com"
	QQMAIL = "2506930314@qq.com"

	os.chdir(sys.path[0])
	CACHE_FILE = "cache/cache-" + today() + ".html"

	# save or refresh cache.
	save, flush = options.get_options(sys.argv)

	# user info
	mail_host="smtp.sina.cn"
	mail_user="yuwancumiana@sina.cn"
	mail_pass="mq2020."
	sender = 'yuwancumiana@sina.cn'  
	receivers = ['2506930314@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱 ,'2535257276@qq.com','635936876@qq.com' 
	
	send_mail(mail_user, mail_pass, receivers)
