import unittest
from io import BytesIO
import requests
import logging
import subprocess

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
    
    #Test "/processList"
    #Abstract Test A.10
    def test_a10(self):   
        logging.info("--> abstract test a10 started")   
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
        logging.info("--> abstract test a10 passed")   
        
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
    
if __name__ == '__main__':
    unittest.main()
    