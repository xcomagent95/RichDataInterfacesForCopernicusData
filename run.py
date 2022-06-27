# -*- coding: utf-8 -*-
#imports
import subprocess

#create api subprocess
api = subprocess.Popen(['python', 'api.py']) #start the api in a subprocess
print("API running...")

#create processing subprocess
processing = subprocess.Popen(['python', 'processing.py']) #start the processing queue in a subprocess
print("Processing running...")

#create test suite subprocess
#test = subprocess.Popen(['python', 'testSuit.py']) #start the test suit
#print("Test suit running running...")

#killSwitch = input("Enter 'k' to stop the API or 'r' to restart the API:")
#if(killSwitch == 'k'):
#    api.kill()
#    processing.kill()
#elif(killSwitch == 'r'):
#    api.kill()
#    processing.kill()
#    api = subprocess.Popen(['python', 'api.py']) #start the api in a subprocess
#    print("API running...")
#    processing = subprocess.Popen(['python', 'processing.py']) #start the processing queue in a subprocess
#    print("Processing running...")
