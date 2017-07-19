#!/usr/bin/python3
#-*-encoding:utf-8-*-
import os,sys
def killProcess(processList):
    for processName in processList:
        processLine = os.popen("ps aux | grep %s" % processName)
        line = processLine.readline()
        arr = line.split()
        col = 0
        for i in range(len(arr)):
            if processName in arr[i]:
                col = i
                break
        #if the script doesn't find the process, then quit
        if not col:
            exit()
        while line != '':
            split1 = line.split()
            if processName in split1[col] :
                ret = os.system("kill -9 %s" % split1[1])
                # print (ret)
                if not ret:
                    if ':' in split1[col]:
                        print ("killed %s,Process name:%s" % (split1[1], split1[col][:-1]) )
                    if '/' in split1[col]:
                        print ("killed %s,Process name:%s" % (split1[1], split1[col] ))                                
            line = processLine.readline()
            if 'grep' in line:
                break

if __name__ == "__main__":
    killProcess(['nginx', 'php-fpm', 'httpd'])
