from helper import getImage, cut, labellize, connectLabels, drawImage, saveImage
from jsonConverter import labelToJson, listToJson
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageColor
from progress.bar import IncrementalBar
from google.cloud import vision
import glob
import progress
import os
import json
import jsonpickle

class Label:
	def __init__(self, name, pos, score):
		self.name = name
		self.score = score
		self.bounding_poly = []
		for vertex in pos.normalized_vertices:
			obj = (vertex.x, vertex.y)
			self.bounding_poly.append(obj)

def labellizeImage(filePath, savePath, nbFrag, client):
	image = getImage(filePath)
	labels = []

	for n in  range(1,nbFrag):
		fragments = cut(image, n)
		#print("Image découpée en " + str((n+1)*(n+1)))

		w, h = image.size
		dw = w / n
		dh = h / n
		x=y=0
		for fragment in fragments:
			newLabels = labellize(fragment, client)

			for label in newLabels:
				vertices = label.bounding_poly.normalized_vertices
				for vertex in vertices:
					vertex.x+=x
					vertex.y+=y
			y+=dh
			if y >= h:
				y=0
				x+=dw

			labels.extend(newLabels)

#		print("Fragments labellisés, " + str(len(labels)) + " labels")
#	lbls = []

#	for label in labels:
#		lbls.append(Label(label.name, label.bounding_poly, label.score))

#	labels = connectLabels(labels)
#	print("Fragements connectés : " + str(len(labels)) + " fragments restants")
	#print (json.dumps(lbls))
#	text = jsonpickle.encode(labels[0])
#	print(text)
	#print(dir(labels[0]))
	drawn = drawImage(image, labels)
	#print("Image dessinée")

	saveImage(drawn, savePath)
	json = listToJson(labels)
	savePath = savePath[:-4]
	savePath += ".json"
	with open(savePath, 'w') as file:
		file.write(json)
	#print("Image sauvegardée")

def labellizeFolder(folderPath, savePath, nbFrag):
	imagesPath = glob.glob(folderPath + "*.jpg")
	client = vision.ImageAnnotatorClient()
	bar = IncrementalBar("Processing of the folder " + folderPath + " in " + str(nbFrag) + " fragments", max = len(imagesPath))
	for path in imagesPath:
		elements = path.split('/')
		imageName = elements[len(elements) - 1]
		outputPath = savePath + imageName
		labellizeImage(path, outputPath, nbFrag, client)
		bar.next()
	bar.finish()
	return 0



inputFolder = "../tolabel/dataset/"
outputFolder = "../output/"

#Récupération des images
os.system("gsutil -m rsync -r gs://tolabellize ../tolabel/")

labellizeFolder(inputFolder, outputFolder, 3)
#labellizeImage("tolabel/images/2eifthqrsda21.jpg", "output/2eifthqrsda21.jpg",  2)

os.system("gsutil -m rsync -r ../output/ gs://labellizedimages")
