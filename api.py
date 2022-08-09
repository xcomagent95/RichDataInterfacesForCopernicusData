# -*- coding: utf-8 -*-
#imports
from flask import Flask , render_template, jsonify, request, send_file
import json
import os
import uuid
import datetime
import utils
import traceback
import logging
import xml.etree.ElementTree as ET

#set HTTP Version to HTTP 1.1
from werkzeug.serving import WSGIRequestHandler
from werkzeug.serving import BaseWSGIServer
WSGIRequestHandler.protocol_version = "HTTP/1.1"
BaseWSGIServer.protocol_version = "HTTP/1.1"

#initialize app
app = Flask(__name__) #initialize application

#landingpage endpoint
@app.route('/',  methods = ['GET']) #allowed methods: GET
def getLandingPage():
    app.logger.info('/') #add log entry when endpoint is called
    try:
        if(request.args.get('f')=="text/html" or 
           request.args.get('f') == None): #check requested content-type from inline request
            response = render_template('html/landingPage.html') #render static landing page
            return response, 200, {"link": "localhost:5000/?f=text/html", "resource": "landingPage"} #return response and okay with link and resource header
        elif(request.args.get('f')=="application/json"): #check requested content-type from inline request
            file = open('templates/json/landingPage.json',) #open landingPage.json
            payload = json.load(file) #create payload 
            file.close() #close landingPage.json
            response = jsonify(payload) #create response
            return response, 200, {"link": "localhost:5000/?f=application/json", "resource": "landingPage"} #return response and okay with link and resource header
        else:
                return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #retrurn internal server error if something went wrong

#conformance endpoint
@app.route('/conformance',  methods = ['GET']) #allowed methods: GET
def getConformance():
    app.logger.info('/conformance') #add log entry when endpoint is called
    try:
        if(request.args.get('f')=="text/html" or 
           request.args.get('f') == None): #check requested content-type from inline request
            response = render_template('html/confClasses.html') #render static conformance page
            return response, 200, {"link": "localhost:5000/conformance?f=text/html", "resource": "conformance"} #return response and okay with link and resource header
        elif(request.args.get('f')=="application/json"): #check requested content-type from inline request
            file = open('templates/json/confClasses.json',) #open ConfClasses.json
            payload = json.load(file) #create response
            file.close() #close ConfClasses.json
            response = jsonify(payload) #create response
            return response, 200, {"link": "localhost:5000/conformance?f=application/json", "resource": "conformance"} #return response and okay with link and resource header
        else:
                return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #retrun internal server error if something went wrong
    
#api endpoint
@app.route('/api',  methods = ['GET']) #allowed methods: GET
def getAPIDefinition():
    app.logger.info('/api') #add log entry when endpoint is called
    try:
        if(request.args.get('f')=="text/html" or 
           request.args.get('f') == None): #check requested content-type from inline request
            response = render_template('html/apiDefinition.html') #render static api definition page
            return response, 200, {"link": "localhost:5000/apiDefinition?f=text/html", "resource": "apiDefinition"} #return response and okay with link and resource header
        elif(request.args.get('f')=="application/json"): #check requested content-type from inline request
            file = open('templates/json/apiDefinition.json',) #open apiDefinition.json
            payload = json.load(file) #create response
            file.close() #close apiDefinition.json
            response = jsonify(payload) #create response
            return response, 200, {"link": "localhost:5000/api?f=application/json", "resource": "apiDefinition"} #return response and okay with link and resource header
        else:
                return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #retrun internal server error if something went wrong

#processes endpoint
@app.route('/processes', methods = ['GET']) #allowed methods: GET
def getProcesses():
    app.logger.info('/processes') #add log entry when endpoint is called
    try:
        if(request.args.get('limit') == None or #if no limit is set
       int(request.args.get('limit')) <= 0 or #or limit value is not valid
       int(request.args.get('limit')) > 10000): #or limit is to large
            limit = 10 #set limit to default value
        else:
            limit = int(request.args.get('limit')) #retrive limit value from request
        if(request.args.get('f')=="text/html" or 
           request.args.get('f') == None): #check requested content-type from inline request
                processList = [] #initialize list of processes
                processDescriptions = os.listdir("templates/json/processes") #list registered process descriptions
                for i in processDescriptions: #iterate over registered process descriptions
                    file = open('templates/json/processes/' + i,) #open process description
                    process = json.load(file) #load the data from .json file
                    file.close() #close .json file
                    processList.append(process) #append process to list of processes
                response = render_template('html/processList.html', processes=processList[0:limit]) #render dynamic process list 
                return response, 200, {"link": "localhost:5000/processes?f=text/html", "resource": "processes"} #return response and ok with link and resource header

        elif(request.args.get('f')=="application/json"): #check requested content-type from inline request
            processList = [] #initialize list of processes
            processDescriptions = os.listdir("templates/json/processes") #list registered process descriptions                 
            for i in processDescriptions: #iterate over registered process descriptions
                file = open('templates/json/processes/' + i,) #open process descriptions
                process = json.load(file) #load the data from .json file
                file.close() #close .json file
                processList.append(process) #append process to list of processes
            processes = {"processes": processList[0:limit], #add processes up to limit parameter and links
                            "links": [ #add links to self and alternate
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
            return response, 200, {"link": "localhost:5000/processes?f=application/json", "resource": "processes"} #return response and ok with link and resource header
        else:
            return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #retrun internal server error if something went wrong
  
#process endpoint
@app.route('/processes/<processID>', methods = ['GET']) #allowed methods: GET
def getProcess(processID):
    app.logger.info('/processes/' + processID) #add log entry when endpoint is called
    try:
        if(request.args.get('f')=="text/html" or 
           request.args.get('f') == None): #check requested content-type from inline request
            if(os.path.exists('templates/json/processes/' + str(processID) + 'ProcessDescription.json')): #check if process description exists
                file = open('templates/json/processes/' + str(processID) + 'ProcessDescription.json',) #open processDescription.json
                process = json.load(file) #load the data from .json file
                file.close() #close processDescription.json
                response = render_template("html/Process.html", process=process) #render dynamic process
                return response, 200, {"link": "localhost:5000/processes/" + str(processID) + "?f=text/html", "resource": "process - " + str(processID)} #return response and ok with link and resource header
            else:
                exception = render_template('html/exception.html', title="No such process exception", description="Requested process could not be found", type="no-such-process")
                return exception, 404, {"resource": "no-such-process"} #return not found if requested process is not found
        elif(request.args.get('f')=="application/json"): #check requested content-type from inline request
            if(os.path.exists('templates/json/processes/' + str(processID) + 'ProcessDescription.json')): #check if process description exists
                file = open('templates/json/processes/' + str(processID) + 'ProcessDescription.json',) #open ProcessDescription.json
                payload = json.load(file) #load the data from .json file
                file.close() #close ProcessDescription.json
                response = jsonify(payload) #create response
                return response, 200, {"link": "localhost:5000/processes/" + str(processID) + "?f=application/json", "resource": "process - " + str(processID)} #return response and ok with link and resource header
            else:
                exception = {"title": "No such process exception", "description": "Requested process could not be found", "type": "no-such-process"}
                return exception, 404, {"resource": "no-such-process"} #return not found if requested process is not found 
        else:
            return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #retrun internal server error if something went wrong

#execute endpoint
@app.route('/processes/<processID>/execution', methods = ['POST']) #allowed methods: POST
def executeProcess(processID):
    app.logger.info('/processes/' + processID + '/execution') #add log entry when endpoint is called
    try:
        if(os.path.exists('templates/json/processes/' + str(processID) + 'ProcessDescription.json')): #check if process description exists
            data = json.loads(request.data.decode('utf8').replace("'", '"')) #jsonify request body
            inputParameters = utils.parseInput(processID, data) #parse request body
            if(inputParameters == False): #if request body can not be parsed
                return "HTTP status code 400: bad request", 400 #return bad request
            jobID = str(uuid.uuid4()) #generate jobID
            created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            #create job directories        
            os.mkdir("jobs/" + jobID) #directory for current job
            os.mkdir("jobs/" + jobID + "/results/") #results directory for current job
            #create job.json
            job_file = {"jobID": str(jobID), #set jobID
                        "processID": str(processID), #set processID
                        "input": inputParameters[0], #set input parameters
                        "output": inputParameters[2],
                        "responseType": inputParameters[1], #set response type (raw or document)
                        "path": "jobs/" + jobID, #set job path
                        "results": "jobs/" + jobID + "/results/", #set results path
                        "downloads": "jobs/" + jobID + "/downloads/"} #set downloads path
            json.dumps(job_file, indent=4) #dump content
            with open("jobs/" + jobID + "/job.json", 'w') as f: #create file
                json.dump(job_file, f) #write content
            f.close() #close file  

            #create status.json
            status_file = {"jobID": str(jobID), #set jobID
                           "processID": str(processID), #set processID
                           "status": "accepted", #set initial status
                           "message": "Step 0/1", #set initial message
                           "type": "process", #set type of job
                           "progress": 0, #set unitial progress
                           "created": created, #set created timestamp
                           "started": "none", #set initial started timestamp
                           "finished": "none", #set initial finished tiestamp
                           "links": [ #add links to self and alternate
                               {
                                   "href": "localhost:5000/jobs/" + jobID + "?f=application/json",
                                    "rel": "self",
                                    "type": "application/json",
                                    "title": "this document as JSON"},
                                {
                                    "href": "localhost:5000/jobs/" + jobID + "?f=text/html",
                                    "rel": "alternate",
                                    "type": "text/html",
                                    "title": "this document as HTML"
                                }
                                ]}
            json.dumps(status_file, indent=4) #dump content
            with open("jobs/" + jobID + "/status.json", 'w') as f: #create file
                json.dump(status_file, f) #write content
            f.close() #close file

            response = jsonify(status_file) #create response
            return response, 201, {"location": "localhost:5000/jobs/" + jobID + "?f=application/json", "resource": "job - " + str(jobID) + "created"} #return response and ok and files created with location header
        else:
            exception = {"title": "No such process exception", "description": "Requested process could not be found", "type": "no-such-process"}
            return exception, 404 #return not found if requested process is not found 
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #retrun internal server error if something went wrong

#jobs endpoint    
@app.route('/jobs', methods = ['GET']) #allowed methods: GET
def getJobs():
    app.logger.info('/jobs') #add log entry when endpoint is called
    try:
        if(request.args.get('limit') == None or #if no limit is set
           int(request.args.get('limit')) <= 0 or #or limit value is not valid
           int(request.args.get('limit')) > 1000): #or limit is to large
            limit = 10 #set limit to default value
        else:
            limit = int(request.args.get('limit')) #retrieve limit value from request
            
        if(request.args.get('type') == None): #if no type parameter is passed
            type = ["process"] #set type parameter to default
        else: #if type parameter is passed
            type = request.args.get('type') #set type parameter to passed value
            
        if(request.args.get('processID') == None): #if no processID parameter is passed
            processes = ["Echo", "FloodMonitoring"] #set processID parameter to default
        else: #if processID parameter is passed
            processes = request.args.get('processID') #set processID parameter to passed value
            
        if(request.args.get('status') == None): #if no status parameter is passed
            stati = ["accepted", "running", "successful", "failed", "dismissed"] #set stati parameter to default
        else:
            stati = request.args.get('status') #set stati parameter to passed value
		
        jobs = os.listdir('jobs/') #list created jobs       
        jobList = [] #initialize list of jobs  
        for i in jobs: #iterate over created jobs
            file = open('jobs/' + i + "/status.json",) #open status.sjon
            status = json.load(file) #load the data from .json file
            file.close() #close .json file
			
            jobCreationDate = datetime.datetime.strptime(str(status["created"]), "%Y-%m-%d %H:%M:%S") #retrieve job creation date and covert to correct format
            datetimeParam = utils.checkCreationDate(jobCreationDate, request) #check creation date with request
			
            durationParams = utils.checkDuration(status, request) #check duration with request
            minDurationParam = durationParams[0] #set min duration
            maxDurationParam = durationParams[1] #set max duration
			
            if(status["type"] in type and #check type
               status["processID"] in processes and #check processID
               status["status"] in stati and #check status
               datetimeParam == True and #check datetime
               minDurationParam == True and #check min duration
               maxDurationParam == True): #check max duration
				#create job entry
                job = {"jobID": status["jobID"], #set jobID
					   "processID": status["processID"], #set processID
					   "type": status["type"], #set type
					   "status": status["status"], #set status
					   "message": status["message"], #set message
					   "created": status["created"], #set created
					   "links": [{ #add links to status file in json and html encodings
							   "href": "localhost:5000/jobs/" + status["jobID"] + "?f=application/json",
							   "rel": "status",
							   "type": "application/json",
							   "title": "Job status as JSON"
						   },
						   {
							   "href": "localhost:5000/jobs/" + status["jobID"] + "?f=text/html",
							   "rel": "status",
							   "type": "text/html",
							   "title": "Job status as HTML"
						   }]
					   }
                jobList.append(job) #append job to list of jobs
		
        if(request.args.get('f')=="text/html" or 
           request.args.get('f') == None): #check requested content-type from inline request
            response = render_template('html/jobList.html', status=jobList[0:limit]) #render dynamic job list 
            return response, 200, {"link": "localhost:5000/jobs?f=text/html", "resource": "jobs"} #return response and ok with link and resource header
        
        
        elif(request.args.get('f')=="application/json"): #check requested content-type from inline request
            temp = jobList[0:limit]
            jobList = {"jobs": temp, #create response payload
    				"links": [ #add links to self and alternate 
    							  {"href": "localhost:5000/jobs?f=application/json",
    							   "rel": "self",
    							   "type": "application/json",
    							   "title": "this document as JSON"},
    							  {"href": "localhost:5000/jobs?f=text/html",
    							   "rel": "alternate",
    							   "type": "text/html",
    							   "title": "this document as HTML"}
    						 ]}		
            response = jsonify(jobList) #create response 
            return response, 200, {"link": "localhost:5000/jobs?f=application/json", "resource": "jobs"} #return response and ok with link and resource header
        else:
            return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #retrun internal server error if something went wrong

#job endpoint for status and dismiss
@app.route('/jobs/<jobID>', methods = ['GET', 'DELETE']) #allowed methods: GET, DELETE
def getJob(jobID):
    if(request.method == 'GET'): #if get request is recieved
        app.logger.info('[GET] /jobs/' + jobID) #add log entry when endpoint is called
        try:
            if(request.args.get('f')=="application/json"): #check requested content-type from inline request
                if(os.path.exists('jobs/' + str(jobID) + '/status.json')): #check if requested job exists
                    file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                    data = json.load(file) #create response   
                    file.close() #close status.josn
                    response = jsonify(data) #create response
                    return  response, 200, {"link": "localhost:5000/jobs/" + str(jobID) + "?f=application/json", "resource": "job - " + str(jobID)} #return response and ok with link und resource header
                else:
                    exception = {"title": "No such job exception", "description": "No job with the requested jobID could be found", "type": "no-such-job"}
                    return exception, 404, {"resource": "no-such-job"} #return not found if requested job is not found 
            elif(request.args.get('f')=="text/html" or 
                 request.args.get('f') == None): #check requested content-type from inline request
                if(os.path.exists('jobs/' + str(jobID) + '/status.json')):
                    file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                    job = json.load(file) #create response   
                    file.close() #close status.json
                    response = render_template("html/Job.html", job=job) #render dynamic job
                    return response, 200, {"link": "localhost:5000/jobs/" + str(jobID) + "?f=text/html", "resource": "job - " + str(jobID)} #return response and ok
                else:
                    exception = render_template('html/exception.html', title="No such job exception", description="No job with the requested jobID could be found", type="no-such-job")
                    return exception, 404, {"resource": "no-such-job"} #return not found if requested job is not found
            else:
                return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
        except Exception:
            traceback.print_exc()
            return "HTTP status code 500: internal server error", 500 #return internal server error if something went wrong
        
    if(request.method == 'DELETE'):
        app.logger.info('[DELETE] /jobs/' + jobID) #add log entry when endpoint is called
        try:       
            if(os.path.exists('jobs/' + str(jobID) + '/status.json')): #check if jobID exists
                with open('jobs/' + str(jobID) + '/status.json', "r") as f: #open status.json
                    file = json.load(f) #load data from status.json
                    if(file["status"] != "dismissed"): #if job is not dismissed
                        file["status"] = "dismissed" #set status to dismissed
                        file["message"] = "job dismissed" #set emssage to dismissed
                        f.close() #close status.json
                        with open('jobs/' + str(jobID) + '/status.json', "w") as f: #write status.json
                            json.dump(file, f) #dump content
                            f.close() #close status.json                    
                        file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                        data = json.load(file) #load data from status.json 
                        file.close() #close status.json
                        
                        if(request.args.get('f')=="text/html" or 
                         request.args.get('f') == None):
                            file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                            job = json.load(file) #create response   
                            file.close() #close status.json
                            response = render_template("html/Job.html", job=job) #render dynamic job
                            return response, 200, {"link": "localhost:5000/jobs/" + str(jobID) + "?f=text/html", "resource": "job - " + str(jobID) + " - dismissed"} #return response and ok
                        elif(request.args.get('f')=="application/json"):
                            response = jsonify(data) #create response
                            return response, 200, {"link": "localhost:5000/jobs/" + str(jobID) + "?f=application/json", "resource": "job - " + str(jobID) + " - dismissed"} #return response and ok with link und resource header
                        else:
                            return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
                    else: #check requested content-type from inline request
                        if(request.args.get('f')=="text/html" or 
                         request.args.get('f') == None):
                            file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                            job = json.load(file) #create response   
                            file.close() #close status.json
                            response = render_template("html/Job.html", job=job) #render dynamic job
                            return response, 410, {"link": "localhost:5000/jobs/" + str(jobID) + "?f=text/html", "resource": "job - " + str(jobID) + " - dismissed"} #return response and ok
                        elif(request.args.get('f')=="application/json"):
                            file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                            data = json.load(file) #load data from status.json 
                            file.close() #close status.json
                            response = jsonify(data) #create response
                            return response, 410, {"link": "localhost:5000/jobs/" + str(jobID) + "?f=application/json", "resource": "job - " + str(jobID) + " - dismissed"} #return gone when job was already dismissed
                        else:
                            return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported   
            else:
                if(request.args.get('f')=="text/html" or request.args.get('f') == None):
                    exception = render_template('html/exception.html', title="No such job exception", description="No job with the requested jobID could be found", type="no-such-job")
                    return exception, 404, {"resource": "no-such-job"} #return not found if requested job is not found
                elif(request.args.get('f')=="application/json"):
                    exception = {"title": "No such job exception", "description": "No job with the requested processID could be found", "type": "no-such-job"}
                    return exception, 404, {"resource": "no-such-job"} #return not found if requested job is not found 
                else:
                    return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported   
        except Exception:   
            traceback.print_exc()
            return "HTTP status code 500: internal server error", 500 #return internal server error if something went wrong

@app.route('/jobs/<jobID>/results', methods = ["GET"]) #allowed methods: GET
def getResults(jobID):
    app.logger.info('/jobs/' + jobID + '/results') #add log entry when endpoint is called
    try:         
        if(os.path.exists('jobs/' + str(jobID))):
            file = open('jobs/' + str(jobID) + "/status.json",) #open status.json
            status = json.load(file) #load the data from .json file
            file.close() #close .json file
            file = open('jobs/' + str(jobID) + "/job.json",) #open job.json
            job = json.load(file) #load the data from .json file
            file.close() #close .json file  
            
            if(job["processID"] == "Echo"): #check processID
                if(status["status"] == "successful"): #check if job is successful
                    if(job["responseType"] == "raw"): #check if response type is raw
                        return send_file('jobs/' + str(jobID) + '/results/result.json', mimetype=job["resultMediaType"]), 200 #send raw file
                    else: #check if response type is document
                        file = open('jobs/' + str(jobID) + '/results/result.json',) #open apiDefinition.json
                        payload = json.load(file) #create response
                        file.close() #close apiDefinition.json
                        
                        result = {"outgoingEcho": payload}
                        
                        json.dumps(result, indent=4) #dump content
                        with open("jobs/" + jobID + "/results/resultsDocument.json", 'w') as f: #create file
                            json.dump(result, f) #write content
                        f.close() #close file
                        
                        return send_file('jobs/' + str(jobID) + '/results/resultsDocument.json', mimetype=job["resultMediaType"]), 200
                elif(status["status"] == "failed"): #check if job failed
                    exception = {"title": "Job failed exception", "description": status["message"], "type": "job-results-failed"}
                    return exception, 404, {"resource": "job-failed"} #return not found if requested job is failed
                else:
                    exception = {"title": "Results not ready exception", "description": "The results with the requested jobID are not ready", "type": "result-not-ready"} 
                    return exception, 404, {"resource": "results-not-ready"} #return not found if requested job results are not ready
                
            elif(job["processID"] == "FloodMonitoring"): #check processID
                if(status["status"] == "successful"): #check if job is successful
                    if(job["responseType"] == "raw"): #check if response type is raw
                        if(len(job["output"]) > 1):
                            utils.zipResults(jobID)
                            return send_file('jobs/' + str(jobID) + '/results/ndsi_bin.zip', mimetype='application/zip'), 200 #send raw file
                        elif(job["output"][0][0] == "ndsi"):
                            return send_file('jobs/' + str(jobID) + '/results/ndsi.tif', mimetype=job["output"][0][1]), 200 #send raw file
                        elif(job["output"][0][0] == "bin"):
                            return send_file('jobs/' + str(jobID) + '/results/bin.tif', mimetype=job["output"][0][1]), 200 #send raw file
                    elif(job["responseType"] == "document"): #check if response type is document
                        if(len(job["output"]) > 1):
                            ndsi64 = utils.encodeImageBase64('jobs/' + str(jobID) + '/results/ndsi_clipped.tif')
                            bin64 = utils.encodeImageBase64('jobs/' + str(jobID) + '/results/bin.tif')
                            ndsi = {"ndsi": [
                                    {"href": "localhost:5000/download/" + str(jobID) + "/ndsi",
                                     "type": job["output"][0][1]
                                     },
                                    {"value": ndsi64,
                                     "encoding": "base64",
                                     "mediaType": job["output"][0][1]},
                                ]}
                            bin = {"bin": [
                                    {"href": "localhost:5000/download/" + str(jobID) + "/bin",
                                     "type": job["output"][0][1]
                                     },
                                    {"value": bin64,
                                     "encoding": "base64",
                                     "mediaType": job["output"][0][1]},
                                ]}
                            response = jsonify([ndsi, bin])
                            return response, 200 #send raw file                        
                        elif(job["output"][0][0] == "ndsi"):
                            ndsi64 = utils.encodeImageBase64('jobs/' + str(jobID) + '/results/ndsi_clipped.tif')
                            result = {"ndsi": [
                                    {"href": "localhost:5000/download/" + str(jobID) + "/ndsi",
                                     "type": job["output"][0][1]
                                     },
                                    {"value": ndsi64,
                                     "encoding": "base64",
                                     "mediaType": job["output"][0][1]},
                                ]}
                            return result, 200 #send raw file
                        elif(job["output"][0][0] == "bin"):
                            bin64 = utils.encodeImageBase64('jobs/' + str(jobID) + '/results/bin.tif')
                            result = {"bin": [
                                    {"href": "localhost:5000/download/" + str(jobID) + "/bin",
                                     "type": job["output"][0][1]
                                     },
                                    {"value": bin64,
                                     "encoding": "base64",
                                     "mediaType": job["output"][0][1]},
                                ]}
                            return result, 200 #send raw file
                elif(status["status"] == "failed"): #check if job failed
                    exception = {"title": "Job failed exception", "description": status["message"], "type": "job-results-failed"}
                    return exception, 404, {"resource": "job-failed"} #return not found if requested job is failed
                else:
                    exception = {"title": "Results not ready exception", "description": "The results with the requested jobID are not ready", "type": "result-not-ready"} 
                    return exception, 404, {"resource": "results-not-ready"} #return not found if requested job results are not ready
        else:
            exception = {"title": "No such job exception", "description": "No job with the requested jobID could be found", "type": "no-such-job"}
            return exception, 404, {"resource": "no-such-job"} #return not found if requested job is not found 
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #return internal server error if something went wrong

@app.route('/download/<jobID>/<requestedFile>', methods = ["GET"])
def downloadFile(jobID, requestedFile):
    try:
        if(os.path.exists('jobs/' + str(jobID))):
            file = open('jobs/' + str(jobID) + "/status.json",) #open status.json
            status = json.load(file) #load the data from .json file
            file.close() #close .json file:
            file = open('jobs/' + str(jobID) + "/job.json",) #open job.json
            job = json.load(file) #load the data from .json file
            file.close() #close .json file  
            if(job["processID"] == "FloodMonitoring"): #check processID
                if(str(requestedFile) == "bin"):
                    return send_file('jobs/' + str(jobID) + '/results/bin.tif', mimetype='application/tiff'), 200 #send raw file
                elif(str(requestedFile) == 'ndsi'):
                    return send_file('jobs/' + str(jobID) + '/results/ndsi_clipped.tif', mimetype='application/tiff'), 200 #send raw file
                else:
                    exception = {"title": "No such file exception", "description": "No file could be found", "type": "no-such-file"}
                    return exception, 404, {"resource": "no-such-file"} #return not found if requested job is not found 
            else:
                return "HTTP status code 501: not implemented", 501
        else:
            exception = {"title": "No such job exception", "description": "No job with the requested jobID could be found", "type": "no-such-job"}
            return exception, 404, {"resource": "no-such-job"} #return not found if requested job is not found 
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #return internal server error if something went wrong:

@app.route('/coverage', methods = ["GET"])
def getCoverage():
    try:
        kmlFiles = os.listdir('data/coverage/')
        coverages = []
        bboxes = []
        for i in kmlFiles:
            tree = ET.parse('data/coverage/' + i)
            root = tree.getroot()
            bbox = root[0][1][1][2][0].text
            name = i[:-4]
            date = i[17:21] + '.' + i[21:23] + '.' + i[23:25]
            dataset = {'name': name,
					   'bbox': bbox,
					   'date': date}
            coverages.append(dataset)
            bboxArray = bbox.split()
            coordinates = []
            for i in bboxArray:
                rawCoords = i.replace(',', ' ')
                coords = rawCoords.split()
                coordinates.append(float(coords[0]))
                coordinates.append(float(coords[1]))
            geojson = {"type": "FeatureCollection", "features": [{
					  "type": "Feature",
					  "properties": {
						  "name": name,
						  "date": date},
					  "geometry": {
						"type": "Polygon",
						"coordinates": [
						  [
							[
							  coordinates[0], coordinates[1]
							],
							[
							  coordinates[2], coordinates[3]
							],
							[
							  coordinates[4], coordinates[5]
							],
							[
							  coordinates[6], coordinates[7]
							],
							[
							  coordinates[0], coordinates[1]
							]
						  ]
						]
					  }
					}
				  ]
				}
            bboxes.append(geojson)
        coverageJSON = {'coverages': coverages}
        if(request.args.get('f')=="text/html" or request.args.get('f') == None): #check requested content-type from inline request
            response = render_template("html/coverage.html", coverages=coverages, bboxes=bboxes) #render dynamic coverage
            return response, 200, {"link": "localhost:5000/coverage?f=application/json", "resource": "coverage"} #return response and ok with link und resource header
        elif(request.args.get('f')=="application/json"): #check requested content-type from inline request
            response = jsonify(coverageJSON)
            return response, 200, {"link": "localhost:5000/coverage?f=application/json", "resource": "coverage"} #return response and ok with link und resource header
        else:
            return "HTTP status code 406: not acceptable", 406 #return not acceptable if requested content-type is not supported
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #return internal server error if something went wrong    
    
#run application
if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False) 
    