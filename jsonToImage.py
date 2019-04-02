# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:22:51 2019

@author: Nathan
"""
import glob
import json
import random
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageColor


def drawJsonToImage(image, labels):
   draw = ImageDraw.Draw(image)
   width, height = (image.size[0], image.size[1])
   font = ImageFont.load_default()
   font.size = 25

   for label in labels:
      bound = label.get("bounding_poly")
      poly = []
      for vertex in bound:
         poly.append(vertex)
      xdeb = xfin = ydeb = yfin = 0
      xdeb = float(poly[0].get("x"))
      if poly[0].get("y"):
         ydeb = float(poly[0].get("y"))
      xfin = float(poly[2].get("x"))
      if poly[2].get("y"):
         yfin = float(poly[2].get("y"))
      name = label.get("name")
      score = label.get("score")
      text = name + "\n" + "{:.2f}".format(float(score))
      rectColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
      shadowColor = 'black'
      outlineAmount = 2

      draw.rectangle(((xdeb, ydeb), (xfin, yfin)), outline = rectColor, width = 1)

      x = (xdeb + xfin) / 2
      y = (ydeb + yfin) / 2

      for adj in range(outlineAmount):
          draw.multiline_text((x-adj, y), text, font=font, fill=shadowColor)
          draw.multiline_text((x+adj, y), text, font=font, fill=shadowColor)
          draw.multiline_text((x, y+adj), text, font=font, fill=shadowColor)
          draw.multiline_text((x, y-adj), text, font=font, fill=shadowColor)
          draw.multiline_text((x-adj, y+adj), text, font=font, fill=shadowColor)
          draw.multiline_text((x+adj, y+adj), text, font=font, fill=shadowColor)
          draw.multiline_text((x-adj, y-adj), text, font=font, fill=shadowColor)
          draw.multiline_text((x+adj, y-adj), text, font=font, fill=shadowColor)

      draw.multiline_text((x, y), text = text, font = font)
   return image
   #image.show()
      #Pour changer la couleur en fonction du texte écrit
      #abs(hash(name)) % (10 ** 6)
      #print(label.get('name'))

rawFolder = "tolabellize/dataset/"
jsonFolder = "labellizedimages/"
outputFolder = jsonFolder

rawImagesPath = glob.glob(rawFolder + "*.jpg")
#rawImagesPath = rawImagesPath[:1]
jsonsPath = glob.glob(jsonFolder + "*.json")
index = 0
for imagePath in rawImagesPath:
   image = Image.open(imagePath).convert("RGB")
   labels = []
   with open(jsonsPath[index], "r") as file:
      text = file.read()
      if(len(text)>10):
         labels = json.loads(text)

   if(len(labels)>0):
      drawn = drawJsonToImage(image, labels)
      elements = imagePath.split("/")
      elements = elements[len(elements) - 1].split("\\")
      imageName = elements[len(elements) - 1]
      drawn.save(outputFolder + imageName)

   index+=1
   print(index)
