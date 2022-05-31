# -*- coding: utf-8 -*-
#imports
import subprocess

#create api subprocess
api = subprocess.Popen(['python', 'api.py']) #start the api in a subprocess
print("API running...")

#create processing subprocess
processingChain = subprocess.Popen(['python', 'processing.py']) #start the processing queue in a subprocess
print("Processing running...")

#create test suite subprocess

testSuite = subprocess.Popen(['python', 'testSuit.py']) #start the test suit
print("Test suit running running...")