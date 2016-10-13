import urllib
import sys
import os
from time import sleep
from tqdm import tqdm
import Image

filename = sys.argv[1]
dirName = filename.rsplit( ".", 1 )[ 0 ]
print("Reading: " +filename)
if(filename == None or not filename.endswith('.txt')):
	raise Exception('Wrong File Type. Must read from txt')

if os.path.isdir(dirName):
	raise Exception('Dir already exists')
else:
	os.mkdir(dirName)

input_file = open(filename, 'r')

counter = 0
for line in tqdm(input_file):
	try:
		resource = urllib.urlopen(line)
	except IOError:
		#print("File " + line +" not found")
		continue
	img = dirName+"/"+dirName + "_" + str(counter) +".jpg"
	#print "Downloaded: " + img
	output = open(img,"wb")
	data = resource.read()

	##Verify that the image is a jpg and that is it valid
	if len(data) < 16 or data[:2] != '\377\330':
		#print("Image not a valid image")
		output.close()
		os.remove(img)
	else:
		output.write(data)
		output.close()
		counter = counter + 1

	# URL= line
	# IMAGE = URL.rsplit('/',1)[1]
	# urllib.urlretrieve(URL, IMAGE)
print(str(counter) + " Images Downloaded into /" + dirName)
