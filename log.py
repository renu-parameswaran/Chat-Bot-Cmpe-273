import shutil
import os
import config

fileName = "file1.txt"

def truncateFile():
    with open(fileName, 'w'): pass

def writetofile(content):

   with open(fileName, "a") as text_file:
        text_file.write("\n" + content)


def writetologfile(fileLog):
    fullLogPath = config.logpath + fileLog
    if not os.path.exists(os.path.dirname(fullLogPath)):
        os.makedirs(os.path.dirname(fullLogPath))
    with open(fileName,"r") as f:
        with open(fullLogPath, "w") as f1:
            #print fullLogPath
            shutil.copy2(fileName,fullLogPath)

