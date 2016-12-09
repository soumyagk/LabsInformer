import json
import os
import random
import urllib
import pandas as pd

from flask import Flask, request, make_response

# Flask app should start in global layout
app = Flask(__name__)

default_resp = "Please visit www.ic.gatech.edu/content/labs-groups for more information"
lab_data = pd.read_excel("chatbotdb.xlsx")
faculty_data = pd.read_excel("faculty.xlsx")

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    params = req.get("result").get("parameters")
    res = {}
    if req.get("result").get("action") == "field_2_lab":
        field = params.get("field")
        if not field:
            print("No field received")
            return res
        res = fetchLab(field)
    elif req.get("result").get("action") == "lab_2_desc":
        lab = params.get("lab_name")
        if not lab:
            print("No lab name received")
            return res
        res = fetchDesc(lab)
    elif req.get("result").get("action") == "lab_2_faculty":
        lab = params.get("lab_name")
        if not lab:
            print("No lab name received")
            return res
        res = fetchFaculty(lab)
    elif req.get("result").get("action") == "lab_2_website":
        lab = params.get("lab_name")
        if not lab:
            print("No lab name received")
            return res
        res = fetchWebsite(lab)
    elif req.get("result").get("action") == "faculty_2_lab":
        faculty = params.get("faculty")
        if not faculty:
            print("No faculty name received")
            return res
        res = fetchFacLab(faculty)
    
    print "Finally: \n"+res
    return res

def fetchLab(field):
    print("fetching lab from given field")
    sub_frame = lab_data[lab_data['field'].str.contains(field)]['lab_name']
    count = sub_frame.shape[0]
    response = ""
    if count > 1:
        for i in range(count):
            response += sub_frame.iloc[i]
            if i != count-1:
                response += ", "
        response += " are some labs working in the field of "
        response += field
    elif count == 1:
        response = sub_frame.iloc[0]+" works in the field of "+field
    else:
        magicno = random.randint(0,25)
        lab = lab_data.loc[magicno,'lab_name']
        field = lab_data.loc[magicno,'field']
        response = "I'm afraid I am not aware of labs in this field under the School of Interactive Computing. "
        response += "Did you know "+ lab +" works in the field of "+field+"?"

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

def fetchFacLab(faculty):
    print("fetching lab from given faculty")
    sub_frame = lab_data[lab_data['faculty'].str.contains(faculty)]['lab_name']
    print sub_frame.head()
    # gender = faculty_data[faculty_data['faculty']==faculty]['gender']
    # pronoun = ""
    # if gender == 'female':
    #     pronoun = "she"
    # else:
    #     pronoun = "he" 
    count = sub_frame.shape[0]
    print count
    response = ""
    if count > 1:
        response = "There are multiple labs associated with "+faculty+". They are "
        for i in range(count):
            response += sub_frame.iloc[i]
            if i == count-2:
                response += " and "
            elif i != count-1:
                response += ", "
        response += "."
    elif count == 1:
        response = faculty + " heads the "+ sub_frame.iloc[0]
    else:

        response = faculty +" does not seem to be working in any specific lab currently. Not that I'm aware of."

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

def fetchDesc(lab):
    print("fetching lab description")
    sub_frame = lab_data[lab_data['lab_name']==lab]['description']
    count = sub_frame.shape[0]
    response = default_resp
    if count > 0:
        response = sub_frame.iloc[0]
    else:
        response = default_resp

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

def fetchFaculty(lab):
    print("fetching lab faculty")
    sub_frame = lab_data[lab_data['lab_name']==lab]['faculty']
    count = sub_frame.shape[0]
    response = default_resp
    if count > 0:
        if(sub_frame.iloc[0]=="multiple"):
            response = "Many researching faculty are involved with this lab. Visit their website for more information. "
            response += lab_data[lab_data['lab_name']==lab]['website'].iloc[0]
        else:
            if ',' in sub_frame.iloc[0]:
                response = sub_frame.iloc[0]+ " are associated with "+lab
            else:
                response = sub_frame.iloc[0]+ " heads the "+lab
    else:
        response = "That's odd. I don't think I know about this lab. I need to up my game!"

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

def fetchWebsite(lab):
    print("fetching lab website")
    sub_frame = lab_data[lab_data['lab_name']==lab]['website']
    count = sub_frame.shape[0]
    response = default_resp
    if count > 0:
        response = "You can visit "+sub_frame.iloc[0]+ " for more information on "+lab
    else:
        response = default_resp

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

def prepareJson(response):
    return {
        "speech": response,
        "displayText": response,
        # "data": data,
        # "contextOut": [],
        "source": "chatbot"
    }

#check if executed file is in the main program and run the app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')