from flask import Flask, request, redirect
import twilio.twiml
import requests, os, json

app = Flask(__name__)

key = os.environ['GOOGLE_KEY']

@app.route("/", methods=['GET', 'POST'])
def lookup():
    message_body = request.values.get('Body')

    try: 
        url = "https://www.googleapis.com/civicinfo/v2/representatives"
        querystring = {"key": key, "levels":["country","administrativeArea1"],
        "roles":["legislatorUpperBody","legislatorLowerBody"], "address": message_body}
        response = requests.request("GET", url, params=querystring)
        json_response = json.loads(response.text)
        offices = json_response['offices']
        officials = json_response['officials']
    except requests.exceptions.RequestException as e:
        print(e)
        message_response = "This is awkward. There was an error. Please enter your address again."
        resp = twilio.twiml.Response()
        resp.message(message_response)
        return str(resp)        

    str_list=[]

    str_list.append("Hi! You are represented by...\n")

    for x in offices:
        str_list.append("\n" + x["name"] + ": \n")
        for y in x['officialIndices']:
            str_list.append(officials[y]['name'] + " ")
            for z in officials[y]['phones']:
                str_list.append(z + "\n")

    str_list.append("\nWant help calling your reps? Check out: http://echothroughthefog.cordeliadillon.com/post/153393286626/how-to-call-your-reps-when-you-have-social-anxiety")     
    message_response = ''.join(str_list)

    resp = twilio.twiml.Response()
    resp.message(message_response)
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
