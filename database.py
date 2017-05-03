import pymysql
import log
import config
import time
from datetime import datetime

# def doQuery(conn) :
#     log.writetofile("Sending query to DB")
#     cur = conn.cursor()
#     cur.execute("SELECT question, answer FROM botreplies")

#     for question, answer in cur.fetchall():
#         log.writetofile("query response: " + question +"->"+ answer)

def connectToDB():
    log.writetofile("entering connectToDB function")
    try:
        myConnection = pymysql.connect(host=config.dbHost, user=config.dbUser, passwd=config.dbPassword, db=config.dbName)
        log.writetofile("DB connection succesfull")
    except Exception, ex:
        myConnection = "error"
        log.writetofile("Error : %s" % ex)

    return myConnection

def closeDbConnection(conn):
    log.writetofile("closing the db connection")
    conn.close()

#To get responses from Database based on question 
def getAllResponses(conn):
    log.writetofile("Sending query to DB")
    cur = conn.cursor()
    sql = "SELECT * FROM responses"
    cur.execute(sql)
    result = cur.fetchall()
    dblist = []
    for row in result:
        id, ans, keyw, ques,img_url = row
        numberOfDbKeywords = len(keyw.split(','))
        dblist.append({"id":"%d" %id,"question":"%s" % ques.lower(),"answer":"%s" % ans.lower(),"numberOfDbKeywords":"%d" %numberOfDbKeywords,"DbKeywords":"%s" % keyw.lower(),"numberOfUserInputKeywords":0,"numberOfMatchingKeywords":0,"matchingKeyWords": "","nonMatchingKeyWords": "","image_url":img_url,"nonMatchingKeywordsInDB":""})
    #log.writetofile(str(dblist))
    return dblist

def storeSentResponse(userInput,answer,keywords,questions,conn):
    log.writetofile("storing sent response to DB..")
    now = datetime.now()
    now.strftime('%m/%d/%Y')

    cur = conn.cursor()
    insertstmt = "insert into sentresponses (UserQuestion,Answer,MatchingKeywords,QuestionPart,CurrentScore,Timestamp) values ('%s', '%s', '%s ', '%s', '%d', '%s')" % (userInput,answer,','.join(keywords),questions,1,now)
    cur.execute(insertstmt)
    log.writetofile("Insert to db successfully done")
    conn.commit()

def getAllPastResponses(questions,keywords,conn):
    log.writetofile("sending query to sentresponses db")
    cur = conn.cursor()
    sql = "SELECT * FROM sentresponses WHERE QuestionPart = '%s' and MatchingKeywords = '%s'" %(questions,','.join(keywords))
    cur.execute(sql)
    result = cur.fetchall()
    dblist = []
    for row in result:
     id,quest,ans,matchkeyw,QP,CS,TS = row
     dblist.append({"id": "%d" % id, "user question": "%s" % quest, "Answer": "%s" % ans, "Matching Keywords": "%s" % matchkeyw,"Question Part": "%s" % QP, "Current Score": "%s" % CS, "Time Stamp": "%s" % TS})
    log.writetofile(str(dblist))
    return dblist

def updatePastResponse(id, feedback,conn):
  cur = conn.cursor()
  feedback = feedback.lower()
  if(feedback == 'y' or feedback == 'yes'):
    sql = "update sentresponses set CurrentScore = CurrentScore + 1 where ID = '%d'" % id
    cur.execute(sql)
    log.writetofile("CurrentScore incremented in db")
    conn.commit()

  elif(feedback == 'n' or feedback == 'no'):
    sql = "update sentresponses set CurrentScore = CurrentScore - 1 where ID = '%d'" % id
    cur.execute(sql)
    log.writetofile("CurrentScore decremented in db")
    conn.commit()

def storeNewResponse(ans,matchedKeywordList,ques,conn):
   if not matchedKeywordList:
     print "List is empty or null"
   else:
     matchedKeywordsListToCsv = ','.join(map(str,matchedKeywordList))
     cur = conn.cursor()
     insertStmt = "insert into responses (Answer,Keywords,Question) values ('%s','%s','%s')" % (ans,matchedKeywordsListToCsv,ques)
     cur.execute(insertStmt)
     log.writetofile("New Responses inserted to db")
     conn.commit()
    
def checkIDExists(id,conn):
  cur = conn.cursor()
  sql = "select ID from sentresponses where ID = '%d'" % id
  rows_count = cur.execute(sql)
  if rows_count > 0:
      log.writetofile("ID exists in DB")
      return True
  else:
      log.writetofile("ID does not exist in DB")
      return False

def checkRowExists(ques,ans,keywordList,conn):
  cur = conn.cursor()
  if not keywordList:
      print "keyword list is empty or null"
  else:
     keywordListToCsv = ','.join(map(str, keywordList))
  sql = "select * from responses where Answer = '%s' and Keywords = '%s'" % (ans,keywordListToCsv)

  #to:do get all keywords and compare

  rows_count = cur.execute(sql)
  if rows_count > 0:
     log.writetofile("Row exists in response table")
     return True
  else:
      log.writetofile("Row does not exist in response table")
      return False

def getPastResponse(id,conn):
  cur = conn.cursor()
  dblist = []
  sql = "select * from sentresponses where ID = '%d'" % id
  cur.execute(sql)
  result = cur.fetchall()
  for row in result:
     dblist.append({"ID": "%d" % row[0], "UserQuestion": "%s" % row[1], "Answer": "%s" % row[2], "MatchingKeywords": "%s" % row[3],
                 "QuestionPart": "%s" % row[4], "CurrentScore": "%d" % row[5], "Timestamp": "%s" % row[6]})
     log.writetofile(str(dblist))
     return dblist
 
def getPastResponseFromUserInput(userInp,conn):

    cur = conn.cursor()
    sql = "select UserQuestion from sentresponses where UserQuestion = '%s'" % userInp
    dblist = []
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        dblist.append({"ID": "%d" % row[0], "UserQuestion": "%s" % row[1], "Answer": "%s" % row[2],
                       "MatchingKeywords": "%s" % row[3],
                       "QuestionPart": "%s" % row[4], "CurrentScore": "%d" % row[5], "Timestamp": "%s" % row[6]})
        log.writetofile(str(dblist))
        return dblist
