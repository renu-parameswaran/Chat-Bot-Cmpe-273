import lang_processor

def getReply(userInput):
    userInputArray = lang_processor.split_message(userInput)
    userInputWithOnlyQuestionAndKeywords = lang_processor.removeUnwantedWords(userInputArray)
    questions,keywords = lang_processor.seperateQuestionAndKeywords(userInputWithOnlyQuestionAndKeywords)

    response = "This is sara. How can I help?"
    if userInput.startswith("do"):
        response = "Need some intelligence first"

    return response

