import pymysql
import log
import config

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
        dblist.append({"id":"%d" %id,"answer":"%s" % ans,"keyword":"%s" % keyw,"question":"%s" % ques,"numberOfMatchingKeywords":0})
    log.writetofile(str(dblist))
        