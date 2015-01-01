=======================================
  PyCall - Python Call - Appel Python 
=======================================

Code permettant de faire des appels sur l'API Spark Cloud depuis du code en Python.

== Fichiers ==

* /sparkapi/sparkapi.py - contient la classe sparkapi pour simplifier les 
                          appel sur Spark Cloud
                          
* sparkapi.ini          - fichier de config pour la connexion sur Spark
                          Cloud. Vous devez créer ce fichier à partir
                          de sparkapi-sample.ini et y encoder les 
                          paramètres de votre PROPRE compte Spark Cloud
                          et le CORE_ID de votre propre Spark Core

* buttoncounter.py      - fait des appels sur un core faisant fonctionner le
                          programme buttoncounter.ino sur votre Core.


== Les Tutoriels Spark Core ==

Vous trouverez nos tutoriels et nombreuses autres informations sur notre wiki.

http://wiki.mchobby.be/index.php?title=Spark.IO-Accueil
