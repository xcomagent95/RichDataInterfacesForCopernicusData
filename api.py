from flask import Flask , render_template, jsonify, request, send_file
import json
import os
import uuid
import datetime

#initialize app
app = Flask(__name__) #define flask app

#landingpage endpoint
@app.route('/',  methods = ['GET']) #allowed methods: GET
def getLandingPage():
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"): #check requested content-type
            response = render_template('html/LandingPage.html') #render static landing page
            return response, 200 #return response and ok
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"): #check requested content-type
            file = open('templates/json/LandingPage.json',) #open LandingPage.json
            payload = json.load(file) #create response
            file.close() #close LandingPage.json
            response = jsonify(payload) #create response
            response.status_code = 200 #set response code
            return response #return response and ok
        else:
                return "HTTP status code 406: not acceptable", 406 #not acceptable 
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error

#conformance endpoint
@app.route('/conformance',  methods = ['GET']) #allowed methods: GET
def getConformance():
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"): #check requested content-type
            response = render_template('html/ConfClasses.html') #render static conformance page
            return response, 200 #return response and ok
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"): #check requested content-type
            file = open('templates/json/ConfClasses.json',) #open ConfClasses.json
            payload = json.load(file) #create response
            file.close() #close ConfClasses.json
            response = jsonify(payload) #create response
            response.status_code = 200 #set response code
            return response #return response and ok
        else:
                return "HTTP status code 406: not acceptable", 406 #not acceptable 
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error

#processes endpoint
@app.route('/processes', methods = ['GET']) #allowed methods: GET
def getProcesses():
    if(request.args.get('limit') == None or int(request.args.get('limit')) <= 0): #if no limit is set
        limit = 10 #default value
    else:
        limit = int(request.args.get('limit')) #get limit from request
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"):  #check requested content-type
                processDescriptions = os.listdir("templates/json/processes") #list registered processes
                response = "<!DOCTYPE html><html><body><h1>Processes:</h1>" #initialize HTML document
                counter = 0 #initialize counter
                for i in processDescriptions: #iterate over registered processes
                    file = open('templates/json/processes/' + i,) #open process descriptions
                    process = json.load(file) #load the data from .json file
                    file.close() #close file
                    #create process description as HTML
                    processHTML = "<p><b>id: " + process["id"] + "</b><br>title: " + process["title"] + "<br>description: " + process["description"] + "<br>version: " + process["version"] + "<br>jobControlOptions: " + str(process["jobControlOptions"]) + "<br>outputTransmission: " + str(process["outputTransmission"]) + "</p>links:<br> href: <a href=localhost:5000/processes/"+ process["id"] + "/execution?input=test>localhost:5000/processes/" + process["id"] + "/execution?input=test</a><br>title: Execute endpoint</p>"
                    response += processHTML #add process as HTML to response
                    counter += 1 #increment counter
                    if(counter == limit): #check if counter has reached request limit
                        break 
                #add links to response
                response += """<p><b>links:</b><br>
                        	href:<a href="localhost:5000/processes?f=text/html">localhost:5000/processes?f=text/html,</a><br>
                        	rel: self,<br>
                            type: text/html,<br>
                        	title: This document<br>
                            <br>
                            href:<a href="localhost:5000/processes?f=application/json">localhost:5000/processes?f=application/json,</a><br>
                        	rel: alternate,<br>
                            type: application/json,<br>
                        	title: This document as JSON<br>
                            </body></html>"""
                return(response), 200 #return response and ok
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"): #check requested content-type
            processDescriptions = os.listdir("templates/json/processes")  #list registered processes
            processesArray = [] #initialize process array                        
            for i in processDescriptions: #iterate over registered processes
                file = open('templates/json/processes/' + i,) #open process descriptions
                process = json.load(file) #load the data from .json file
                file.close() #close file 
                processesArray.append(process) #append process to processes array
            processes = {"processes": processesArray[0:limit], #add processes up to limit parameter and links
                            "links": [
                               {
                                 "href": "localhost:5000/processes?f=applicattion/json",
                                 "rel": "self",
                                 "type": "application/json"
                            },
                               {
                                 "href": "localhost:5000/processes?f=text/html",
                                 "rel": "alternate",
                                 "type": "text/html"
                            }
                            ]}
            response = jsonify(processes) #create response
            response.status_code = 200 #set response code
            return response #return response and ok
        else:
            return "HTTP status code 406: not acceptable", 406 #not acceptable 
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error
  
#process endpoint
@app.route('/processes/<processID>', methods = ['GET']) #allowed methods: GET
def getProcess(processID):
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"):  #check requested content-type
            if(os.path.exists('templates/html/processes/' + str(processID) + 'ProcessDescription.html')):
                response = render_template('html/processes/' + str(processID) + 'ProcessDescription.html')
                return response, 200
            else:
                return "HTTP status code 404: not found", 404 #not found
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"):  #check requested content-type
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
            return "HTTP status code 406: not acceptable", 406 #not acceptable
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error    

#execute endpoint
@app.route('/processes/<processID>/execution', methods = ['POST']) #allowed methods: POST
def executeProcess(processID):
    try:
        if(os.path.exists('templates/json/processes/' + str(processID) + 'ProcessDescription.json')):                
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
                           "type": "process",
                           "progress": 0, 
                           "created": str(datetime.datetime.now()),
                           "started": "none",
                           "finished": "none",
                           "links": [
                               {"href": "localhost:5000/jobs/" + jobID + "?f=application/json",
                                        "rel": "self",
                                        "type": "application/json",
                                        "title": "this document as JSON"},
                                        {"href": "localhost:5000/jobs/" + jobID + "?f=text/html",
                                        "rel": "alternate",
                                        "type": "text/html",
                                        "title": "this document as HTML"}
                                        ]}
            json.dumps(status_file, indent=4)
            with open("jobs/" + jobID + "/status.json", 'w') as f: #create file
                json.dump(status_file, f) #write content
            f.close() #close file               
            response = jsonify(status_file) #create response
            response.status_code = 201 #set response code
            response.headers['location'] = "jobs/" + jobID #set location header
            return response #return response and ok and files created
        else:
            return "HTTP status code 404: not found", 404 #not found
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error

#jobs endpoint    
@app.route('/jobs', methods = ['GET'])
def getJobs():
    if(request.args.get('limit') == None or int(request.args.get('limit')) <= 0):
        limit = 10 #default value
    else:
        limit = int(request.args.get('limit'))       
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"):
            jobs = os.listdir("jobs/")
            response = "<!DOCTYPE html><html><body><h1>Jobs:</h1>"
            counter = 0                  
            for i in jobs:
                file = open('jobs/' + i + "/status.json",)
                status = json.load(file)
                file.close() 
                file = open('jobs/' + i + "/job.json",)
                job = json.load(file)
                file.close() 
                jobHTML = "<p>processID: " + job["processID"] + "<br>jobID: " + status["jobID"] + "<br>status: " + status["status"] + "<br>message: " + status["message"] + "<br>created: " + status["created"] + "<br>links:<br>href: <a href=localhost:5000/jobs/"+ status["jobID"] + "?f=application/json>localhost:5000/jobs/" + status["jobID"] + "?f=application/json</a><br>rel: status as JSON<br>title: Job Status<br> type: application/json<br>href: <a href=localhost:5000/jobs/"+ status["jobID"] + "?f=text/html>localhost:5000/jobs/" + status["jobID"] + "?f=text/html</a><br>rel: status as JSON<br>title: Job Status<br> type: text/html</p>"
        
                response += jobHTML
                counter += 1
                if(counter == limit):
                    break
            response += """<p><b>links:</b><br>
                        href:<a href="localhost:5000/jobs?f=text/html">localhost:5000/jobs?f=text/html,</a><br>
                        rel: self,<br>
                        type: text/html,<br>
                        title: This document<br>
                        <br>
                        href:<a href="localhost:5000/jobs?f=application/json">localhost:5000/jobs?f=application/json,</a><br>
                        rel: alternate,<br>
                        type: application/json,<br>
                        title: This document as JSON<br>
                        </body></html>"""
            return(response), 200 
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"):
            jobList = os.listdir('jobs/')
            jobArray = []
            count = 0
            for i in jobList:
                if count == int(limit):
                    break
                with open('jobs/' + i + '/status.json', "r") as f:
                    data = json.load(f)
                    jobID = data["jobID"]
                    status = data["status"]
                    message = data["message"]
                    progress = data["progress"]
                    #links müssen noch ergänzt werden
                f.close()
                    
                with open('jobs/' + i + '/job.json', "r") as f:
                    data = json.load(f)
                    processID = data["jobID"]
                    #links müssen noch ergänzt werden
                f.close()
                job = {"processID": processID,
                       "jobID": jobID,
                       "status": status,
                       "message": message,
                       "progress": progress,
                       "links": [{
                           "href": "localhost:5000/jobs/" + jobID + "?f=application/json",
                           "rel": "status",
                           "type": "application/json",
                           "title": "Job status"
                           }]
                       }
                jobArray.append(job)
                count += 1
            jobs = {"jobs": jobArray,
                    "links": [
                               {"href": "localhost:5000/jobs?f=application/json",
                                "rel": "self",
                                "type": "application/json",
                                "title": "this document as JSON"},
                               {"href": "localhost:5000/jobs?f=text/html",
                                "rel": "alternate",
                                "type": "text/html",
                                "title": "this document as HTML"}
                               ]}
            response = jsonify(jobs)  
            response.status_code = 200
            return response #return response and ok and files created  
        else:
            return "HTTP status code 406: not acceptable", 406
    except:
         return "HTTP status code 500: internal server error", 500 #internal server error

#job endpoint for status and dismiss
@app.route('/jobs/<jobID>', methods = ['GET', 'DELETE'])
def getJob(jobID):
    if(request.method == 'GET'):
        if(request.content_type == "application/json" or request.args.get('f')=="application/json"):
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
        elif(request.content_type == "text/html" or request.args.get('f')=="text/html"):
            if(os.path.exists('jobs/' + str(jobID) + '/status.json')):
                try:
                    file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                    job = json.load(file) #create response   
                    print(job)
                    file.close() #close status.json
                    jobHTML = "<!DOCTYPE html><html><body><p><b>jobID: " + job["jobID"] + "</b><br>Status: " + job["status"] + "<br>Message: " + job["message"] + "<br>progress: " + str(job["progress"]) + "<br>" + job["created"] + "<br><b>links:</b><br><br>href: <a href=localhost:5000/jobs/"+ job["jobID"] + "?f=text/html>localhost:5000/jobs/" + job["jobID"] + "?f=text/html</a><br>rel: status<br>title: Job Status<br> type: text/html<br>href: <a href=localhost:5000/jobs/"+ job["jobID"] + "?f=application/json>localhost:5000/jobs/" + job["jobID"] + "?f=application/json</a><br>rel: status<br>title: Job Status<br> type: application/json</p></body></html>"
                    return  jobHTML #return response and ok
                except:
                    return "HTTP status code 500: internal server error", 500 #internal server error
            else:
                return "HTTP status code 404: not found", 404 #not found
        else:
            return "HTTP status code 406: not acceptable", 406
        
    if(request.method == 'DELETE'):
        try:       
            if(os.path.exists('jobs/' + str(jobID) + '/status.json')):
                with open('jobs/' + str(jobID) + '/status.json', "r") as f:
                    file = json.load(f)
                    if(file["status"] != "dismissed"):
                        file["status"] = "dismissed"
                        file["message"] = "job dismissed"
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