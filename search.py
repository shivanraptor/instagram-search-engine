# Instagram Image Reverse Search Engine - THE SEARCH SCRIPT
# Usage:
# python search.py --query path/to/images_to_test.jpg

# import the necessary packages
from PIL import Image
import imagehash
import argparse
import MySQLdb
import cv2
import os

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
ap.add_argument("-q", "--query", required = True,
	help = "path to the query image")
args = vars(ap.parse_args())

# open the database
mysql = MySQLdb.connect(host=config.Config.DB_HOST,user=config.Config.DB_USER,passwd=config.Config.DB_PASS,db=config.Config.DB_NAME)
cursor = mysql.cursor()

# load the query image, compute the difference image hash, and
# and grab the images from the database that have the same hash
# value
image = cv2.imread(args["query"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
imagehash = dhash(image)

sql = "SELECT ig_name FROM igdb WHERE ig_key='%s'" % (imagehash)
cursor.execute(sql)
if cursor.rowcount > 0:
	rows = cursor.fetchall()
	print "Found %d images" % (cursor.rowcount)
	for row in rows:
		print "IG Username is %s" % (row[0])
else:
	print "Found 0 images"

#filenames = db[h]
#print "Found %d images" % (len(filenames))

# loop over the images
#for filename in filenames:
#	image = Image.open(args["dataset"] + "/" + filename)
#	image.show()

# close the shelve database
mysql.close()
