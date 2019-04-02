This project is using Google Cloud Vision API to labellize images.

It uses a VM build on Google Compute to ask the API, the response is then converted into JSON that can be saved.

To enhance the number of detected objects, you can cut the images in identical rectangular parts.
The object detection seems more precise but the system can detect strange things.

Enoncé initial :

Responsable :	Pascal SALEMBIER

Titre : Utilisation d'API de Deep Learning pour l'analyse d'images

Description :	
L'objectif de cette TX est de mettre en oeuvre un ou plusieurs services d'analyse d'images reposant sur du Machine Learning (AWS Rekognition, Google Auto ML, Uber Ludwig,...) afin de tester leurs capacité à identifier des objets plus ou moins complexes et abstraits dans un corpus de photos.

Ce travail s'inscrit dans le contexte d'un projet de recherche mené en collaboration avec Orange Labs sur l'évaluation de systèmes d'authentification graphique. A partir d'un ensemble d'illustrations utilisées comme jeu de test, la mise en oeuvre de systèmes automatiques d'analyse d'images permettra de vérifier la résistance d'un système d'authentification graphique expérimental à des attaques automatiques nécessitant des capacités  d'identification d'objets permettant l'inférence de mots de passe.


