from flask import Flask, request, redirect
import twilio.twiml
import googlemaps, requests, os

app = Flask(__name__)

gmaps = googlemaps.Client(key=os.environ['GOOGLEMAPSKEY'])

@app.route("/", methods=['GET', 'POST'])
def lookup():
    message_body = request.values.get('Body')

    geocode_result = gmaps.geocode(message_body) #TODO: Auto retries but needs something to catch errors

    if (len(geocode_result) == 0):
        message_response = "This is not a valid address. Please try again and make sure to send an address including a street number, city, and state."
        resp = twilio.twiml.Response()
        resp.message(message_response)
        return str(resp)
    elif (len(geocode_result) > 1):
        message_response = "There are multiple address results for this address. Please try again and make sure to send an address including a street number, city, and state."
        resp = twilio.twiml.Response()
        resp.message(message_response)
        return str(resp)

    if (geocode_result[0]['types'] != ['street_address']):
        message_response = "Sometimes a city or zip code has multiple districts. Please try again and make sure to send an address including a street number, city, and state."
        resp = twilio.twiml.Response()
        resp.message(message_response)
        return str(resp)

    lat = str(geocode_result[0]['geometry']['location']['lat'])
    lng = str(geocode_result[0]['geometry']['location']['lng'])

    try:
        national = requests.get("https://congress.api.sunlightfoundation.com/legislators/locate?latitude=" + lat + "&longitude=" + lng)
        national.raise_for_status()
        national_json = national.json()
    except requests.exceptions.RequestException as e: 
        print(e)
        message_response = "This is awkward. There was an error. Please enter your address again."
        resp = twilio.twiml.Response()
        resp.message(message_response)
        return str(resp)

    try:
        state = requests.get("https://openstates.org/api/v1/legislators/geo/?lat=" + lat +"&long=" + lng)
        state.raise_for_status()
        state_json = state.json()    
    except requests.exceptions.RequestException as e: 
        print(e)
        message_response = "This is awkward. There was an error. Please enter your address again."
        resp = twilio.twiml.Response()
        resp.message(message_response)
        return str(resp)

    str_list=[]

    str_list.append("You are represented by:\nState level:\n")
    for x in range(0, len(state_json)):
        str_list.append(state_json[x]['first_name'] + " " + state_json[x]['last_name'] + " " 
            + "(" + state_json[x]['state'].upper() + "-" + state_json[x]['district'] + ")" + " ")
        str_list.append(state_json[x]['offices'][0]['phone'] + "\n \n") # TODO: could have more than one office

    str_list.append("National level:\n")
    for x in range(0, national_json['count']):
        if national_json['results'][x]['title']:
            str_list.append(national_json['results'][x]['title'] + " ")
        
        str_list.append(national_json['results'][x]['first_name'] + " " + national_json['results'][x]['last_name'] + " " 
            + "(" + national_json['results'][x]['state'])
        
        if (national_json['results'][x]['district']):
            str_list.append("-" + str(national_json['results'][x]['district']) + ") ")
        else:
            str_list.append(") ")
        
        str_list.append(national_json['results'][x]['phone'] + "\n \n")

    str_list.append("Want help calling your reps? Check out: http://echothroughthefog.cordeliadillon.com/post/153393286626/how-to-call-your-reps-when-you-have-social-anxiety")     
    message_response = ''.join(str_list)

    resp = twilio.twiml.Response()
    resp.message(message_response)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)