import pymysql
import log
import config

def doQuery(conn) :
    log.writetofile("Sending query to DB")
    cur = conn.cursor()
    cur.execute("SELECT question, answer FROM botreplies")

    for question, answer in cur.fetchall():
        log.writetofile("query response: " + question +"->"+ answer)

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
