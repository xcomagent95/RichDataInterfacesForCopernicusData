from flask import Flask , render_template, jsonify, request, send_file
import json
import os
import uuid
import datetime
import utils
import traceback

#initialize app
app = Flask(__name__) #define flask app

#landingpage endpoint
@app.route('/',  methods = ['GET']) #allowed methods: GET
def getLandingPage():
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"): #check requested content-type
            response = render_template('html/landingPage.html') #render static landing page
            return response, 200, {"link": "localhost:5000/?f=text/html"} #return response and ok
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"): #check requested content-type
            file = open('templates/json/landingPage.json',) #open LandingPage.json
            payload = json.load(file) #create response
            file.close() #close LandingPage.json
            response = jsonify(payload) #create response
            response.headers['link'] = "localhost:5000/?f=application/json"
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
            response = render_template('html/confClasses.html') #render static conformance page
            return response, 200, {"link": "localhost:5000/conformance?f=text/html"} #return response and ok
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"): #check requested content-type
            file = open('templates/json/confClasses.json',) #open ConfClasses.json
            payload = json.load(file) #create response
            file.close() #close ConfClasses.json
            response = jsonify(payload) #create response
            response.headers['link'] = "localhost:5000/conformance?f=application/json"
            response.status_code = 200 #set response code
            return response #return response and ok
        else:
                return "HTTP status code 406: not acceptable", 406 #not acceptable 
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error
    
#api endpoint
@app.route('/api',  methods = ['GET']) #allowed methods: GET
def getAPIDefinition():
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"): #check requested content-type
            response = render_template('html/api/index.html') #render api definition
            return response, 200, {'link':'localhost:5000/apiDefinition?f=text/html'}
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"): #check requested content-type
            file = open('templates/json/apiDefinition.json',) #open ConfClasses.json
            payload = json.load(file) #create response
            file.close() #close ConfClasses.json
            response = jsonify(payload) #create response
            response.headers['link'] = "localhost:5000/apiDefinition?f=application/json"
            response.status_code = 200 #set response code
            return response #return response and ok
        else:
                return "HTTP status code 406: not acceptable", 406 #not acceptable 
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #internal server error

#processes endpoint
@app.route('/processes', methods = ['GET']) #allowed methods: GET
def getProcesses():
    if(request.args.get('limit') == None or int(request.args.get('limit')) <= 0 or int(request.args.get('limit')) > 1000): #if no limit is set
        limit = 10 #default value
    else:
        limit = int(request.args.get('limit')) #get limit from request
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"): #check requested content-type
                processList = []
                processDescriptions = os.listdir("templates/json/processes") #list registered processes
                response = "<!DOCTYPE html><html><body><h1>Processes:</h1>" #initialize HTML document
                counter = 0 #initialize counter
                for i in processDescriptions: #iterate over registered processes
                    file = open('templates/json/processes/' + i,) #open process descriptions
                    process = json.load(file) #load the data from .json file
                    file.close() #close file
                    processList.append(process)
                    if(counter == limit): #check if counter has reached request limit
                        break 
                response = render_template('html/processes.html', processes=processList) #render static conformance page
                return response, 200, {"link": "localhost:5000/processes?f=text/html"} #return response and ok
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
            response.headers['link'] = "localhost:5000/processes?f=application/json"
            response.status_code = 200 #set response code
            return response #return response and ok
        else:
            return "HTTP status code 406: not acceptable", 406 #not acceptable 
    except Exception:
        traceback.print_exc()
        return "HTTP status code 500: internal server error", 500 #internal server error
  
#process endpoint
@app.route('/processes/<processID>', methods = ['GET']) #allowed methods: GET
def getProcess(processID):
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"):  #check requested content-type
            if(os.path.exists('templates/json/processes/' + str(processID) + 'ProcessDescription.json')):
                file = open('templates/json/processes/' + str(processID) + 'ProcessDescription.json',) #open ProcessDescription.json
                process = json.load(file) #create response   
                file.close() #close ProcessDescription.json
                response = render_template("html/Process.html", process=process)
                return response, 200, {"link": "localhost:5000/processes/" + str(processID) + "?f=text/html"} #return response and ok
            else:
                return "HTTP status code 404: not found", 404 #not found
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"):  #check requested content-type
            if(os.path.exists('templates/json/processes/' + str(processID) + 'ProcessDescription.json')):
                file = open('templates/json/processes/' + str(processID) + 'ProcessDescription.json',) #open ProcessDescription.json
                payload = json.load(file) #create response   
                file.close() #close ProcessDescription.json
                response = jsonify(payload)
                response.headers['link'] = "localhost:5000/processes/" + str(processID) + "?f=application/json"
                response.status_code = 200
                return response #return response and ok
            else:
                return "HTTP status code 404: not found", 404 #not found
        else:
            return "HTTP status code 406: not acceptable", 406 #not acceptable
    except Exception:
        traceback.print_exc()
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
                           "created": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
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
            response.headers['location'] = "localhost:5000/jobs/" + jobID + "?f=application/json" #set location header
            response.headers['link'] = "localhost:5000/jobs/" + jobID + "?f=application/json"
            return response #return response and ok and files created
        else:
            return "HTTP status code 404: not found - No such process", 404 #not found
    except:
        return "HTTP status code 500: internal server error", 500 #internal server error

#jobs endpoint    
@app.route('/jobs', methods = ['GET'])
def getJobs():
    if(request.args.get('limit') == None or int(request.args.get('limit')) <= 0 or int(request.args.get('limit')) > 1000):
        limit = 10 #default value
    else:
        limit = int(request.args.get('limit'))   
        
    if(request.args.get('type') == None):
        type = ["process"]
    else:
        type = request.args.get('type')   
        
    if(request.args.get('processID') == None):
        processes = ["Echo"]
    else:
        processes = request.args.get('processID')  
        
    if(request.args.get('status') == None):
        stati = ["accepted", "running", "successful", "failed", "dismissed"]
    else:
        stati = request.args.get('status')
        
    try:
        if(request.content_type == "text/html" or request.args.get('f')=="text/html"):
            jobs = os.listdir("jobs/")
            counter = 0    
            jobList = []              
            for i in jobs:
                file = open('jobs/' + i + "/status.json",)
                status = json.load(file)
                file.close() 
                file = open('jobs/' + i + "/job.json",)
                job = json.load(file)
                file.close() 
                
                jobCreationDate = datetime.datetime.strptime(str(status["created"]), "%Y-%m-%d %H:%M:%S") 
                datetimeParam = utils.checkCreationDate(jobCreationDate, request)
                
                durationParams = utils.checkDuration(status, request)
                minDurationParam = durationParams[0]
                maxDurationParam = durationParams[1]
                
                if(status["type"] in type and job["processID"] in processes and status["status"] in stati and datetimeParam == True and minDurationParam == True and maxDurationParam == True):
                    jobList.append(status)
                    counter += 1
                    if(counter == limit):
                        break
            response = render_template('html/jobs.html', status=jobList)
            return response, 200, {"link": "localhost:5000/jobs?f=text/html"}
        
        
        elif(request.content_type == "application/json" or request.args.get('f')=="application/json"):
            jobList = os.listdir('jobs/')
            jobArray = []
            count = 0
            for i in jobList:
                
                file = open('jobs/' + i + "/status.json",)
                status = json.load(file)
                file.close() 
                file = open('jobs/' + i + "/job.json",)
                job = json.load(file)
                file.close() 
                
                jobCreationDate = datetime.datetime.strptime(str(status["created"]), "%Y-%m-%d %H:%M:%S") 
                datetimeParam = utils.checkCreationDate(jobCreationDate, request)
                
                durationParams = utils.checkDuration(status, request)
                minDurationParam = durationParams[0]
                maxDurationParam = durationParams[1]
                
                if(status["type"] in type and job["processID"] in processes and status["status"] in stati and datetimeParam == True and minDurationParam == True and maxDurationParam == True):
                    job = {"jobID": status["jobID"],
                           "processID": job["processID"],
                           "type": status["type"],
                           "status": status["status"],
                           "message": status["message"],
                           "created": status["created"],
                           "links": [{
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
                    jobArray.append(job)
                    count += 1
                if count == int(limit):
                    break
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
            response.headers['link'] = "localhost:5000/jobs?f=application/json"
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
                    response.headers['link'] = "localhost:5000/jobs/" + str(jobID) + "?f=application/json"
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
                    response = render_template("html/Job.html", job=job)
                    return response, 200, {"link": "localhost:5000/jobs/" + str(jobID) + "?f=text/html"} #return response and ok
                except:
                    return "HTTP status code 500: internal server error", 500 #internal server error
            else:
                return "HTTP status code 404: not found", 404 #not found
        else:
            return "HTTP status code 406: not acceptable", 406 #not acceptable
        
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
                        file = open('jobs/' + str(jobID) + '/status.json') #open status.json
                        data = json.load(file) #create response   
                        file.close() #close status.json
                        
                        response = jsonify(data)
                        response.headers['link'] = "localhost:5000/jobs/" + str(jobID) + "?f=application/json"
                        response.status_code = 200
                        return  response #return response and ok
                    else:
                        return "HTTP Status Code 200: ok", 200
            else:
                return "HTTP status code 404: not found", 404 #not found
        except:
            return "HTTP status code 500: internal server error", 500 #internal server error

@app.route('/jobs/<jobID>/results', methods = ["GET"])
def getResults(jobID):
    if(os.path.exists('jobs/' + str(jobID))):
        try:
            file = open('jobs/' + str(jobID) + "/status.json",)
            status = json.load(file)
            file.close() 
            file = open('jobs/' + str(jobID) + "/job.json",)
            job = json.load(file)
            file.close() 
            
            if(job["processID"] == "Echo"):
                if(status["status"] == "successful"):
                    return send_file('jobs/' + str(jobID) + '/results/result.json', mimetype='application/json'), 200
                else:
                    return "HTTP status code 404: not found - Result not ready", 404 #not found
        except:
            return "HTTP status code 500: internal server error", 500 #internal server error
    else:
        return "HTTP status code 404: not found - No such job", 404 #not found

         
#run application
app.run(debug=True, use_reloader=False) 