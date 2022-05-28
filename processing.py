# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 10:28:07 2022

@author: Alexander
"""
import os
import json
import time
import utils

def processingChain():
    jobs = os.listdir('jobs/')
    
    
    processing_list = []
    for i in jobs:
        job = os.listdir('jobs/' + i)
        file = open('jobs/' + i + '/status.json')
        response = json.load(file)
        if(response["status"] == 'accepted'):
            processing_list.append((response["jobID"], response["created"]))
        file.close()
    processing_list.sort(key = lambda x: x[1])

    if(len(processing_list) > 0):
        oldest_job = processing_list[0][0]
        print('oldest job-id: ' + oldest_job)
        
        with open('jobs/' + oldest_job + '/status.json', "r") as f:
            data = json.load(f)
            data["status"] = "running"
            f.close()
            with open('jobs/' + oldest_job + '/status.json', "w") as f:
                json.dump(data, f)
            f.close()
        
        with open('jobs/' + oldest_job + '/job.json', "r") as f:
            data = json.load(f)
        
        if(data["processID"] == 'Echo'):
           job = utils.readJob('jobs/' + oldest_job + '/job.json')
           utils.echoProcess(job)
        processingChain()

while(True):           
    processingChain() 
    time.sleep(300)
