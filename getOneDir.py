#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys, os
import github

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("usage:  %s url1 url2 ..." % (os.path.basename(__file__)))
	else:
		for url in [sys.argv[i] for i in range(1, len(sys.argv))]:
			#print(url.split('//'))
			if "github.com" in url:
				github.getSubDir(url)