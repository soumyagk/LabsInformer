import json
import os
import urllib
import simplejson
import pandas as pd

from flask import Flask, request, make_response

# Flask app should start in global layout
app = Flask(__name__)
#conn = pymysql.connect(host='localhost', port=5000, user='root', passwd='random123', db='chatbot')
#cur = conn.cursor()

default_resp = "Please visit www.ic.gatech.edu/content/labs-groups for more information"
lab_data = pd.read_excel("chatbotdb.xlsx")
#basic route 
# @app.route("/")
# def main():
#     return "Welcome!"

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
            return res
        res = fetchLab(field)
    elif req.get("result").get("action") == "lab_2_desc":
        lab = params.get("lab_name")
        if not field:
            return res
        res = fetchDesc(lab)
    elif req.get("result").get("action") == "lab_2_faculty":
        lab = params.get("lab_name")
        if not field:
            return res
        res = fetchFaculty(lab)
    elif req.get("result").get("action") == "lab_2_website":
        lab = params.get("lab_name")
        if not field:
            return res
        res = fetchWebsite(lab)
    
    return res

def fetchLab(field):
    # result = performQuery("select lab_name from sic_lab where field="+field)
    sub_frame = lab_data[lab_data['field']==field]['lab_name']
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
        response = default_resp

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

def fetchDesc(lab):
    # result = performQuery("select description from sic_lab where lab_name="+lab)
    sub_frame = lab_data[lab_data['lab_name']==lab]['description']
    count = sub_frame.shape[0]
    response = default_resp
    if count > 0:
        response = sub_frame.iloc[0]

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

def fetchFaculty(lab):
    # result = performQuery("select faculty from sic_lab where lab_name="+lab)
    sub_frame = lab_data[lab_data['lab_name']==lab]['faculty']
    count = sub_frame.shape[0]
    response = default_resp
    if count > 0:
        if(sub_frame.iloc[0]=="NA"):
            response = "Many researching faculty are involved with this lab. Visit their website for more information."
        else:
            response = sub_frame.iloc[0]+ " are associated with "+lab

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

def fetchWebsite(lab):
    # result = performQuery("select website from sic_lab where lab_name="+lab)
    sub_frame = lab_data[lab_data['lab_name']==lab]['website']
    count = sub_frame.shape[0]
    response = default_resp
    if count > 0:
        response = "You can visit "+sub_frame.iloc[0]+ " for more information on "+lab

    print("Response: "+response)

    json_res = prepareJson(response)
    return json_res

# def performQuery(query):
#     cur.execute(query)
#     result_str = []
#     for row in cur:
#         result_str.append(row);
#     return simplejson.dumps(result_str);

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