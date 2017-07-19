#!/usr/bin/python3
#-*-encoding:utf-8-*-
#usage: ./scriptprogram processname
import os,sys
processLine = os.popen("ps aux | grep %s" % sys.argv[1])
line = processLine.readline()
arr = line.split()
col = 0
for i in range(len(arr)):
    if sys.argv[1] in arr[i]:
        col = i
        break
#if the script doesn't find the process, then quit
if not col:
    exit()
while line != '':
    split1 = line.split()
    if sys.argv[1] in split1[col] :
        ret = os.system("kill -9 %s" % split1[1])
        # print (ret)
        if not ret:
            print ("killed %s,Process name:%s" % (split1[1], split1[col][:-1]) )
    line = processLine.readline()
    if 'grep' in line:
        break
