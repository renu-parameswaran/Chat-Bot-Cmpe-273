import lang_processor
import database
import log
import config
import operator
import time
import sendemail
import weather
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import random
import sara
#from selenium import webdriver


currentMode = "default"
userInputQuestions = []
userInputKeywords = []
responseID = 0
conn = database.connectToDB()


# Function to get keywords and Questions separately from user input
def userInputQuestionKeyword(userInput):
    userInputArray = lang_processor.split_message(userInput)
    userInputWithOnlyQuestionAndKeywords = lang_processor.removeUnwantedWords(userInputArray)
    questions, keywords = lang_processor.seperateQuestionAndKeywords(userInputWithOnlyQuestionAndKeywords)
    return questions, keywords


def getReply(userInput):
    global conn
    userInputArray = lang_processor.split_message(userInput)
    questions, keywords = userInputQuestionKeyword(userInput)

    response, image_url = handle_request(questions, keywords, userInput, userInputArray, conn)
    if not questions:
        questionPart = "none"
    else:
        questionPart = questions[0]

    return response, image_url, questionPart


def handle_request(questions, keywords, userInput, userInputArray, conn):
    count = len(questions)
    image_url = "none"
    if (count == 0):
        response = common_replies(userInputArray, conn)
    else:

        if (conn != "error"):
            response, image_url = pickBestResponse(keywords, userInput, userInputArray, questions[0], conn)
            #response = lang_processor.generateResponse(userInputArray, questions[0], response)

        else:
            response = config.dbConnectionError

    return response, image_url


def pickBestResponse(keywords, userInput, userInputArray, questionPartInUserInput, conn):
    image_url = "none"
    pastResponses, isPastResponseExists = database.getPastResponseFromUserInput(userInput, conn)

    if isPastResponseExists:
        pastResponses.sort(key=operator.itemgetter('CurrentScore'), reverse=True)
        pastResponse = pastResponses[0]
        if int(pastResponse['CurrentScore']) > 0:
            log.writetofile("I am giving a reply from my past experiences")
            response = pastResponse['Answer'] + config.giveFeedback + str(pastResponse['ID'])
            image_url = pastResponse['Image_Url']
            database.storeMetricInES(userInput,response)
        else:
            log.writetofile(
                "Score for my past experiences does not look good. I am gonna look for new responses in the DB")
            response, image_url = getBestResponseFromDB(keywords, userInput, userInputArray, questionPartInUserInput,
                                                        conn, True, pastResponse['Answer'])
    else:
        log.writetofile("Getting new response from DB")
        response, image_url = getBestResponseFromDB(keywords, userInput, userInputArray, questionPartInUserInput, conn,
                                                    False, "none")

    return response, image_url


def getBestResponseFromDB(keywords, userInput, userInputArray, questionPartInUserInput, conn, isNegativeScore,
                          previousAnswer):
    image_url = "none"
    if isNegativeScore:
        DBResponses = database.getAllResponsesExceptAnswerWithNegativeScore(conn, previousAnswer)
    else:
        DBResponses = database.getAllResponses(conn)
    DBResponses = getMatchingKeywords(DBResponses, keywords)
    DBResponses.sort(key=operator.itemgetter('numberOfMatchingKeywords'), reverse=True)
    #log.writetofile("sorted:" + str(DBResponses))

    for dbResponse in DBResponses:
        # 100% match for the keywords in user input with db keywords. Return this response
        # to do: two questions with 100% match?? match question!!
        if dbResponse['nonMatchingKeyWords'] == "" and dbResponse['nonMatchingKeywordsInDB'] == "":
            log.writetofile("100% match found")
            image_url = dbResponse["image_url"]
            sentResponseID = database.storeSentResponse(userInput, dbResponse['answer'], keywords, questionPartInUserInput, conn,
                                       image_url)
            print sentResponseID
            response = dbResponse['answer'] + config.giveFeedback + str(sentResponseID)
            return response , image_url
        # not 100%.
        # perform spell check and find similar words
        else:
                nonMatchingKeywords = dbResponse['nonMatchingKeyWords'].split(',')
                nonMatchingKeywordsinDB = dbResponse['nonMatchingKeywordsInDB'].split(',')

                for nonMatchingKeyword in nonMatchingKeywords:
                    correctedKeyword = lang_processor.autocorrect(nonMatchingKeyword)
                    synonyms = lang_processor.getSynonyms(correctedKeyword)
                    # log.writetofile("synonyms for user input " + correctedKeyword + ":" + str(synonyms))

                    for nonMatchingKeyword in nonMatchingKeywordsinDB:
                        DBsynonyms = lang_processor.getSynonyms(nonMatchingKeyword)
                        # log.writetofile("synonyms for DB " + nonMatchingKeyword + ":" + str(DBsynonyms))

                        if (set(DBsynonyms) == set(synonyms)):
                            log.writetofile("matching synonym found.")
                            dbResponse["numberOfMatchingKeywords"] = dbResponse["numberOfMatchingKeywords"] + 1;

    DBResponses.sort(key=operator.itemgetter('numberOfMatchingKeywords'), reverse=True)
    log.writetofile("after synonyms : " + str(DBResponses))

    isAmbiguousReply = False
    responseNumber = 1
    for dbResponse in DBResponses:

        if responseNumber == 1:
            firstResponseMatchingCount = dbResponse["numberOfMatchingKeywords"]
            response = dbResponse["answer"]
            responseNumber = responseNumber + 1
            questionPart = dbResponse["question"]
            image_url = dbResponse["image_url"]
        else:
            if (firstResponseMatchingCount != 0):
                if firstResponseMatchingCount == dbResponse["numberOfMatchingKeywords"]:
                    if questionPart == questionPartInUserInput:
                        log.writetofile("2 responses.picking bases on question")
                    elif questionPartInUserInput == dbResponse["question"]:
                        response = dbResponse["answer"]
                        image_url = dbResponse["image_url"]
                        log.writetofile("2 responses.picking 2nd based on question")
                    else:
                        log.writetofile("2 responses.ambiguos")
                        isAmbiguousReply = True
                        image_url = dbResponse["image_url"]
                        response = config.ambiguousInput
            else:
                log.writetofile("0 matching keywords")
                isAmbiguousReply = True
                image_url = dbResponse["image_url"]
                response = config.ambiguousInput

            if (isAmbiguousReply):
                log.writetofile("not storing in sent responses")
            else:
                sentResponseID = database.storeSentResponse(userInput, response, keywords, questionPartInUserInput, conn, image_url)
                log.writetofile("storing sent response")
                print sentResponseID
                response = response + config.giveFeedback + str(sentResponseID)

            return response, image_url

    # pastResponses = database.getPastResponseFromUserInput(userInput,conn)
    return config.noAppropriateResponseFound


def check_for_greeting(input1):
    GREETING_RESPONSES = ["Hi!,what's up with you?", "'sup bro :wink:", "hey :smiley:", "hi..Welcome :smiley:",
                          "How can i help you?", "Sure, What help do u need?",
                          "I'm bored! Give me good questions! :sob:"]
    response = random.choice(GREETING_RESPONSES)
    return response


def check_for_complaints(input2):
    SORRY_RESPONSES = ["sorry :neutral_face:", "I will try to improve my answers :ok_hand:", "i'm really sorry :sob:",
                       "I apologize for being late to reply :pray:"]
    response = random.choice(SORRY_RESPONSES)
    return response


def common_replies(user_input_array,conn):
    question1 = user_input_array[0]

    train = [
        ('hi', 'pos'),
        ('hello', 'pos'),
        ('please improve your answers', 'pos'),
        ('can you give me this?', 'pos'),
        ('i love your answers.', 'pos'),
        ('this is an amazing answer!', 'pos'),
        ('a very Good Morning', 'pos'),
        ('this is your best work.', 'pos'),
        ("this is an awesome answer", 'pos'),
        ('i do not like this', 'neg'),
        ('sorry', 'neg'),
        ('i am tired of this stuff.', 'neg'),
        ("i can't deal with this", 'neg'),
        ('you have to improve', 'neg'),
        ('you are taking so much time to learn.', 'neg')
    ]
    cl = NaiveBayesClassifier(train)

    for i in user_input_array:
        ques = ' '.join(user_input_array)
    blob = TextBlob(ques, classifier=cl)
    sentiment = blob.classify()
    print (sentiment)
    log.writetofile("entering positive or negative checking")
    common_questions = ['request appointment', 'text books references download', 'sjsu main campus map',
                        'share cmpe273 greensheet', 'slack manual assistance error problem', 'help', 'improve',
                        'great day', 'bye tata cya see you later', 'thank you thanks', 'thanks Sara',
                        'please improve your answers', 'are you feeling good today?', 'amazing answers', 'bye']
    for i in common_questions:
        if (sentiment == 'pos' and question1 != "is" and question1 != "does" and (ques not in ' '.join(common_questions))):
            response = check_for_greeting(ques)

        elif (sentiment == 'neg' and question1 != "is" and question1 != "does" and (ques not in ' '.join(common_questions))):
            response = check_for_complaints(ques)

        elif (question1 == "is" or question1 == "does"):
            keywords = lang_processor.removeUnwantedWords(user_input_array)
            resp = database.isCorrectAnswer(keywords, conn)
            if (resp == True):
                response = "yes"
            else:
                response = "no"
        elif (ques in "request appointment"):
            response = sendemail.SendEmail()

        elif (ques in "share cmpe273 greensheet"):
            attachments = [
                {
                    "fallback": "Greensheet Cmpe 273 spring 2017 semester - https://www.dropbox.com/sh/qrzvf659cw2k4uv/AACrelHpOwJTX88TDN-PQ8o9a?dl=0&preview=cmpe273-greensheet.docx",
                    "pretext": "Cmpe 273 Greensheet",
                    "title": "Cmpe 273 Spring 2017 Semester Greensheet",
                    "title_link": "https://www.dropbox.com/sh/qrzvf659cw2k4uv/AACrelHpOwJTX88TDN-PQ8o9a?dl=0&preview=cmpe273-greensheet.docx",
                    "color": "#36a64f",
                }
            ]

            response = "click on this link for greensheet"
            sara.send_image(config.channel, attachments)

        elif (ques in "thank you thanks"):
            response = "You are welcome! :thumbsup:"

        elif (ques in "sjsu main campus map"):
            attachments = [
                {

                    "title": "Sjsu Main Campus",
                    "title_link": "http://www.sjsu.edu/map/docs/campus-map.pdf",
                    "color": "#36a64f"
                }
            ]
            response = "Check out this link for main campus map!"
            sara.send_image(config.channel, attachments)


        elif (ques in "more clear"):
            response = "sure :ok_hand:"

        elif (ques in "text books references download"):
            response = "Check these links to download text books! :thumbsup:"

            attachments = [
                {
                    "text": "Text Books/Readings -",
                    "fallback": "text book 1 - https://books.google.com/books?id=CclkovBDqJkC&printsec=frontcover&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false",
                    "fields": [
                        {

                            "title": "Web Services, by Gustavo Alonso, Fabio Casati, Harumi Kuno and Vijay Machiraju (2003) ",
                            "value": "<https://books.google.com/books?id=CclkovBDqJkC&printsec=frontcover&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false|Download here>",
                            "short": True
                        },
                        {
                            "title": "Enterprise Integration Patterns, by Gregor Hohpe and Bobby Woolf (2003)",
                            "value": "<http://ptgmedia.pearsoncmg.com/images/9780321200686/samplepages/0321200683.pdf|Download here>",
                            "short": True
                        },
                        {
                            "title": "Restful Web Services, by Leonard Richardson, Sam Ruby and David Hansson (2007)",
                            "value": "<https://www.crummy.com/writing/RESTful-Web-Services/RESTful_Web_Services.pdf|Download here>",
                            "short": True
                        }
                    ],
                    "color": "#F35A00"
                }
            ]

            sara.send_image(config.channel, attachments)


        elif (ques in "great day"):
            response = "Yes,Thanks. Wish you a Wonderful Day. :ok_hand:"

        elif (ques in "please improve your answers"):
            response = "Yes..sure, I will definitely improve them. :ok_hand:"

        elif (ques in "are you feeling good today?"):
            response = "Hi! I'm good..How are you feeling this week?"

        elif (ques in "amazing answers"):
            response = "Thanks! I know im so good at it!. :heart_eyes:"

        elif (ques in "bye tata cya see you later"):
            response = "Bye! Adios! Have a good day! :wave: "

        elif (ques in "help :rolling_eyes:"):
            response = "Sure! What help do u need? "

        elif (ques in "slack manual assistance error problem"):
            attachments = [
                {
                    "fallback": "help with slack - https://get.slack.help/hc/en-us",
                    "pretext": "Slack help center",
                    "title": "Hi, How can we help?",
                    "title_link": "https://get.slack.help/hc/en-us",
                    "color": "#36a64f"
                }
            ]
            response = "Check out this link for help center!"
            sara.send_image(config.channel, attachments)


        elif (ques in "improve"):
            response = "Yes..sure, I will definitely improve them.:thumbsup: "

        else:
            response = "I'm sorry, I don't understand! Sometimes I have an easier time with a few simple keywords.\n "

        return response

# Function to get matching Keywords
def getMatchingKeywords(allResponses, keywords):
    currentKeywordList = []

    for response in allResponses:
        length = len(response['DbKeywords'].split(','))

        for i in range(0, length):
            currentKeywordList.append(response['DbKeywords'].split(',')[i])

        matchKeywordList = []
        notMatchingKeywordList = []
        notMatchingKeywordListinDB = []

        for val1 in currentKeywordList:
            for val2 in keywords:
                if (val2.lower() == val1.lower()):
                    matchKeywordList.append(val2.lower())

        for val1 in keywords:
            if val1 not in matchKeywordList:
                notMatchingKeywordList.append(val1.lower())

        for val1 in currentKeywordList:
            if val1 not in matchKeywordList:
                notMatchingKeywordListinDB.append(val1.lower())
                response['nonMatchingKeywordsInDB'] = ','.join(notMatchingKeywordListinDB)

        response['numberOfUserInputKeywords'] = len(keywords)
        response['numberOfMatchingKeywords'] = len(matchKeywordList)

        if response['numberOfUserInputKeywords'] != response['numberOfMatchingKeywords']:
            response['nonMatchingKeyWords'] = unicode.encode(','.join(notMatchingKeywordList))

        lengthMKL = len(matchKeywordList)
        stra = ""
        for i in range(0, lengthMKL):
            stra = stra + matchKeywordList[i] + ","

        response['matchingKeyWords'] = stra
        try:
            response['matchingKeyWords'] = (unicode.encode(response['matchingKeyWords'])).rstrip(',')
        except:
            response['matchingKeyWords'] = ""

        del matchKeywordList[:]
        del currentKeywordList[:]
        del notMatchingKeywordList[:]

    log.writetofile("Adding matching keyword")
    log.writetofile(str(allResponses))
    return allResponses


# Function to get the Current Mode
def currentWorkingMode(userInput):
    image_url = "none"
    questionPart = "none"
    global currentMode
    if (currentMode == "default"):
        if (userInput == "1"):
            currentMode = "chat"
            response = config.chatResponse
            log.writetofile(response)
        elif (userInput == "2"):
            currentMode = "training"
            response = config.trainingResponse1
            log.writetofile(response)
        elif (userInput == "3"):
            currentMode = "feedback"
            response = config.feedbackResponse1
            log.writetofile(response)
        elif (userInput == "4"):
            currentMode = "statistics"
            response = config.statisticsResponse
            log.writetofile(response)
        elif (userInput == "5"):
            currentMode = "weather"
            response = config.weatherResponse
            log.writetofile(response)
        elif (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            response = "Invalid Input. Please input the number to choose your mode"
            log.writetofile(response)
    elif (currentMode == "chat"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            response, image_url, questionPart = getReply(userInput)
            log.writetofile("Calling function botController getReply")

    elif (currentMode == "training"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            global userInputQuestions, userInputKeywords
            userInputQuestions, userInputKeywords = userInputQuestionKeyword(userInput)
            # print type(userInputQuestions)
            # print userInputQuestions
            if (len(userInputQuestions)):
                currentMode = "training2"
                response = config.trainingResponse2
    elif (currentMode == "training2"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            global userInputQuestions, userInputKeywords
            unicodeKeywords = []
            conn = database.connectToDB()
            unicodeKeywords = ','.join(userInputKeywords)
            if (database.checkRowExists(userInputQuestions[0], userInput, unicodeKeywords, conn)):
                log.writetofile("row already exist so not inserting")
                response = "Thanks for the information. " + config.moreTraining
                currentMode = "moretraining"
            else:
                database.storeNewResponse(userInput, unicodeKeywords, userInputQuestions[0], conn)
                currentMode = "moretraining"
                response = "Thanks for the information. " + config.moreTraining
    elif (currentMode == "moretraining"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        if (userInput.lower() == "yes".lower() or userInput.lower() == "y"):
            currentMode = "training"
            response = config.trainingResponse1
        elif(userInput.lower() == "no".lower() or userInput.lower() == "n"):
            response = defaultMode()
        else:
            response = "Please enter yes or no"


    elif (currentMode == "feedback"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        elif (userInput.isalpha()):
            response = "Please enter the number for Response ID"
        else:
            id = int((unicode.encode(userInput)))
            conn = database.connectToDB()
            if (database.checkIDExists(id, conn)):
                global responseID
                responseID = userInput
                currentMode = "feedback2"
                dblist = database.getPastResponse(id, conn)
                for var1 in dblist:
                    response = "Question is: " + var1['UserQuestion'] + "\n" + config.feedbackResponse2
            else:
                response = "Response ID does not exist"
    elif (currentMode == "feedback2"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            global responseID
            conn = database.connectToDB()
            id = int((unicode.encode(responseID)))
            database.updatePastResponse(id, userInput, conn)
            if (userInput.lower() == "yes".lower() or userInput.lower() == "y"):
                response = config.feedbackResponseYes
                currentMode = "morefeedback"
            if (userInput.lower() == "no".lower() or userInput.lower() == "n"):
                currentMode = "wrongfeedback"
                response = config.feedbackResponseNo
    elif (currentMode == "morefeedback"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        if (userInput.lower() == "yes".lower() or userInput.lower() == "y"):
            currentMode = "feedback"
            response = config.feedbackResponse1
        elif(userInput.lower() == "no".lower() or userInput.lower() == "n"):
            response = defaultMode()
        else:
            response = "Please enter yes or no"
    elif (currentMode == "wrongfeedback"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            global responseID
            id = int((unicode.encode(responseID)))
            conn = database.connectToDB()
            dblist = database.getPastResponse(id, conn)

            for var1 in dblist:
                if (database.checkRowExists(var1['QuestionPart'], userInput, var1['MatchingKeywords'], conn)):
                    log.writetofile("row already exist so not inserting")


                else:
                    log.writetofile("new row inserted")
                    database.storeNewResponse(userInput, var1['MatchingKeywords'], var1['QuestionPart'], conn)

            response = config.feedbackResponseYes
            currentMode = "morefeedback"
    elif (currentMode == "weather"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            questions, keywords = userInputQuestionKeyword(userInput)
            response = weather.getWeather(keywords)
            #response = "weather mode initiated"

    else:
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            #driver = webdriver.Chrome()
            #driver.get('http://localhost:5601/goto/2d0d499fbddc57172334c009f2ab5614')
            #driver.save_screenshot('vivek.png')
            #driver.quit()
            response = "to view statistics visit, visit http://localhost:5601/goto/2d0d499fbddc57172334c009f2ab5614"

    return response, image_url, questionPart


# Function for default mode when userinput==0
def defaultMode():
    global currentMode
    currentMode = "default"
    log.writetofile("Returning to default mode")
    return config.initialDisplayMessage


def getMessage():
    currentTime = int(time.strftime('%H:%M').split(':')[0])
    if currentTime >= 6 and currentTime <= 12:
        response = "Hello!" + " " + "Good morning!"
    elif currentTime >= 12 and currentTime <= 18:
        response = "Hello" + " " + "Good afternoon!"
    elif currentTime >= 18 and currentTime <= 22:
        response = "Hello" + " " + "Good evening!"
    else:
        response = "Hello" + " " + "Greetings. It's late and you should get some sleep!"
    return response
