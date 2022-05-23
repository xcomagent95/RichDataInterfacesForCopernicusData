import pycurl
import unittest
from io import BytesIO

class TestStringMethods(unittest.TestCase):
      
    def setUp(self):
        pass
     
    #Test Landing Page "/"
    #Abstract Test A.1
    def test_a1(self):        
        self.assertEqual( 'a'*4, 'aaaa')
    #Abstract Test A.2
    def test_a2(self):        
        self.assertEqual( 'a'*4, 'aaaa')
        
    #Test Conformance "/conformance"
    #Abstract Test A.5
    def test_a5(self):        
        self.assertEqual( 'a'*4, 'aaaa')
    #Abstract Test A.6
    def test_a6(self):        
        self.assertEqual( 'a'*4, 'aaaa')

        
        
    
if __name__ == '__main__':
    unittest.main()