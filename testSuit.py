import unittest
from io import BytesIO
import requests
import logging
import subprocess
import json
from werkzeug.serving import WSGIRequestHandler

logging.basicConfig(filename = 'testSuitLog.log', 
                    level=logging.INFO, 
                    format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

api = subprocess.Popen(['python', 'api.py']) #start the api in a subprocess
print("API running...")

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        pass
    logging.info("------------------> new test run <------------------")  
    #Test "/"
    #Abstract Test A.1
    def test_a1(self):  
        logging.info("--> abstract test a1 started")  
        request = requests.get('http://localhost:5000/?f=application/json')
        resource = request.headers["resource"]
        self.assertEqual(resource, 'landingPage')
        
        request = requests.get('http://localhost:5000/?f=text/html')
        resource = request.headers["resource"]
        self.assertEqual(resource, 'landingPage')
        logging.info("--> abstract test a1 passed")  
        
    #Abstract Test A.2
    def test_a2(self): 
        logging.info("--> abstract test a2 started")  
        request = requests.get('http://localhost:5000/?f=application/json')
        status_code = request.status_code
        content_type = request.headers["Content-Type"]
        self.assertEqual(status_code, 200)
        self.assertEqual(content_type, "application/json")
        
        request = requests.get('http://localhost:5000/?f=text/html')
        status_code = request.status_code
        content_type = request.headers["Content-Type"]
        self.assertEqual(status_code, 200)
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        logging.info("--> abstract test a2 passed")
        
    #Test "/api"
    #Abstract Test A.3
    def test_a3(self):   
        logging.info("--> abstract test a3 started")  
        request = requests.get('http://localhost:5000/api?f=application/json')
        resource = request.headers["resource"]
        self.assertEqual(resource, 'api')
        
        request = requests.get('http://localhost:5000/api?f=text/html')
        resource = request.headers["resource"]
        self.assertEqual(resource, 'api')
        logging.info("--> abstract test a3 passed")
        
    #Abstract Test A.4
    def test_a4(self):     
        logging.info("--> abstract test a4 started")   
        request = requests.get('http://localhost:5000/api?f=application/json')
        status_code = request.status_code
        self.assertEqual(status_code, 200)
        
        request = requests.get('http://localhost:5000/api?f=text/html')
        status_code = request.status_code
        self.assertEqual(status_code, 200)
        logging.info("--> abstract test a4 passed")   
        
    #Test "/conformance"
    #Abstract Test A.6
    def test_a6(self):   
        logging.info("--> abstract test a5 started")   
        request = requests.get('http://localhost:5000/conformance?f=application/json')
        status_code = request.status_code
        self.assertEqual(status_code, 200)
        
        request = requests.get('http://localhost:5000/conformance?f=text/html')
        status_code = request.status_code
        self.assertEqual(status_code, 200)
        logging.info("--> abstract test a5 passed")
    
    #Abstract Test A.7
    def test_a7(self):   
        logging.info("--> abstract test a7 started")   
        response = requests.get("http://localhost:5000/?f=application/json")
        self.assertEqual(response.raw.version, 11)
        
        response = requests.get("http://localhost:5000/conformance?f=application/json")
        self.assertEqual(response.raw.version, 11)
        
        response = requests.get("http://localhost:5000/api?f=application/json")
        self.assertEqual(response.raw.version, 11)
        logging.info("--> abstract test a7 passed") 
        
        response = requests.get("http://localhost:5000/processes?f=application/json")
        self.assertEqual(response.raw.version, 11)
        
        response = requests.get("http://localhost:5000/jobs?f=application/json")
        self.assertEqual(response.raw.version, 11)
        
        response = requests.get("http://localhost:5000/jobs/test?f=application/json")
        self.assertEqual(response.raw.version, 11)
        
        response = requests.get("http://localhost:5000/processes/Echo?f=application/json")
        self.assertEqual(response.raw.version, 11)
        logging.info("--> abstract test a7 passed")   
    
    #Test "/processList"    
    #Abstract Test A.8 & A.10
    def test_a10(self):   
        logging.info("--> abstract test a8 & a10 started")   
        request = requests.get('http://localhost:5000/processes?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        self.assertEqual(resource, 'processes')
        self.assertEqual(status_code, 200)
        
        request = requests.get('http://localhost:5000/processes?f=text/html')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        self.assertEqual(resource, 'processes')
        self.assertEqual(status_code, 200)
        logging.info("--> abstract test a8 & a10 passed") 
 
    #Abstract Test A.9 & A.12
    def test_a12(self):   
        logging.info("--> abstract test a9 & a12 started")   
        
        #Test Echo process
        request = requests.get('http://localhost:5000/processes?f=application/json&limit=1')
        limit = len(request.json()["processes"])
        self.assertEqual(limit, 1)
        
        request = requests.get('http://localhost:5000/processes?f=application/json&limit=-1')
        limit = len(request.json()["processes"])
        self.assertEqual(True, limit >= 0 and limit <= 10)
        
        request = requests.get('http://localhost:5000/processes?f=application/json&limit=-1')
        limit = len(request.json()["processes"])
        self.assertEqual(True, limit <= 1000 and limit <= 10)
        logging.info("--> abstract test a9 & a12 passed")  
  
    #Abstract Test A.13 & A.14
    def test_a13_14(self):   
        logging.info("--> abstract test a13 & a14 started")   
        
        #Test Echo process
        request = requests.get('http://localhost:5000/processes/Echo?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        self.assertEqual(resource, 'Echo')
        self.assertEqual(status_code, 200)
        
        request = requests.get('http://localhost:5000/processes/Echo?f=text/html')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        self.assertEqual(resource, 'Echo')
        self.assertEqual(status_code, 200)
        logging.info("--> abstract test a13 & a14 passed")  
    
    #Abstract Test A.15
    def test_a15(self):
        logging.info("--> abstract test a15 started")  
        request = requests.get('http://localhost:5000/processes/nonexistentProcess?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        self.assertEqual(resource, 'no-such-process')
        self.assertEqual(status_code, 404)
        
        request = requests.get('http://localhost:5000/processes/nonexistentProcess?f=text/html')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        self.assertEqual(resource, 'no-such-process')
        self.assertEqual(status_code, 404)
        logging.info("--> abstract test a15 passed")
     
    #Abstract Test A.34
    def test_a34(self):
        logging.info("--> abstract test a34 started")  
        request = requests.post('http://localhost:5000/processes/Echo/execution', json={'inputs':{'inputValue':'test'}, 'outputs':{'complexObjectOutput': {'format': {'mediaType': 'application/json'}, 'transmissionMode': 'value'}}, 'response': 'document'})
        status_code = request.status_code
        self.assertEqual(status_code, 201)
        logging.info("--> abstract test a34 passed")        
        
    #Abstract Test A.35 & A.36
    def test_a35_36(self):
        logging.info("--> abstract test a35 & a36 started")  
        request = requests.get('http://localhost:5000/jobs/test?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        self.assertEqual(resource, 'job')
        self.assertEqual(status_code, 200)
        
        request = requests.get('http://localhost:5000/jobs/test?f=text/html')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        self.assertEqual(resource, 'job')
        self.assertEqual(status_code, 200)
        logging.info("--> abstract test a35 & a36 passed")
        
    #Abstract Test A.37
    def test_a37(self):
        logging.info("--> abstract test a37 started")  
        request = requests.get('http://localhost:5000/jobs/nonexistentJob?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        self.assertEqual(resource, 'no-such-job')
        self.assertEqual(status_code, 404)
        
        request = requests.get('http://localhost:5000/jobs/nonexistentJob?f=text/html')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        self.assertEqual(resource, 'no-such-job')
        self.assertEqual(status_code, 404)
        logging.info("--> abstract test a37 passed")
        
    #Abstract Test A.38
    def test_a38(self):
        logging.info("--> abstract test a38 started")  
        request = requests.get('http://localhost:5000/jobs/test/results?f=application/json')
        status_code = request.status_code
        self.assertEqual(status_code, 200)
        logging.info("--> abstract test a38 passed")
        
    #Abstract Test A.45
    def test_a45(self):
        logging.info("--> abstract test a38 started")  
        request = requests.get('http://localhost:5000/jobs/nonexistentJob/results?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        self.assertEqual(resource, 'no-such-job')
        self.assertEqual(status_code, 404)
        logging.info("--> abstract test a45 passed")
    
    #Abstract Test A.46
    def test_a46(self):
        logging.info("--> abstract test a46 started")  
        request = requests.get('http://localhost:5000/jobs/testNotReady/results?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        self.assertEqual(resource, 'results-not-ready')
        self.assertEqual(status_code, 404)
        logging.info("--> abstract test a46 passed")
        
    #Abstract Test A.47
    def test_a47(self):
        logging.info("--> abstract test a47 started")  
        request = requests.get('http://localhost:5000/jobs/testFailed/results?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        self.assertEqual(resource, 'job-failed')
        self.assertEqual(status_code, 404)
        logging.info("--> abstract test a47 passed")
        
    #Abstract Test A.55
    def test_a55(self):
        logging.info("--> abstract test a55 started") 
        
        request = requests.get('http://localhost:5000/?f=application/json')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        
        request = requests.get('http://localhost:5000/api?f=application/json')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        
        request = requests.get('http://localhost:5000/conformance?f=application/json')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        
        request = requests.get('http://localhost:5000/processes?f=application/json')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        
        request = requests.get('http://localhost:5000/processes/Echo?f=application/json')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        
        request = requests.get('http://localhost:5000/jobs?f=application/json')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        
        request = requests.get('http://localhost:5000/jobs/test?f=application/json')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        
        logging.info("--> abstract test a55 passed")  
        
    #Abstract Test A.57
    def test_a57(self):
        logging.info("--> abstract test a57 started") 
        
        request = requests.get('http://localhost:5000/?f=text/html')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        request = requests.get('http://localhost:5000/api?f=text/html')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        request = requests.get('http://localhost:5000/conformance?f=text/html')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        request = requests.get('http://localhost:5000/processes?f=text/html')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        request = requests.get('http://localhost:5000/processes/Echo?f=text/html')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        request = requests.get('http://localhost:5000/jobs?f=text/html')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        request = requests.get('http://localhost:5000/jobs/test?f=text/html')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        logging.info("--> abstract test a57 passed")   
        
    #Abstract Test A.60
    def test_a60(self):
        logging.info("--> abstract test a60 started") 
        
        request = requests.get('http://localhost:5000/api?f=text/html')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "text/html; charset=utf-8")
        
        request = requests.get('http://localhost:5000/api?f=application/json')
        content_type = request.headers["Content-Type"]
        self.assertEqual(content_type, "application/json")
        
        
        logging.info("--> abstract test a60 passed")   
    
    #Abstract Test A.70 & A79
    def test_a70_a79(self):   
        logging.info("--> abstract test a70 & a79 started")   
        
        #Test Echo process
        request = requests.get('http://localhost:5000/jobs?f=application/json&limit=1')
        limit = len(request.json()["jobs"])
        self.assertEqual(limit, 1)
        
        request = requests.get('http://localhost:5000/jobs?f=application/json&limit=-1')
        limit = len(request.json()["jobs"])
        self.assertEqual(True, limit >= 0 and limit <= 10)
        
        request = requests.get('http://localhost:5000/jobs?f=application/json&limit=-1')
        limit = len(request.json()["jobs"])
        self.assertEqual(True, limit <= 1000 and limit <= 10)
        logging.info("--> abstract test a70 & a79 passed") 
        
    #Abstract Test A.64 & A.71
    def test_a64_a71(self):   
        logging.info("--> abstract test a64 & a71 started")   
        
        request = requests.get('http://localhost:5000/jobs?f=application/json')
        status_code = request.status_code
        resource = request.headers["resource"]
        self.assertEqual(status_code, 200)
        self.assertEqual(resource, "jobs")
        
        request = requests.get('http://localhost:5000/jobs?f=text/html')
        status_code = request.status_code
        resource = request.headers["resource"]
        self.assertEqual(status_code, 200)
        self.assertEqual(resource, "jobs")
        
        logging.info("--> abstract test a64 & a71 passed") 
    
    #Abstract Test A.65 & A.73
    def test_a65_a73(self):
        logging.info("--> abstract test a65 & a73 started")   
        type_validation = True
        requested_type = "process"
        request = requests.get('http://localhost:5000/jobs?f=application/json&type=' + requested_type).json()
        jobs = request["jobs"]
        print()
        for i in jobs:
            if(requested_type != i["type"]):
                type_validation = False
        
        self.assertEqual(type_validation, True)
        
        
        logging.info("--> abstract test a65 & a73 passed") 
        
    #Abstract Test A.66 & A.74 & A.75
    def test_a66_a74_a75(self):
        logging.info("--> abstract test a66 & a74 & a75 started")   
        type_validation = True
        requested_process = "Echo"
        request = requests.get('http://localhost:5000/jobs?f=application/json&processID=' + requested_process).json()
        jobs = request["jobs"]
        print()
        for i in jobs:
            if(requested_process != i["processID"]):
                type_validation = False
        
        self.assertEqual(type_validation, True)
        
        
        logging.info("--> abstract test a66 & a74 & a75 passed") 
        
    #Abstract Test A.67 & A.76
    def test_a67_a76(self):
        logging.info("--> abstract test a67 & a76 started")   
        type_validation = True
        requested_status = "created"
        request = requests.get('http://localhost:5000/jobs?f=application/json&status=' + requested_status).json()
        jobs = request["jobs"]
        print()
        for i in jobs:
            if(requested_status != i["status"]):
                type_validation = False
        
        self.assertEqual(type_validation, True)
        
        
        logging.info("--> abstract test a67 & a76 passed")
        
    #Abstract Test A.81 & A.82
    def test_a81_82(self):
        with open('jobs/testDismissed/status.json', "r") as f:
                data = json.load(f)
                data["status"] = "created"
                f.close()
                with open('jobs/testDismissed/status.json', "w") as f:
                    json.dump(data, f) 
        
        
        logging.info("--> abstract test a81 & a82 started")  
        request = requests.delete('http://localhost:5000/jobs/testDismissed')
        status_code = request.status_code
        resource = request.headers["resource"]
        self.assertEqual(resource, 'job-dismissed')
        self.assertEqual(status_code, 200)
        logging.info("--> abstract test a81 & a82 passed")    
    
if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    unittest.main()
    