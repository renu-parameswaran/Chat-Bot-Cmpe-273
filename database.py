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
def getAllResponses(questions,conn):
    log.writetofile("Sending query to DB")
    cur = conn.cursor()
    sql = "SELECT * FROM responses WHERE Question = '%s'" % questions
    cur.execute(sql)
    result = cur.fetchall()
    dblist = []
    for row in result:
        id, ans, keyw, ques = row
        dblist.append({"id":"%d" %id,"answer":"%s" % ans,"keywords":"%s" % keyw,"question":"%s" % ques,"numberOfMatchingKeywords":0,"matchingKeyWords": ""})
    log.writetofile(str(dblist))
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
