#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import commands
import cgi, cgitb
import MySQLdb
import cv2
import uuid
# import config settings
import config
# import functions
from functions import dhash

UPLOAD_DIR = './upload'

def save_uploaded_file():
	print "Content-Type: text/html; charset=UTF-8\n"
	print '''
		<html>
		<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<title>Result</title>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">
		<link rel="stylesheet" href="css/igsearch.css" />
		<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
		</head>
		<body class="text-center">
			<div class="result_box">
	'''
	
	form = cgi.FieldStorage()
	if not form.has_key('file_upload'):
		print '<p>ERROR: Missing Upload Input Param</p>'
		return
	form_file = form['file_upload']
	if not form_file.file:
		print '<p>ERROR: Missing upload file</p>'
		return
	if not form_file.filename:
		print '<p>ERROR: Missing upload filename</p>'
		return
	form_file.file.seek(0, os.SEEK_END)
	filesize = form_file.file.tell()
	form_file.file.seek(0) # reset to the start of the file
	if filesize > 5 * 1024 * 1024:
		print '<p>ERROR: File size should be less than 5MB</p>'
		return

	uploaded_file_path = os.path.join(UPLOAD_DIR, str(uuid.uuid4()) + ".jpg")
	with open(uploaded_file_path, 'wb') as fout:
		while True:
			chunk = form_file.file.read(100000)
			if not chunk:
				break
			fout.write(chunk)
	print '<p>Upload completed</p>'
	
	# open the image for inspection, load image from disk
	image = cv2.imread(uploaded_file_path)
	
	# skip if the image cannot be loaded
	if image is None:
		print '<p>ERROR: Image cannot be loaded</p>'
		return
	
	# convert the image to grayscale and compute hash
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imagehash = dhash(image)
	
	# open the database
	mysql = MySQLdb.connect(host=config.Config.DB_HOST,user=config.Config.DB_USER,passwd=config.Config.DB_PASS,db=config.Config.DB_NAME)
	cursor = mysql.cursor()
	
	sql = "SELECT ig_name FROM igdb WHERE ig_key='%s'" % (imagehash)
	cursor.execute(sql)
	
	if cursor.rowcount > 0:
		rows = cursor.fetchall()
		print "<p>Found %d result(s)</p>" % (cursor.rowcount)
		for row in rows:
			print "<p>IG Username is <b>%s</b></p>" % (row[0])
	else:
		print "<p>Found 0 results</p>"
	
	mysql.close()
	
	# remove the file afterwards
	os.remove(uploaded_file_path)
	
	print "</div></body></html>"

cgitb.enable()
save_uploaded_file()