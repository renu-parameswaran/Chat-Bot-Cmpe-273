import sara
import database
import log

if __name__ == "__main__":
    log.truncateFile()
    log.writetofile("*****Starting the log file*****")
    
    sara.slackListeToChannel()