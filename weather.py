import requests
import json

def getWeather(request):

    url = "https://c2erak496a.execute-api.us-west-2.amazonaws.com/Test/reading/000002"
    for value in request:
        print value
        if( value in "library" or value in "milpitas" or value in "fremont"):
                if(value=="library"):
                 url = "https://c2erak496a.execute-api.us-west-2.amazonaws.com/Test/reading/000001"
                elif(value == "milpitas"):
                 url = "https://c2erak496a.execute-api.us-west-2.amazonaws.com/Test/reading/000002"
                else:
                 url = "https://c2erak496a.execute-api.us-west-2.amazonaws.com/Test/reading/000003"
        elif(value in "temperature" or value in "humidity" or value in "weather" ):
                   userRequest = value

        else:
                return "I cannot handle"

    print "url:" + url
    myResponse = requests.get(url)

    if(myResponse.ok):

        jData = json.loads(myResponse.content)
        if(userRequest == "temperature"):
         response ="temparature is %s" %  jData['payload']['temperature']
        elif(userRequest == "humidity"):
         response = "humidity is %s" % jData['payload']['humidity']
        else:
         response = "temperature is %s and humidity is %s" % (jData['payload']['temperature'] , jData['payload']['humidity'])

    #response = response + "Last Recorded at %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(1236472051807/1000.0))

    else:

        response = "Request failed"

    return response