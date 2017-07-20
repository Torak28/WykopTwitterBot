import os
import shutil


filenamePicture = "output.jpg"
filenameText = "output.txt"
pycahce = "./__pycache__"

if os.path.exists(filenamePicture):
	os.remove(filenamePicture)

if os.path.exists(filenameText):
	os.remove(filenameText)

if os.path.exists(pycahce):
	shutil.rmtree(pycahce)
