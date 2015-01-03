=======================================
  PyCall - Python Call - Appel Python 
=======================================

Code permettant de faire des appels sur l'API Spark Cloud depuis du code en Python.

== Fichiers ==

* /sparkapi/sparkapi.py - contient les classes SparkApi et SparkCore 
						  pour simplifier les appels sur vos Cores via 
                          Spark Cloud
                          
* sparkapi.ini          - fichier de config pour la connexion sur Spark
                          Cloud. Vous devez créer ce fichier à partir
                          de sparkapi-sample.ini et y encoder les 
                          paramètres de votre PROPRE compte Spark Cloud
                          et le CORE_ID de votre propre Spark Core

* netled.py             - fait des appels de fonction sur le core 
                          pour controler des LED sur le core via le 
                          programme netled.ino
                          
* lecture-tmp36.py      - fait des lectures de variable sur le core
                          pour lire la valeur du senseur de température
                          tmp36. Voir le programme lecture-tmp36.ino 

* buttoncounter.py      - fait des appels sur un core faisant fonctionner le
                          programme buttoncounter.ino sur votre Core.
                          
* core-info.py          - Obtenir plus d'information sur un core.
						  Les fonctions et les variables publiées.
						  
* cores-list.py			- Lister les cores associé à votre compte
                          Spark Cloud


== Les Tutoriels Spark Core ==

Vous trouverez nos tutoriels et nombreuses autres informations sur notre wiki.

http://wiki.mchobby.be/index.php?title=Spark.IO-Accueil
