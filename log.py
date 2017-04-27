fileName = "file1.txt"

def truncateFile():
    with open(fileName, 'w'): pass

def writetofile(content):

   with open(fileName, "a") as text_file:
        text_file.write("\n" + content)

