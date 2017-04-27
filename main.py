import sara
import database
import log

if __name__ == "__main__":
    log.truncateFile()
    log.writetofile("*****Starting the log file*****")
    conn = database.connectToDB()
    if(conn!="error"):
        database.doQuery(conn)
        database.closeDbConnection(conn)
    sara.slackListeToChannel()