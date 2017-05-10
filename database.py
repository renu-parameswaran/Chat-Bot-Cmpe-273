import pymysql
import log
import config
import time
import lang_processor
from datetime import datetime
from elasticsearch import Elasticsearch


# def doQuery(conn) :
#     log.writetofile("Sending query to DB")
#     cur = conn.cursor()
#     cur.execute("SELECT question, answer FROM botreplies")

#     for question, answer in cur.fetchall():
#         log.writetofile("query response: " + question +"->"+ answer)

def connectToDB():
    log.writetofile("entering connectToDB function")
    try:
        myConnection = pymysql.connect(host=config.dbHost, user=config.dbUser, passwd=config.dbPassword,
                                       db=config.dbName)
        log.writetofile("DB connection succesfull")
    except Exception, ex:
        myConnection = "error"
        log.writetofile("Error : %s" % ex)

    return myConnection


def closeDbConnection(conn):
    log.writetofile("closing the db connection")
    conn.close()


# To get responses from Database based on question
def getAllResponses(conn):
    log.writetofile("Sending query to DB")
    cur = conn.cursor()
    sql = "SELECT * FROM responses"
    cur.execute(sql)
    result = cur.fetchall()
    dblist = []
    for row in result:
        id, ans, keyw, ques, img_url = row
        numberOfDbKeywords = len(keyw.split(','))
        dblist.append({"id": "%d" % id, "question": "%s" % ques.lower(), "answer": "%s" % ans.lower(),
                       "numberOfDbKeywords": "%d" % numberOfDbKeywords, "DbKeywords": "%s" % keyw.lower(),
                       "numberOfUserInputKeywords": 0, "numberOfMatchingKeywords": 0, "matchingKeyWords": "",
                       "nonMatchingKeyWords": "", "image_url": img_url, "nonMatchingKeywordsInDB": ""})
    # log.writetofile(str(dblist))
    return dblist


def getAllResponsesExceptAnswerWithNegativeScore(conn, previousAnswer):
    log.writetofile("Getting responses without answer with negative score")
    cur = conn.cursor()
    sql = "SELECT * FROM responses where Answer!='%s'" % previousAnswer
    cur.execute(sql)
    result = cur.fetchall()
    dblist = []
    for row in result:
        id, ans, keyw, ques, img_url = row
        numberOfDbKeywords = len(keyw.split(','))
        dblist.append({"id": "%d" % id, "question": "%s" % ques.lower(), "answer": "%s" % ans.lower(),
                       "numberOfDbKeywords": "%d" % numberOfDbKeywords, "DbKeywords": "%s" % keyw.lower(),
                       "numberOfUserInputKeywords": 0, "numberOfMatchingKeywords": 0, "matchingKeyWords": "",
                       "nonMatchingKeyWords": "", "image_url": img_url, "nonMatchingKeywordsInDB": ""})
    # log.writetofile(str(dblist))
    return dblist


def storeSentResponse(userInput, answer, keywords, questions, conn, img_url):
    log.writetofile("storing sent response to DB..")
    now = datetime.now()
    now.strftime('%m/%d/%Y')

    cur = conn.cursor()
    insertstmt = "insert into sentresponses (UserQuestion,Answer,MatchingKeywords,QuestionPart,CurrentScore,Timestamp,image_url) values ('%s', '%s', '%s ', '%s', '%d', '%s', '%s')" % (
    userInput, answer, ','.join(keywords), questions, 1, now, img_url)
    cur.execute(insertstmt)
    timestamp = datetime.now()
    es = Elasticsearch()
    es.index(index="sararesponses", doc_type="metrics", id=timestamp,
             body={"question": userInput, "answer": answer, "timestamp": timestamp})
    log.writetofile("Insert to db successfully done")
    sentResponseID = conn.insert_id()

    conn.commit()
    return sentResponseID


def getAllPastResponses(questions, keywords, conn):
    log.writetofile("sending query to sentresponses db")
    cur = conn.cursor()
    sql = "SELECT * FROM sentresponses WHERE QuestionPart = '%s' and MatchingKeywords = '%s'" % (
    questions, ','.join(keywords))
    cur.execute(sql)
    result = cur.fetchall()
    dblist = []
    for row in result:
        id, quest, ans, matchkeyw, QP, CS, TS, img_url = row
        dblist.append({"id": "%d" % id, "user question": "%s" % quest, "Answer": "%s" % ans,
                       "Matching Keywords": "%s" % matchkeyw, "Question Part": "%s" % QP, "Current Score": "%s" % CS,
                       "Time Stamp": "%s" % TS, "Image_Url": "%s" % img_url})
    log.writetofile(str(dblist))
    return dblist


def updatePastResponse(id, feedback, conn):
    cur = conn.cursor()
    feedback = feedback.lower()
    now = datetime.now()
    now.strftime('%m/%d/%Y')
    if (feedback == 'y' or feedback == 'yes'):
        print id
        sql = "update sentresponses set CurrentScore = CurrentScore + 1, Timestamp = '%s' where ID = '%d'" % (now, id)
        cur.execute(sql)
        log.writetofile("CurrentScore incremented in db")
        conn.commit()
        isPositive = 1
        isNegative = 0

    elif (feedback == 'n' or feedback == 'no'):
        sql = "update sentresponses set CurrentScore = CurrentScore - 1, Timestamp = '%s' where ID = '%d'" % (now, id)
        cur.execute(sql)
        log.writetofile("CurrentScore decremented in db")
        conn.commit()
        isPositive = 0
        isNegative = 1

    es = Elasticsearch()
    es.index(index="feedback", doc_type="metrics", id=now,
             body={"isPositive": isPositive, "isNegative": isNegative, "timestamp": now})


def storeNewResponse(ans, matchedKeywordList, ques, conn):
    if not matchedKeywordList:
        print "List is empty or null"
    else:
        # matchedKeywordsListToCsv = ','.join(map(str,matchedKeywordList))
        cur = conn.cursor()
        # decodedKeyword = (unicode.encode(matchedKeywordList))
        # decodedQuestion = ((unicode.encode(ques)))
        matchedKeywordList=lang_processor.removeSpaceKeyword(matchedKeywordList)
        insertStmt = "insert into responses (Answer,Keywords,Question,image_url) values ('%s','%s','%s','none')" % (
        ans, matchedKeywordList, ques)

        print insertStmt
        cur.execute(insertStmt)
        log.writetofile("New Responses inserted to db")
        conn.commit()


def checkIDExists(id, conn):
    cur = conn.cursor()
    sql = "select ID from sentresponses where ID = '%d'" % id
    rows_count = cur.execute(sql)
    if rows_count > 0:
        log.writetofile("ID exists in DB")
        return True
    else:
        log.writetofile("ID does not exist in DB")
        return False


def checkRowExists(ques, ans, keywordList, conn):
    cur = conn.cursor()
    log.writetofile("..user input keywords" + " " + str(keywordList))

    UserkeywordList = str(keywordList)

    if not keywordList:
        print "keyword list is empty or null"
        return False
    else:

        sql = "select Keywords from responses where Question = '%s' and Answer = '%s'" % (ques, ans)
        rows_count = cur.execute(sql)
        result = cur.fetchall()
        for i in result:
            resultrow = i[0]

        if rows_count > 0:
            if (set(resultrow) == set(UserkeywordList)):
                log.writetofile("Row exists in response table")
                return True
            else:
                return False


        else:
            log.writetofile("Row does not exist in response table")
            log.writetofile("not exists")
            return False


def getPastResponse(id, conn):
    cur = conn.cursor()
    dblist = []
    sql = "select * from sentresponses where ID = '%d'" % id
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        dblist.append({"ID": "%d" % row[0], "UserQuestion": "%s" % row[1], "Answer": "%s" % row[2],
                       "MatchingKeywords": "%s" % row[3],
                       "QuestionPart": "%s" % row[4], "CurrentScore": "%d" % row[5], "Timestamp": "%s" % row[6],
                       "Image_Url": "%s" % row[7]})
        log.writetofile(str(dblist))
        return dblist


def getPastResponseFromUserInput(userInp, conn):
    cur = conn.cursor()
    sql = "select * from sentresponses where UserQuestion = '%s'" % userInp
    dblist = []
    cur.execute(sql)
    result = cur.fetchall()
    rowExists = False
    for row in result:
        dblist.append({"ID": "%d" % row[0], "UserQuestion": "%s" % row[1], "Answer": "%s" % row[2],
                       "MatchingKeywords": "%s" % row[3],
                       "QuestionPart": "%s" % row[4], "CurrentScore": "%d" % row[5], "Timestamp": "%s" % row[6],
                       "Image_Url": "%s" % row[7]})

        rowExists = True
        log.writetofile(str(dblist))
    return dblist, rowExists


def isCorrectAnswer(keywords, conn):
    log.writetofile("sending query to responses db")
    cur = conn.cursor()
    userkeylist = []
    for i in keywords:
        userkeylist.append(i)
    log.writetofile(str(userkeylist))
    sql = "select Keywords from responses"
    cur.execute(sql)
    result = cur.fetchall()
    resultrow = []
    for i in result:
        resultrow.append(i[0])
    resultlist = ','.join(resultrow)
    a = resultlist.split(",")
    newwordslist = [x for x in userkeylist if x not in a]

    answer = newwordslist[0:]

    userinputlist = [x for x in userkeylist if x not in newwordslist]
    for i in userinputlist:
        listuser = ','.join(userinputlist)

    sql = "select Keywords from responses where Answer = '%s'" % (' '.join(answer))
    rows_count = cur.execute(sql)
    log.writetofile(sql)

    if rows_count > 0:
        result = cur.fetchall()
        dblist = result[0]
        log.writetofile(str(dblist))

        if (set(listuser) == set(dblist[0])):
            log.writetofile("Row exists in response table")
            return True
        else:
            log.writetofile("no matching found")
            return False

    else:
        return False


def storeMetricInES(userInput, response):
    es = Elasticsearch()
    timestamp = datetime.now()
    es.index(index="cache", doc_type="metrics", id=timestamp,
             body={"question": userInput, "answer": response, "timestamp": timestamp})
