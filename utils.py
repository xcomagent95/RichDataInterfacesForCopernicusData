import time
import json

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
    
    input = job.input[0]
    time.sleep(30)
    
    if(checkForDismissal(job.path + '/status.json') == True):
        return
    
    result ={"result": input,
             "message": "This is an echo"}
    json.dumps(result, indent=4)
    with open(job.results + "result.json", 'w') as f: #create file
        json.dump(result, f) #write content
        f.close() #close file
            
    updateStatus(job.path + '/status.json', "successful", "Step 1 of 1 completed", "100")

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
            data["message"] = message
            data["progress"] = percentage
            f.close()
            with open(path, "w") as f:
                json.dump(data, f)    
    