# -*- coding: utf-8 -*-
import time
import json
from shutil import make_archive
from zipfile import ZipFile
import os
import datetime
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, products

import sys
sys.path.append('C:\\Users\\Alexander\\.snap\\snap-python')
import snappy
from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF

from osgeo import gdal, ogr, osr
from gdalconst import GA_ReadOnly

#from scipy import ndimage
#import matplotlib.pyplot as plt
from skimage.filters import threshold_isodata
from skimage.filters import threshold_yen
from skimage.filters import threshold_otsu
import datetime
from skimage import io
import traceback

import numpy as np
import xml.etree.cElementTree as et
import math

import base64

import zipfile

import shutil

class job:
    def __init__(self, id, process, job_path, results_path, downloads_path, input):
        self.id = id #unique id for the job
        self.process = process #process the job is running
        self.path = job_path
        self.results = results_path #path for processing results
        self.downloads = downloads_path #path for downloaded files
        self.input = input

def readJob(jobFile):
    with open(jobFile, "r") as f: #open job file
        data = json.load(f) #read job file 
        
    jobObject = job(data["jobID"], data["processID"], data["path"], data["results"], data["downloads"], data["input"]) #create job object
        
    return jobObject #return job object

def floodMonitoringProcess(job):
	try:
		setStarted(job.path + '/status.json')
		datasets = datasets = os.listdir("data/")
		if(checkForDismissal(job.path + '/status.json') == True):
			return
		
		footprint ={"type": "FeatureCollection","features": [{
						"type": "Feature",
						"properties": {},
						"geometry": {
							"type": "Polygon",
								"coordinates": [[
									[float(job.input[4]),float(job.input[5])],
									[float(job.input[6]),float(job.input[5])],
									[float(job.input[6]),float(job.input[7])],
									[float(job.input[4]),float(job.input[7])],
									[float(job.input[4]),float(job.input[5])]
								]]}}]}
		json.dumps(footprint, indent=4)
		with open(job.path + "/footprint.geojson", 'w') as f:
			json.dump(footprint, f)
			f.close()
			
		updateStatus(job.path + '/status.json', "running", "Step 1 of 10 completed", "10")

		pre_date_t0 = datetime.date(int(job.input[0][0:4]), int(job.input[0][4:6]), int(job.input[0][6:]))
		pre_date_t1 = pre_date_t0 + datetime.timedelta(days=1)
		post_date_t0 = datetime.date(int(job.input[1][0:4]), int(job.input[1][4:6]), int(job.input[1][6:]))
		post_date_t1 = post_date_t0 + datetime.timedelta(days=1)
		 
		updateStatus(job.path + '/status.json', "running", "Step 2 of 10 completed", "20")
		
		if(checkForDismissal(job.path + '/status.json') == True):
			return
		
		try:
			api = loginCopernicusHub(job)
			updateStatus(job.path + '/status.json', "running", "Step 3 of 10 completed", "30")
		except:
			updateStatus(job.path + '/status.json', "failed", "Login to Copernicus Hub was not successful", "0")
			return
			
		if(checkForDismissal(job.path + '/status.json') == True):
			return
		
		try:
			pre_product = getProduct(api, job, pre_date_t0, pre_date_t1)
		except:
			updateStatus(job.path + '/status.json', "failed", "Pre-Dataset could not be found", "0")
			return
		
		if(pre_product[1] + ".zip" not in datasets):
			retrievalStatus = retrieveProduct(api, pre_product[0], pre_product[1], job.downloads)
			if(retrievalStatus == True):
				updateStatus(job.path + '/status.json', "running", "Step 4 of 10 completed", "40")
			else:
				updateStatus(job.path + '/status.json', "failed", "Pre-Dataset is stored in long term storage", "0")
				return
		
		try:
			calibrateProductSNAP(pre_product[1], job)
		except:
			updateStatus(job.path + '/status.json', "failed", "Pre-Dataset could not be calibrated", "0")
			return
			
		updateStatus(job.path + '/status.json', "running", "Step 5 of 10 completed", "50")
		
		if(checkForDismissal(job.path + '/status.json') == True):
			return
		
		try:
			post_product = getProduct(api, job, post_date_t0, post_date_t1)
		except:
			updateStatus(job.path + '/status.json', "failed", "Post-Dataset could not be found", "0")
			return
		
		if(post_product[1] + ".zip" not in datasets):
			retrievalStatus = retrieveProduct(api, post_product[0], post_product[1], job.downloads)
			if(retrievalStatus == True):
				updateStatus(job.path + '/status.json', "running", "Step 6 of 10 completed", "40")
			else:
				updateStatus(job.path + '/status.json', "failed", "Post-Dataset is stored in long term storage", "0")
				return
		
		try:
			calibrateProductSNAP(post_product[1], job)
		except:
			updateStatus(job.path + '/status.json', "failed", "Pre-Dataset could not be calibrated", "0")
			return
			
		updateStatus(job.path + '/status.json', "running", "Step 7 of 10 completed", "70")
			
		if(checkForDismissal(job.path + '/status.json') == True):
			return
		
		try:
			ndsiSNAP(job, pre_product[1], post_product[1])
		except:
			updateStatus(job.path + '/status.json', "failed", "NDSI could not be calculated", "0")
			return
		
		updateStatus(job.path + '/status.json', "running", "Step 8 of 10 completed", "80")
		
		try:
			clipProductSNAP(job)
		except:
			updateStatus(job.path + '/status.json', "failed", "NDSI could not be clipped", "0")
			return
		updateStatus(job.path + '/status.json', "running", "Step 9 of 10 completed", "90")
		
		try:
			theresholdSNAP(job)
		except:
			updateStatus(job.path + '/status.json', "failed", "Threshold could not be calculated", "0")
			return
		
		updateStatus(job.path + '/status.json', "running", "Step 10 of 10 completed", "100")
		setFinished(job.path + '/status.json')
	except:
		updateStatus(job.path + '/status.json', "failed", "The job has failed", "-")
		return
def echoProcess(job):
    try:
        if(checkForDismissal(job.path + '/status.json') == True):
            return
		
        setStarted(job.path + '/status.json')
		
		
        input = job.input[0]
        time.sleep(5)
		
		
        if(checkForDismissal(job.path + '/status.json') == True):
            return
		
        result ={"result": input,
				 "message": "This is an echo"}
        json.dumps(result, indent=4)
        with open(job.results + "result.json", 'w') as f: #create file
            json.dump(result, f) #write content
            f.close() #close file
        updateStatus(job.path + '/status.json', "successful", "Step 1 of 1 completed", "100")
        setFinished(job.path + '/status.json')
    except:
        updateStatus(job.path + '/status.json', "failed", "The job has failed", "-")
        return

def checkForDismissal(path):
    with open(path, "r") as f:
                data = json.load(f)
                if(data["status"] == "dismissed"):
                    f.close()
                    return True
                else:
                    return False
                
def updateStatus(path, status, message, percentage):
    with open(path, "r") as f:
            data = json.load(f)
            data["status"] = status
            data["message"] = message
            data["progress"] = percentage
            f.close()
            with open(path, "w") as f:
                json.dump(data, f) 

def setStarted(path):
    with open(path, "r") as f:
            data = json.load(f)
            data["started"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.close()
            with open(path, "w") as f:
                json.dump(data, f) 

def setFinished(path):
    with open(path, "r") as f:
            data = json.load(f)
            data["finished"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            data["status"] = 'successful'
            f.close()
            with open(path, "w") as f:
                json.dump(data, f) 
                
def zipResults(jobID):
    files = ["ndsi_clipped.tif", "bin.tif"] # zip file name
    with zipfile.ZipFile("jobs/" + jobID + "/results/ndsi_bin.zip", 'w') as zipF:
        for file in files:
            zipF.write("jobs/" + jobID + "/results/" + file, "\\" + file, compress_type=zipfile.ZIP_DEFLATED)
    
def convertRFC3339ToDatetime(datetimeString):
    r1 = datetimeString.replace('"', '') 
    r2 = r1.replace('T', ' ') 
    date = datetime.datetime.strptime(r2, "%Y-%m-%d %H:%M:%S")
    return date

def checkCreationDate(creationDate, request):
    datetimeParam = False
    if(request.args.get('datetime') == None):
        datetimeParam = True
    elif(request.args.get('datetime').startswith('[')):
        lowerBound = request.args.get('datetime')[9:]
        lowerDate = convertRFC3339ToDatetime(lowerBound)
        if(creationDate < lowerDate):
            datetimeParam = True
    elif(request.args.get('datetime').endswith(']')):
        upperBound = request.args.get('datetime')[0:29]
        upperDate = convertRFC3339ToDatetime(upperBound)
        if(creationDate > upperDate):
            datetimeParam = True
    else:
        upperBound = request.args.get('datetime')[0:29]
        upperDate = convertRFC3339ToDatetime(upperBound)
        lowerBound = request.args.get('datetime')[32:]
        lowerDate = convertRFC3339ToDatetime(lowerBound)
        if(creationDate < lowerDate and creationDate > upperDate):
            datetimeParam = True
    return datetimeParam

def checkDuration(status, request):
    if(status["started"] != "none" and (request.args.get('minDuration') != None or request.args.get('maxDuration') != None)):
        now = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        started = datetime.datetime.strptime(str(status["started"]), "%Y-%m-%d %H:%M:%S")
        duration = now - started
        duration_in_s = duration.total_seconds()
        print(duration_in_s)
        if(request.args.get('minDuration') != None and request.args.get('maxDuration') == None):
            minDuration = int(request.args.get('minDuration')[1:-1])
            if(duration_in_s > minDuration):
                minDurationParam = True
            else:
                minDurationParam = False
            maxDurationParam = True
                        
        elif(request.args.get('minDuration') == None and request.args.get('maxDuration') != None):
            maxDuration = int(request.args.get('maxDuration')[1:-1])
            if(duration_in_s < maxDuration):
                maxDurationParam = True
            else:
                maxDurationParam = False
            minDurationParam = True
                        
        else:
            minDuration = int(request.args.get('minDuration')[1:-1])
            maxDuration = int(request.args.get('maxDuration')[1:-1])
            if(duration_in_s < maxDuration and duration_in_s > minDuration):
                minDurationParam = True
                maxDurationParam = True
            else:
                minDurationParam = False
                maxDurationParam = False
    elif(status["started"] == "none" and (request.args.get('minDuration') != None or request.args.get('maxDuration') != None)):
        minDurationParam = False
        maxDurationParam = False
    else:
        minDurationParam = True
        maxDurationParam = True
    
    return [minDurationParam, maxDurationParam]

def parseInput(processID, data):
    responseType = None
    #set response Type
    if("response" in data):
        #set response type
        if(data["response"] not in ["document", "raw"]):
            responseType = "raw" #set raw as default
        else:
            responseType = data["response"] #else set selected
     
    #parse echo input
    if(processID == "Echo"):
        inputs = [data["inputs"]["echo"]]
        response = [inputs, responseType]
        
        file = open('templates/json/processes/' + processID + 'ProcessDescription.json',) #open ProcessDescription.json
        process = json.load(file) #create response   
        file.close() #close ProcessDescription.json
        
        #check transmission mode
        if("response" in data):
            if(data["outputs"]["outgoingEcho"]["transmissionMode"] not in process["outputTransmission"]):
                response = False
        
        #check media type
        if("format" in data["outputs"]["outgoingEcho"]):
            if(data["outputs"]["outgoingEcho"]["format"]["mediaType"] != process["outputs"]["outgoingEcho"]["schema"]["contentMediaType"]):
                response = False
            else:
                response.append(data["outputs"]["outgoingEcho"]["format"]["mediaType"])
        else:
            response.append(process["outputs"]["outgoingEcho"]["schema"]["contentMediaType"])
            
    if(processID == "FloodMonitoring"):
       
        if(data["inputs"]["bbox"]["bbox"][0] > data["inputs"]["bbox"]["bbox"][2] or data["inputs"]["bbox"]["bbox"][1] < data["inputs"]["bbox"]["bbox"][3]):
            return False
        
        #try:
         #   preDate = datetime.date(int(job.input[0][0:4]), int(job.input[0][4:6]), int(job.input[0][6:]))
         #   postDate = datetime.date(int(job.input[1][0:4]), int(job.input[1][4:6]), int(job.input[1][6:]))
        #except:
         #   traceback.print_exc()
          #  return False
        
        #if(postDate < preDate):
          #  return False
        
        inputs = [data["inputs"]["preDate"],
                  data["inputs"]["postDate"],
                  data["inputs"]["username"],
                  data["inputs"]["password"],
                  data["inputs"]["bbox"]["bbox"][3],
                  data["inputs"]["bbox"]["bbox"][2],
                  data["inputs"]["bbox"]["bbox"][1],
                  data["inputs"]["bbox"]["bbox"][0]]
        
        outputs = []
        
        #check transmission mode
        file = open('templates/json/processes/' + processID + 'ProcessDescription.json',) #open ProcessDescription.json
        process = json.load(file) #create response   
        file.close() #close ProcessDescription.json
        if("outputs" in data):
            for i in data["outputs"]:
                if(data["outputs"][i]["transmissionMode"] not in process["outputTransmission"]):
                    response = False
                    return response
                if(data["outputs"][i]["format"]["mediaType"] != process["outputs"][i]["schema"]["contentMediaType"]):
                    response = False
                    return response
                outputs.append([i, data["outputs"][i]["format"]["mediaType"], data["outputs"][i]["transmissionMode"]])
        response = [inputs, responseType, outputs]
    return response

def loginCopernicusHub(job):
    api = SentinelAPI(job.input[2], job.input[3]) #create api object
    return api #return api object

def getProduct(api, job, t0, t1):
    #footprint = geojson_to_wkt(read_geojson(footprint))
    product_list = api.query(geojson_to_wkt(read_geojson(job.path + "/footprint.geojson")), platformname='Sentinel-1', date=(t0, t1), producttype='GRD', sensoroperationalmode='IW', polarisationmode='VV VH') 

    product = product_list.get(list(product_list.keys())[0])
    product_id = product.get("uuid")
    product_title = product.get("title")

    return (product_id, product_title) #return a tuple containing the product id and the product title

def retrieveProduct(api, product_id, product_name, downloads_path):
    #tiff_filter = products.make_path_filter("*/measurement/*-iw-grd-vv-*-*-*-*-*.tif") #define .tif filter
    try:
        api.download(product_id, directory_path="data/", checksum=False) #download full product
        getKML(product_name)
        return True
    except LTATriggered:
        return False
    
def calibrateProductSNAP(product_id, job):
    product = snappy.ProductIO.readProduct("data/" + product_id + '.zip')
    
    #apply orbit file
    parameters = snappy.HashMap()
    parameters.put('Apply-Orbit-File', True)
    apply_orbit_file = GPF.createProduct('Apply-Orbit-File', parameters, product)
    
    #clipping
    wkt = geojson_to_wkt(read_geojson(job.path + '/footprint.geojson'))
    geometry = WKTReader().read(wkt)
    #SubsetOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
    
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geometry)
    product_subset = snappy.GPF.createProduct('Subset', parameters, apply_orbit_file)
    
    #denoising
    parameters = HashMap()
    parameters.put('removeThermalNoise', True)
    product_denoised = GPF.createProduct("ThermalNoiseRemoval", parameters, product_subset)
    
    #calibrating
    parameters = HashMap()
    parameters.put('outputSigmaBand', True)
    parameters.put('sourceBands', 'Intensity_VV')
    parameters.put('selectedPolarisations', "VV")
    parameters.put('outputImageScaleInDb', False)
    product_calibrated = GPF.createProduct("Calibration", parameters, product_denoised)
    
    #speckle filtering
    filterSizeY = '5'
    filterSizeX = '5'
    parameters = HashMap()
    parameters.put('sourceBands', 'Sigma0_VV')
    parameters.put('filter', 'Lee')
    parameters.put('filterSizeX', filterSizeX)
    parameters.put('filterSizeY', filterSizeY)
    parameters.put('dampingFactor', '2')
    parameters.put('estimateENL', 'true')
    parameters.put('enl', '1.0')
    parameters.put('numLooksStr', '1')
    parameters.put('targetWindowSizeStr', '3x3')
    parameters.put('sigmaStr', '0.9')
    parameters.put('anSize', '50')
    speckle_filter = snappy.GPF.createProduct('Speckle-Filter', parameters, product_calibrated)
    
    #terrain correction
    parameters = HashMap()
    #parameters.put('demName', 'SRTM 3Sec')
    #parameters.put('saveSelectedSourceBand', True)
    speckle_filter_tc = GPF.createProduct("Ellipsoid-Correction-RD", parameters, speckle_filter)
    
    ProductIO.writeProduct(speckle_filter_tc, job.results + product_id + '.tif', 'GeoTIFF')  
    
def ndsiSNAP(job, preID, postID):
    files = os.listdir(job.results)
    
    pre_dataset = gdal.Open(job.results + files[0]) #load pre dataset with gdal
    post_dataset = gdal.Open(job.results + files[1]) #load post dataset with gdal
    
    pre_band = pre_dataset.GetRasterBand(1) #get pre raster band
    pre_array = pre_band.ReadAsArray() #read pre raster band as array 
    
    post_band = post_dataset.GetRasterBand(1)  #get post raster band
    post_array = post_band.ReadAsArray() #read post raster band as array 
    post_array = post_band.ReadAsArray() #read post raster band as array 
    
    
    result_array = pre_array.astype('float32') #initialize result array
    
    x_range = min(pre_dataset.RasterXSize, post_dataset.RasterXSize) #get minimal x bounds
    y_range = min(pre_dataset.RasterYSize, post_dataset.RasterYSize) #get minimal y bounds
    
    for i in range(0, y_range): #iterate over y range
        for j in range(0, x_range): #iterate over x range
            if(post_array[i][j] != 0):
                result_array[i][j] = float((post_array[i][j]-pre_array[i][j])/(post_array[i][j]+pre_array[i][j])) #calculate NDSI value
            else:
                result_array[i][j] = -0
            
    driver = gdal.GetDriverByName('GTiff') #initialize driver
    image_out = driver.Create(job.results + 'ndsi.tif', pre_dataset.RasterXSize, pre_dataset.RasterYSize, 1, gdal.GDT_Float32) #initialize output image
    image_out.SetGeoTransform(pre_dataset.GetGeoTransform()) #set geotransform of output image
    image_out.SetProjection(pre_dataset.GetProjection()) #set projection of output image
    image_out.GetRasterBand(1).WriteArray(result_array) #set band information of output image
    image_out.GetRasterBand(1).SetNoDataValue(0) #set no data value of output image
    image_out.FlushCache() #flush the cash
    image_out = None #free output image
    pre_dataset = None #free source image
    post_dataset = None #free source image 
    
def clipProductSNAP(job):
    dataset = gdal.Open(job.results + 'ndsi.tif') #open raster file with gdal
    gdal.Warp(job.results + 'ndsi_clipped.tif', dataset, cutlineDSName = job.path + '/footprint.geojson', cropToCutline = True, dstNodata = -0, format="GTiff") #use gadl.warp for clipping
    dataset = None #free dataset

#function for binarize an image unsing a thresholding     
def theresholdSNAP(job):
    dataset = gdal.Open(job.results + 'ndsi_clipped.tif') #load dataset with gdal
    
    band = dataset.GetRasterBand(1) #get raster band
    image = band.ReadAsArray() #read raster band as array 
    
    otsu_thresh = threshold_otsu(image) #apply otsu thresholding
    binary_otsu = image > otsu_thresh #binarize with otsu threshold
    
    driver = gdal.GetDriverByName('GTiff') #initialize driver
    image_out = driver.Create(job.results + 'bin.tif', dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32) #initialize output image
    image_out.SetGeoTransform(dataset.GetGeoTransform()) #set geotransform of output image
    image_out.SetProjection(dataset.GetProjection())  #set projection of output image
    image_out.GetRasterBand(1).WriteArray(binary_otsu) #set band information of output image
    image_out.GetRasterBand(1).SetNoDataValue(-999) #set no data value of output image
    image_out.FlushCache() #flush the cash
    image_out = None #free output image
    dataset = None #free input image    
    
def encodeImageBase64(imagePath):
    with open(imagePath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
    
def getKML(productName):
    zip = zipfile.ZipFile('data/' + productName + '.zip')
    zip.extract(productName + '.SAFE/preview/map-overlay.kml', 'data/')
    zip.close()
    
    shutil.move('data/' + productName + '.SAFE/preview/map-overlay.kml', 'data/coverage/' + productName + '.kml')
    shutil.rmtree('data/' + productName + '.SAFE')
