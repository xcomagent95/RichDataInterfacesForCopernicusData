# -*- coding: utf-8 -*-
#imports
import subprocess

#create api subprocess
api = subprocess.Popen(['python', 'api.py']) #start the api in a subprocess
print("API running...")

#create processing subprocess
processingChain = subprocess.Popen(['python', 'processing.py']) #start the processing queue in a subprocess
print("Processing running...")