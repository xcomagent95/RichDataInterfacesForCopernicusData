from flask import Flask , render_template, jsonify, request, send_file
import json

#initialize app
app = Flask(__name__) #define flask app

#conformance endpoint
#landingpage endpoint
@app.route('/',  methods = ['GET']) 
def getLandingPage():
    try:
        if(request.content_type == "text/html"):
            response = render_template('html/LandingPage.html')
            return response, 200
        elif(request.content_type == "application/json"):
            file = open('templates/json/LandingPage.json',) #open LandingPage.json
            payload = json.load(file) #create response
            file.close() #close LandingPage.json
            response = jsonify(payload)
            response.status_code = 200
            return response #return response and ok
        else:
                return "HTTP status code 406: not acceptable", 406
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error

@app.route('/conformance',  methods = ['GET']) 
def getConformance():
    try:
        if(request.content_type == "text/html"):
            response = render_template('html/ConfClasses.html')
            return response, 200
        elif(request.content_type == "application/json"):
            file = open('templates/json/ConfClasses.json',) #open ConfClasses.json
            payload = json.load(file) #create response
            file.close() #close ConfClasses.json
            response = jsonify(payload)
            response.status_code = 200
            return response #return response and ok
        else:
                return "HTTP status code 406: not acceptable", 406
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error

#processes endpoint
@app.route('/processes',  methods = ['GET']) 
def getProcesses():
    if(request.args.get('limit') == None):
        limit = 10 #default value
    else:
        limit = int(request.args.get('limit'))
    try:
        #has to be generated from scratch
        file = open('static/ProcessList.json',) #open ProcessList.json
        payload = json.load(file) #create response 
        file.close() #close ProcessList.json
        processesArray = payload["processes"]
        processes = {"processes": processesArray[0:limit],
                       "links": [
                                {
                                  "href": "https://processing.example.org/oapi-p/processes?f=json",
                                  "rel": "self",
                                  "type": "application/json"
                                },
                                {
                                  "href": "https://processing.example.org/oapi-p/processes?f=html",
                                  "rel": "alternate",
                                  "type": "text/html"
                                }
                              ]}
        response = jsonify(processes)
        response.status_code = 200
        return response #return response and ok
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error
    
#run application
app.run(debug=True, use_reloader=False) 