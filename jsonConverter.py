def labelToJson(label):

	json = "{" + "\n"
	json += '"mid"' + ": " + '"' + label.mid + '",' + "\n"
	json += '"name"' + ": " + '"' +label.name + '",' + "\n"
	json +='"score"' + ": " + '"' + str(label.score) + '",' + "\n"
	json += '"bounding_poly"' + ": [" + "\n"
	for vertex in label.bounding_poly.normalized_vertices:
		json += "{"
		json += '"x"' + ": " + '"' + str(vertex.x) + '"'
		if(vertex.y):
			json +=",\n" +  '"y"' + ": " + '"' + str(vertex.y) + '"' + "\n"
          else:
               json +=",\n" +  '"y"' + ": " + '"' + "0" + '"' + "\n"
		json += "}"
		json += ","

     if json[-1] == ",":
          json = json[:-1]
	json += "]" + "\n"
	json += "}"
	return json

def listToJson(labels):
	json = "["
	for label in labels:
		json += labelToJson(label)
		json += ","
	json = json[:-1]
	json +="]"
	return json

