# -*- coding: utf-8 -*-

import sys
import getopt


def _show_usage():
	print("""

Usage:
    python """ + sys.argv[0].split('/')[-1] + """ <command> <options>

Commands:
    No command yet.(●'◡'●)

General Options:
    -h, --help		Show help, wothout option.
    -s, --save		Weather to keep the cache.
    -f, --flush-cache	Refresh the cache, and you can get the latest webpage

  After option, you have to make a choice or you may get an error. 
    Yes			'y', 'Y', 'yes'
    No			'n', 'N', 'no'
			
		""")


def get_options(argv):
	weather_save = 'y'  # 默认保存
	refresh = 'n'  # 默认不获取最新
	try:
		opts, args = getopt.getopt(argv[1:], "hs:f:", ["help", "save=", "flush-cache="])
	except getopt.GetoptError:
		print("""
		\rOops! An ERROR happened.
		\rType "python """ + argv[0].split('/')[-1] + """ -h" for more help.
	""")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			_show_usage()
			exit(0)
		elif opt in ('-s', '--save'):
			weather_save = arg
		elif opt in ('-f', '--flush-cache'):
			refresh = arg

	return weather_save, refresh
