import unittest
from io import BytesIO
import requests
import logging
import subprocess

logging.basicConfig(filename = 'testSuitLog.log', 
                    level=logging.INFO, 
                    format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


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
    #Abstract Test A.5
    def test_a3(self):   
        logging.info("--> abstract test a3 started")  
        request = requests.get('http://localhost:5000/api?f=application/json')
        resource = request.headers["resource"]
        self.assertEqual(resource, 'api')
        
        request = requests.get('http://localhost:5000/api?f=text/html')
        resource = request.headers["resource"]
        self.assertEqual(resource, 'api')
        logging.info("--> abstract test a3 passed")
        
    #Abstract Test A.6
    def test_a4(self):     
        logging.info("--> abstract test a4 started")   
        request = requests.get('http://localhost:5000/?f=application/json')
        status_code = request.status_code
        self.assertEqual(status_code, 200)
        
        request = requests.get('http://localhost:5000/?f=text/html')
        status_code = request.status_code
        self.assertEqual(status_code, 200)
        logging.info("--> abstract test a4 passed")   
        
    #Test "/conformance"
        
        
    
if __name__ == '__main__':
    unittest.main()
    