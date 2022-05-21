# -*- coding: utf-8 -*-
#imports
import subprocess

#create api subprocess
api = subprocess.Popen(['python', 'api.py'])

#create processing subprocess
processingChain = subprocess.Popen(['python', 'processing.py'])

print("API running...")