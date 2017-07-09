from PIL import Image 
from PIL.ExifTags import TAGS, GPSTAGS
import numpy as np
import pandas as pd
import sys
import os
# image = Image.open("IMG_2858.jpg")
# info = image._getexif() 
# for tag, value in info.items(): 
# 	key = TAGS.get(tag, tag) 
# 	print(key + " " + str(value))

#i dont think this works 
# gpsinfo = {}
# for key in exif['GPSInfo'].keys():
#     decode = ExifTags.GPSTAGS.get(key,key)
#     gpsinfo[decode] = exif['GPSInfo'][key]
# print gpsinfo

def decodeGpsData(data):
    return {GPSTAGS.get(tag, tag): value for tag, value in data.items()}
 

def getExifData(image):
    """Extract exif data from a PIL Image to a dictionary, converting GPS tags."""
    exif = image._getexif()
    for tagId in exif:
        value = exif.pop(tagId)
        tagName = TAGS.get(tagId, tagId)
        if tagName == "GPSInfo":
            value = decodeGpsData(value)
        exif[tagName] = value
    return exif

def toDegrees(coordinates):
    """Convert coordinates like ((42, 1), (122, 1), (309712, 10000)) to decimal.
 
    Coordinates are stored in exif as a tuple of degree-info, minute-info and
    second-info. Each info is a pair of value, divider - essentially, a fraction.
 
    """
    factor = 1.0
    result = 0.0
    for (value, divider) in coordinates:
        result += value / (factor * divider)
        factor *= 60
    return result

def getLocation(exifData):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    result = {'lat': None, 'lon': None}
    if 'GPSInfo' not in exifData:
        return result
    gpsInfo = exifData["GPSInfo"]
    latitude = gpsInfo.get("GPSLatitude")
    latitudeHemisphere = gpsInfo.get('GPSLatitudeRef')
    longitude = gpsInfo.get('GPSLongitude')
    longitudeHemisphere = gpsInfo.get('GPSLongitudeRef')
    if 'GPSAltitude' in gpsInfo:     #altitude -- drone only i think --altitude ref = 1 for all i think
    	result['alt'] = gpsInfo['GPSAltitude']
    else: 
    	result['alt'] = None
    if latitude and latitudeHemisphere and longitude and longitudeHemisphere:
        result['lat'] = toDegrees(latitude)
        if latitudeHemisphere == "S":
            result['lat'] *= -1
        result['lon'] = toDegrees(longitude)
        if longitudeHemisphere == "W":
            result['lon'] *= -1
    return result

def getTime(exifData):	
	result ={'day': None, 'month': None, 'year': None, 'hour': None, 'min': None, 'sec': None}	
	if 'DateTimeOriginal' not in exif:
		return result	
	else:
		date_time = exif['DateTimeOriginal'].split(" ")	#format: [u'2017:06:04', u'19:48:46']
		result['year'] = date_time[0].split(":")[0]
		result['month'] = date_time[0].split(":")[1]
		result['day'] = date_time[0].split(":")[2]
		result['hour'] = date_time[1].split(":")[0]
		result['min'] = date_time[1].split(":")[1]
		result['sec'] = date_time[1].split(":")[2]		
	return result


if __name__ == "__main__": 
	#been copy pasting this into terminal -- need to make function for date time
	files = os.listdir(os.getcwd())
	#for only the files in the folder
	imagelist = [f for f in files if not f.startswith('.') and os.path.isfile("/".join((os.getcwd(), f)))]
	bytes = []  
		#get size of the file to ID type of photo -- low kb = likely downloads from canon 
	for f in imagelist: 
		onepath = "/".join((os.getcwd(), f))
		bytes.append(os.stat(onepath).st_size)
	lat = []
	longitude = []
	cameradeets = []
	day = [] 
	month = []
	year = []
	hour = []
	minute = []
	second = []
	iso = []
	exposuretime = []
	orientation = []
	focallength =[]
	Fstop = []
	alt = []

	for imagename in imagelist:
		image = Image.open(imagename)
		print imagename
		exif = getExifData(image)
		if 'LensModel' in exif:  #not all photos have lens model
			camerainfo = exif['LensModel']
			cameradeets.append(camerainfo)
		else:
			cameradeets.append(None)	
		if 'ISOSpeedRatings' in exif:
			iso.append(exif['ISOSpeedRatings'])
		else:
			iso.append(None)
		if 'ExposureTime' in exif:
			exposuretime.append(exif['ExposureTime'])
		else:
			exposuretime.append(None)	
		if 'FocalLength' in exif:
			focallength.append(exif['FocalLength'])
		else:
			focallength.append(None)
		if 'Orientation' in exif:  #only for iphone
			orientation.append(exif['Orientation'])	
		else:
			orientation.append(None)
		if 'FNumber' in exif:
			Fstop.append(exif['FNumber'])
		else:
			Fstop.append(None)
		# if 'GPSAltitude' in exif: 
		# 	alt.append(exif['GPSAltitude'])
		# else: 
		# 	alt.append(None)
		gpsloc = getLocation(exif)
		lat.append(gpsloc['lat'])
		longitude.append(gpsloc['lon'])
		alt.append(gpsloc['alt'][0])   #i think this is in meters, units of thousands though 
		timedata = getTime(exif)
		day.append(timedata['day'])
		month.append(timedata['month'])
		year.append(timedata['year'])
		hour.append(timedata['hour'])
		minute.append(timedata['min'])
		second.append(timedata['sec'])

# #iphone
# df = np.column_stack((lat, longitude, alt, cameradeets, iso, exposuretime, orientation, focallength, Fstop, month, day, year, hour, minute, second, bytes, imagelist))
# metadata = pd.DataFrame(df, columns = ["latitude", "longitude", "altitude", "shotinfo","iso", "exposure_time", "orientation", "focal_length", "FStop", "month", "day", "year", "hour", "minute", "sec", "size_bytes", "filename"])

#canon has tuples 
df = np.column_stack((lat, longitude, alt, cameradeets, iso, exposuretime, focallength, Fstop, month, day, year, hour, minute, second, bytes, imagelist))
metadata = pd.DataFrame(df, columns = ["latitude", "longitude", "altitude","shotinfo","iso", "exposure_time1","exposure_time2", "focal_length1","focal_length2", "FStop1","FStop2", "month", "day", "year", "hour", "minute", "sec", "size_bytes", "filename"])

metadata.to_csv("photogps_data.csv", sep = ",", encoding = 'utf-8')
