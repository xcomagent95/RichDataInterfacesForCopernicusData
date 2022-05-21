from flask import Flask , render_template, jsonify, request, send_file
import json
import os

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
    if(request.args.get('limit') == None or int(request.args.get('limit')) <= 0):
        limit = 10 #default value
    else:
        limit = int(request.args.get('limit')) 
    try:
        if(request.content_type == "text/html"):
            return("test"), 200
            #generate from files
        
        elif(request.content_type == "application/json"):
            processDescriptions = os.listdir("templates/json/processes")
            processesArray = []
                        
            for i in processDescriptions:
                file = open('templates/json/processes/' + i,)
                process = json.load(file)
                file.close() 
                processesArray.append(process)
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
        else:
            return "HTTP status code 406: not acceptable", 406
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error
  
#process endpoint
@app.route('/processes/<processID>', methods = ['GET'])
def getProcess(processID):
    try:
        if(request.content_type == "text/html"):
            if(os.path.exists('templates/html/processes/' + str(processID) + 'ProcessDescription.html')):
                response = render_template('html/processes/' + str(processID) + 'ProcessDescription.html')
                return response, 200
            else:
                return "HTTP status code 404: not found", 404 #not found
        elif(request.content_type == "application/json"):
            if(os.path.exists('templates/json/processes/' + str(processID) + 'ProcessDescription.json')):
                file = open('templates/json/processes/' + str(processID) + 'ProcessDescription.json',) #open ProcessDescription.json
                payload = json.load(file) #create response   
                file.close() #close ProcessDescription.json
                response = jsonify(payload)
                response.status_code = 200
                return response #return response and ok
            else:
                return "HTTP status code 404: not found", 404 #not found
        else:
            return "HTTP status code 406: not acceptable", 406
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error    
#run application
app.run(debug=True, use_reloader=False) 