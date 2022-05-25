import time
import json
from shutil import make_archive
from zipfile import ZipFile
import os
import datetime

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

def echoProcess(job):
    if(checkForDismissal(job.path + '/status.json') == True):
        return
    
    setStarted(job.path + '/status.json')
    
    input = job.input[0]
    time.sleep(10)
    
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