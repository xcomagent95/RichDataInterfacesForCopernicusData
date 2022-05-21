from flask import Flask , render_template, jsonify, request, send_file
import json
import os
import uuid
import datetime

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

#execute endpoint
@app.route('/processes/<processID>/execution', methods = ['POST'])
def executeProcess(processID):
    try:
        if(os.path.exists('templates/json/processes/' + str(processID) + 'ProcessDescription.json')):
            if(processID == "Echo"):
                input = request.args.get('input')
                jobID = str(uuid.uuid4()) #generate jobID
                #create job directories        
                os.mkdir("jobs/" + jobID) #directory for current job
                os.mkdir("jobs/" + jobID + "/results/") #results directory for current job
                os.mkdir("jobs/" + jobID + "/downloads/") #download directory for current job
                #create job.json
                job_file = {"jobID": str(jobID), 
                            "processID": str(processID), 
                            "input": [input],
                            "path": "jobs/" + jobID,
                            "results": "jobs/" + jobID + "/results/",
                            "downloads": "jobs/" + jobID + "/downloads/"}
                json.dumps(job_file, indent=4)
                with open("jobs/" + jobID + "/job.json", 'w') as f: #create file
                    json.dump(job_file, f) #write content
                    f.close() #close file  
                #create status.json
                status_file = {"jobID": str(jobID),
                                  "status": "accepted",
                                  "message": "Step 0/1",
                                  "progress": 0, 
                                  "created": str(datetime.datetime.now()),
                                  "links": [
                                          {"href": "link zum job",
                                           "rel": "self",
                                           "type": "application/json",
                                           "title": "this document"}
                                          ]}
                json.dumps(status_file, indent=4)
                with open("jobs/" + jobID + "/status.json", 'w') as f: #create file
                    json.dump(status_file, f) #write content
                    f.close() #close file               
                response = jsonify(status_file)  
                response.status_code = 201
                response.headers['location'] = "jobs/" + jobID
                return response #return response and ok and files created
        else:
            return "HTTP status code 404: not found", 404 #not found
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error

#job endpoint for status and dismiss
@app.route('/jobs/<jobID>', methods = ['GET', 'DELETE'])
def getJob(jobID):
    if(request.method == 'GET'):
        if(os.path.exists('jobs/' + str(jobID) + '/status.json')):
            try:
                file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                data = json.load(file) #create response   
                file.close() #close status.json
                
                response = jsonify(data)
                response.status_code = 200
                return  response #return response and ok
            except:
                return "HTTP status code 500: internal server error", 500 #internal server error
        else:
            return "HTTP status code 404: not found", 404 #not found
        
    if(request.method == 'DELETE'):
        try:       
            if(os.path.exists('jobs/' + str(jobID) + '/status.json')):
                with open('jobs/' + str(jobID) + '/status.json', "r") as f:
                    file = json.load(f)
                    if(file["status"] != "dismissed"):
                        file["status"] = "dismissed"
                        f.close()
                        with open('jobs/' + str(jobID) + '/status.json', "w") as f:
                            json.dump(file, f)
                            f.close()
                        return "HTTP Status Code 200: ok", 200
                    else:
                        return "HTTP Status Code 200: ok", 200
            else:
                return "HTTP status code 404: not found", 404 #not found
        except:
            return "HTTP status code 500: internal server error", 500 #internal server error
                
#run application
app.run(debug=True, use_reloader=False) 