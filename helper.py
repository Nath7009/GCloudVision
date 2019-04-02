from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageColor
import glob
import os
import pickle
import google
from pathlib import Path
from google.cloud import vision
import warnings


def getImage(path):
	return Image.open(path).convert("RGB")

def cut(image, n):
	w, h = image.size
	winc = w/n
	hinc = h/n
	images = []
	for i in range(n):
		for j in range(n):
			border = (winc*i, hinc*j, winc*(i+1), hinc*(j+1))
			images.append(image.crop(border))
	return images

def labellize(image, client):
	tempPath = "temp/img.jpg"
	image.save(tempPath)
	warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")
	#client = vision.ImageAnnotatorClient()
	with open(tempPath, mode = 'rb') as file:
		content = file.read()
	visionImage = vision.types.Image(content=content)
	os.remove(tempPath)
	labels = client.object_localization(image=visionImage).localized_object_annotations
	w,h = (image.size[0], image.size[1])

	#On dé-normalise les vecteurs pour pouvoir les dessiner
	for label in labels:
		vertices = label.bounding_poly.normalized_vertices
		for vertex in vertices:
			vertex.x *= w
			vertex.y *= h

	return labels

def connectLabels(labels):
	#Ecart tolérable entre deux labels
	seuil = 10
	ret = labels
	for a in labels:
		for b in labels:
			if a.bounding_poly != b.bounding_poly and  a.name == b.name:
				debA = a.bounding_poly.normalized_vertices[0]
				finA = a.bounding_poly.normalized_vertices[2]
				debB = b.bounding_poly.normalized_vertices[0]
				finB = b.bounding_poly.normalized_vertices[2]

				if debB.x > debA.x and debB.y > debA.y and finB.x < finA.x and finB.y < finA.y:
#					print(a, b)
					ret.remove(b)
#					labels.remove(b)
#				elif a not in ret:
#					ret.append(a)
#				if finA.x - debB.x < seuil and finA.y - debB.y < seuil:


	return ret
#Pour le moment je ne connecte pas les différents objets entre eux

def drawImage(image, labels):
	draw = ImageDraw.Draw(image)
	width, height = (image.size[0], image.size[1])
	font = ImageFont.load_default()
	font.size = 20

	#TODO Mettre une couleur à l'extérieur des lettres plutôt qu'un rectangle
	for label in labels:
		poly = label.bounding_poly.normalized_vertices
		xdeb = xfin = ydeb = yfin = 0
		xdeb = poly[0].x
		ydeb = poly[0].y

		xfin = poly[2].x
		yfin = poly[2].y
		text = label.name + '\n' + "{:.2f}".format(label.score)
		w, h = font.getsize(label.name)
		w+=5
		h+=2
		h*=2
		x = (xdeb + xfin) / 2
		y = (ydeb + yfin) / 2

		draw.rectangle(((xdeb, ydeb), (xfin, yfin)), width = 4)
		draw.rectangle((x, y, x + w, y + h), fill='black')
		draw.multiline_text((x, y), text = text, align = "center", font = font)

	return image


def saveImage(image, path):
	image.save(path)

