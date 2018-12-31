# Instagram Image Reverse Search Engine - THE INDEXING SCRIPT
# Usage:
# python index.py --dataset images

# import the necessary packages
from imutils import paths
import argparse
import cv2
import os
import MySQLdb
import glob
# import config settings
import config

# function from: https://www.pyimagesearch.com/2017/11/27/image-hashing-opencv-python/
def dhash(image, hashSize=8):
	# resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hashSize + 1, hashSize))
 
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
 
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
	
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "path to input dataset of images")
args = vars(ap.parse_args())

# open the MySQL database
mysql = MySQLdb.connect(host=config.Config.DB_HOST, user=config.Config.DB_USER, passwd=config.Config.DB_PASS, db=config.Config.DB_NAME)
cursor = mysql.cursor()

# loop through the directory to look for .jpg
for imagePath in glob.glob(args["dataset"] + "/*/*.jpg"):
	# load image from disk
	image = cv2.imread(imagePath)
	
	# skip if the image cannot be loaded
	if image is None:
		continue
	
	# convert the image to grayscale and compute hash
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imagehash = dhash(image)
	
	# skip if the image is unreadable, or hash equals 0 for some reasons (blank screenshot)
	if imagehash != '0':	
		# extract the file name and the subfolder name
		filename = imagePath[imagePath.rfind("/") + 1:]
		tokens = imagePath.split('/')
		subfolder = tokens[1].replace("#", ".")
	
		# insert / update DB
		sql = "REPLACE INTO igdb (ig_key, ig_name, file_path) VALUES ('%s','%s','%s')" % (imagehash, subfolder, filename)
		cursor.execute(sql)
		# Commit the transaction
		mysql.commit()
	
		# Option 1: rename the file afterwards
		os.rename(imagePath, imagePath.replace(".jpg", ".done"))
	
		# Option 2: remove the image (WARN: irreversible action)
		#if os.path.exists(imagePath):
		#	os.remove(imagePath)

# close DB connection after use
mysql.close()