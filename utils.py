# -*- coding: utf-8 -*-
import time
import json
from shutil import make_archive
from zipfile import ZipFile
import os
import datetime
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, products

class job:
    def __init__(self, id, process, job_path, results_path, downloads_path, input):
        self.id = id #unique id for the job
        self.process = process #process the job is running
        self.path = job_path
        self.results = results_path #path for processing results
        self.downloads = downloads_path #path for downloaded files
        self.input = input

def readJob(jobFile):
    with open(jobFile, "r") as f: #open job file
        data = json.load(f) #read job file 
        
    jobObject = job(data["jobID"], data["processID"], data["path"], data["results"], data["downloads"], data["input"]) #create job object
        
    return jobObject #return job object

def floodMonitoringProcess(job):
    footprint ={"type": "FeatureCollection","features": [{
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                            "coordinates": [[
                                [float(job.input[4]),float(job.input[5])],
                                [float(job.input[6]),float(job.input[5])],
                                [float(job.input[6]),float(job.input[7])],
                                [float(job.input[4]),float(job.input[7])],
                                [float(job.input[4]),float(job.input[5])]
                            ]]}}]}
    json.dumps(footprint, indent=4)
    with open(job.path + "/footprint.geojson", 'w') as f:
        json.dump(footprint, f)
        f.close()

def echoProcess(job):
    if(checkForDismissal(job.path + '/status.json') == True):
        return
    
    setStarted(job.path + '/status.json')
    
    try:
        input = job.input[0]
        time.sleep(5)
    except:
        updateStatus(job.path + '/status.json', "failed", "The job has failed", "-")
    
    if(checkForDismissal(job.path + '/status.json') == True):
        return
    
    result ={"result": input,
             "message": "This is an echo"}
    json.dumps(result, indent=4)
    with open(job.results + "result.json", 'w') as f: #create file
        json.dump(result, f) #write content
        f.close() #close file
    updateStatus(job.path + '/status.json', "successful", "Step 1 of 1 completed", "100")
    setFinished(job.path + '/status.json')

def checkForDismissal(path):
    with open(path, "r") as f:
                data = json.load(f)
                if(data["status"] == "dismissed"):
                    f.close()
                    return True
                else:
                    return False
                
def updateStatus(path, status, message, percentage):
    with open(path, "r") as f:
            data = json.load(f)
            data["status"] = status
            data["message"] = message
            data["progress"] = percentage
            f.close()
            with open(path, "w") as f:
                json.dump(data, f) 

def setStarted(path):
    with open(path, "r") as f:
            data = json.load(f)
            data["started"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.close()
            with open(path, "w") as f:
                json.dump(data, f) 

def setFinished(path):
    with open(path, "r") as f:
            data = json.load(f)
            data["finished"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.close()
            with open(path, "w") as f:
                json.dump(data, f) 
                
def zipResults(job):
    file = job.path + "/results"  # zip file name
    directory = job.results
    make_archive(file, "zip", directory)  # zipping the directory
    
def convertRFC3339ToDatetime(datetimeString):
    r1 = datetimeString.replace('"', '') 
    r2 = r1.replace('T', ' ') 
    date = datetime.datetime.strptime(r2, "%Y-%m-%d %H:%M:%S")
    return date

def checkCreationDate(creationDate, request):
    datetimeParam = False
    if(request.args.get('datetime') == None):
        datetimeParam = True
    elif(request.args.get('datetime').startswith('[')):
        lowerBound = request.args.get('datetime')[9:]
        lowerDate = convertRFC3339ToDatetime(lowerBound)
        if(creationDate < lowerDate):
            datetimeParam = True
    elif(request.args.get('datetime').endswith(']')):
        upperBound = request.args.get('datetime')[0:29]
        upperDate = convertRFC3339ToDatetime(upperBound)
        if(creationDate > upperDate):
            datetimeParam = True
    else:
        upperBound = request.args.get('datetime')[0:29]
        upperDate = convertRFC3339ToDatetime(upperBound)
        lowerBound = request.args.get('datetime')[32:]
        lowerDate = convertRFC3339ToDatetime(lowerBound)
        if(creationDate < lowerDate and creationDate > upperDate):
            datetimeParam = True
    return datetimeParam

def checkDuration(status, request):
    if(status["started"] != "none" and (request.args.get('minDuration') != None or request.args.get('maxDuration') != None)):
        now = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        started = datetime.datetime.strptime(str(status["started"]), "%Y-%m-%d %H:%M:%S")
        duration = now - started
        duration_in_s = duration.total_seconds()
        print(duration_in_s)
        if(request.args.get('minDuration') != None and request.args.get('maxDuration') == None):
            minDuration = int(request.args.get('minDuration')[1:-1])
            if(duration_in_s > minDuration):
                minDurationParam = True
            else:
                minDurationParam = False
            maxDurationParam = True
                        
        elif(request.args.get('minDuration') == None and request.args.get('maxDuration') != None):
            maxDuration = int(request.args.get('maxDuration')[1:-1])
            if(duration_in_s < maxDuration):
                maxDurationParam = True
            else:
                maxDurationParam = False
            minDurationParam = True
                        
        else:
            minDuration = int(request.args.get('minDuration')[1:-1])
            maxDuration = int(request.args.get('maxDuration')[1:-1])
            if(duration_in_s < maxDuration and duration_in_s > minDuration):
                minDurationParam = True
                maxDurationParam = True
            else:
                minDurationParam = False
                maxDurationParam = False
    elif(status["started"] == "none" and (request.args.get('minDuration') != None or request.args.get('maxDuration') != None)):
        minDurationParam = False
        maxDurationParam = False
    else:
        minDurationParam = True
        maxDurationParam = True
    
    return [minDurationParam, maxDurationParam]

def parseInput(processID, data):
    responseType = None
    #set response Type
    if("response" in data):
        if(data["response"] not in ["document", "raw"]):
            responseType = "raw"
        else:
            responseType = data["response"]
            
    if(processID == "Echo"):
        inputs = [data["inputs"]["inputValue"]]
        #outputs = [data["outputs"]["complexObjectOutput"]]
        response = [inputs, responseType]
        
        #check transmission mode
        file = open('templates/json/processes/' + processID + 'ProcessDescription.json',) #open ProcessDescription.json
        process = json.load(file) #create response   
        file.close() #close ProcessDescription.json
        
        if("response" in data):
            if(data["outputs"]["complexObjectOutput"]["transmissionMode"] not in process["outputTransmission"]):
                response = False

        if("format" in data["outputs"]["complexObjectOutput"]):
            if(data["outputs"]["complexObjectOutput"]["format"]["mediaType"] != process["outputs"]["complexObjectOutput"]["schema"]["contentMediaType"]):
                response = False
            else:
                response.append(data["outputs"]["complexObjectOutput"]["format"]["mediaType"])
        else:
            response.append(process["outputs"]["complexObjectOutput"]["schema"]["contentMediaType"])
            
    if(processID == "FloodMonitoring"):
        inputs = [data["inputs"]["preDate"],
                  data["inputs"]["postDate"],
                  data["inputs"]["username"],
                  data["inputs"]["password"],
                  data["inputs"]["ulx"],
                  data["inputs"]["uly"],
                  data["inputs"]["lrx"],
                  data["inputs"]["lry"]]
        
        #outputs = [data["outputs"]["complexObjectOutput"]]
        response = [inputs, responseType]
        
        #check transmission mode
        file = open('templates/json/processes/' + processID + 'ProcessDescription.json',) #open ProcessDescription.json
        process = json.load(file) #create response   
        file.close() #close ProcessDescription.json
        
        if("response" in data):
            if(data["outputs"]["complexObjectOutput"]["transmissionMode"] not in process["outputTransmission"]):
                response = False

        if("format" in data["outputs"]["complexObjectOutput"]):
            if(data["outputs"]["complexObjectOutput"]["format"]["mediaType"] != process["outputs"]["complexObjectOutput"]["schema"]["contentMediaType"]):
                response = False
            else:
                response.append(data["outputs"]["complexObjectOutput"]["format"]["mediaType"])
        else:
            response.append(process["outputs"]["complexObjectOutput"]["schema"]["contentMediaType"])
                
                    
    return response