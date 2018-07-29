import urllib2, lxml.html, sys, os, commands

header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'}

def getDirAndFileList(url):
	#print(sys._getframe().f_code.co_name)
	req = urllib2.Request(url=url, headers=header)
	dirList = []
	fileList = []
	try:
		html = urllib2.urlopen(req, timeout=120).read()
		doc  = lxml.html.fromstring(html)
		itemList = doc.xpath('//div[@class="file-wrap"]/table/tbody/tr[@class="js-navigation-item"] | \
			//include-fragment[@class="file-wrap"]/table/tbody/tr[@class="js-navigation-item"]')
		#print(len(itemList))
		for row in itemList:
			#print(row.xpath('td[@class="icon"]/svg/@class')[0])
			if 'directory' in row.xpath('td[@class="icon"]/svg/@class')[0]:
				#print(row.xpath('td[@class="icon"]/svg/@class')[0])
				if 'This path' in row.xpath('td[@class="content"]/span/a/@title')[0]:
					dirList.append( row.xpath('td[@class="content"]/span/a/span/text()')[0] + 
						row.xpath('td[@class="content"]/span/a/text()')[0] )
					# print(row.xpath('td[@class="content"]/span/a/span/text()')[0] + 
					# 	row.xpath('td[@class="content"]/span/a/text()')[0] )
					# exit(0)
				else:
					dirList.append(row.xpath('td[@class="content"]/span/a/@title')[0])
				#print(dirList)
			else:
				#print(row.xpath('td[@class="content"]/span/a/@title')[0])
				fileList.append(row.xpath('td[@class="content"]/span/a/@title')[0])
				#print(fileList)
		#print(dirList)
		#print(fileList)
		if len(fileList) == 0:
			f = open('%s.html'%url.split('/')[-1], 'w')
			f.write(html)
			f.close()
		#print("return dirList, fileList")
		return dirList, fileList
	except Exception, e:
		print("Exception has happened: "+e.message)
		# exit(0)

def downloadFile(dirPath, fileList, url):
	#print(sys._getframe().f_code.co_name)
	origin_work_dir = os.getcwd()
	os.chdir(dirPath)
	prefix = 'https://raw.githubusercontent.com'
	for fileName in fileList:
		downloadUrl = prefix + url.split('//')[1].replace('tree/', '').replace('github.com','')+'/'+fileName
		#print(downloadUrl)
		#os.system('wget %s' % downloadUrl)
		print("Downlading %s" % dirPath+'/'+fileName)
		commands.getstatusoutput('wget %s' % downloadUrl)
		#os.popen('wget %s' % downloadUrl)
		# os.system('touch %s' % fileName)
	os.chdir(origin_work_dir)

def createDir(dirPath, dirList):
	#print(sys._getframe().f_code.co_name)
	origin_work_dir = os.getcwd()
	os.chdir(dirPath)
	for dirItem in dirList:
		#print(dirItem)
		os.makedirs(dirItem)
	os.chdir(origin_work_dir)

def recursive(curDir, url):	
	# print('---------------------------------------')
	# print("url: ", url)
	# print("curDir: ", curDir)
	subDirList, fileList = getDirAndFileList(url)
	if len(fileList) != 0:
		downloadFile(curDir, fileList, url)
	# print("subDirList: ", subDirList)
	# print("fileList: ", fileList)
	if len(subDirList) != 0:
		createDir(curDir, subDirList)
		for dirItem in subDirList:
			# print("curDir: ", curDir+'/'+dirItem)
			recursive(curDir+'/'+dirItem, url+'/'+dirItem)


def getSubDir(url):
	#url = "https://github.com/ApolloAuto/apollo/tree/master/modules/drivers/velodyne"
	curDir = url.split('/')[-1]
	if os.path.exists(curDir):
		print("%s exists, please change to another directory." % curDir)
		exit(0)
	else:
		os.mkdir(curDir, 0755)
		# subDirList = fileList = []
		# subDirList, fileList = getDirAndFileList(url)
		subDirList = []
		rootDir = os.getcwd() + "/" + curDir
		recursive(curDir, url)
		# print(os.getcwd())
		# downloadFile(rootDir, fileList, url)
		# print(os.getcwd())
		# createDir(rootDir, subDirList)
		# print(os.getcwd())
		
		# curDirList = subDirList
		# for dirItem in curDirList