# -*- coding: utf-8 -*-
import os
import json
import time
import utils
import logging

def processingChain():
    logging.info("--> checking jobs")
    jobs = os.listdir('jobs/') #list all created jobs
    processing_list = [] #initialize processing list
    
    for i in jobs: #iterate over created jobs
        job = os.listdir('jobs/' + i) #list items in job directory
        file = open('jobs/' + i + '/status.json') #read status.json
        data = json.load(file) #load data from .json
        file.close() #close file
        
        if(data["status"] == 'accepted'): #check is status is accepted
            processing_list.append((data["jobID"], data["created"])) #append jobID and created timestamp
    processing_list.sort(key = lambda x: x[1]) #sort processing list by created timestamp

    if(len(processing_list) > 0): #check if there are unprocesses jobs
        oldest_job = processing_list[0][0] #retrieve the oldest job
        logging.info("--> running job: " + oldest_job)        
        utils.updateStatus("jobs/" + oldest_job + '/status.json', "running", "the job has been started", "0")
        
        with open('jobs/' + oldest_job + '/job.json', "r") as f: #load job.json
            data = json.load(f) #load data from .json
        
        if(data["processID"] == 'Echo'): #if job is running an Echo process
           job = utils.readJob('jobs/' + oldest_job + '/job.json') #create job object
           utils.echoProcess(job) #run echo process
           
        if(data["processID"] == 'FloodMonitoring'):
            job = utils.readJob('jobs/' + oldest_job + '/job.json') #create job object
            utils.floodMonitoringProcess(job) #run flood monitoring process
        logging.info("--> finished job: " + oldest_job)   
        processingChain() #restart processing chain

while(True): #run           
    processingChain() #processing chain
    time.sleep(30) #every five minutes
