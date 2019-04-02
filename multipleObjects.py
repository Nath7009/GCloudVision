
"""Localize objects in the local image.

Args:
path: The path to the local file.
"""
import glob
import json
from google.cloud import vision
import warnings
import pickle

warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")
client = vision.ImageAnnotatorClient()
localPath = '/home/Nathan/tolabel/cutimages/'
files = glob.glob(localPath+'*.jpg')
print(files)
for path in files:
	jsonpath = path.replace(localPath,"/home/Nathan/output/")
	jsonpath = jsonpath.strip('.jpg')
#	jsonpath+='.bin'
	print(jsonpath)
	with open(path, 'rb') as image_file:
	    content = image_file.read()
	image = vision.types.Image(content=content)
	
	objects = client.object_localization(image=image).localized_object_annotations
#	file = open(jsonpath,'w')
#	file.write(pickle.dump(objects))
#	with open(jsonpath, mode = 'wb') as file:
#		pickle.dump(objects, file)
#	print(dir(objects))
#	print('Number of objects found: {}'.format(len(objects)))
#	print(objects)
#	file.write('{')
	i=0
	for object_ in objects:
#		print(dir(object_))
#		print(object_.SerealizeToString)
#		file.write('{')
#		file.write('"object" : {')
		currPath = jsonpath + '_'  + '{:02d}'.format(i) + ".bin"
		with open(currPath, mode = 'wb') as file:
			pickle.dump(object_, file)
			file.close()
		print('\n{} (confidence: {})'.format(object_.name, object_.score))
		print('Normalized bounding polygon vertices: ')
		i=i+1
		for vertex in object_.bounding_poly.normalized_vertices:
			print(' - ({}, {})'.format(vertex.x, vertex.y))
#		file.write('}')
#	file.write('}')
