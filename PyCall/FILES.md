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
                          
* sparkapi-inifile-tls.py - *** OUTILS PRATIQUE ***
                          Programme simple qui se connecte sur votre 
						  compte Spark et affiche l'access_token et 
						  CORE_ID a copier/coller dans le fichier 
						  sparkapi.ini

== Fichiers (Requête sur Core) ==

* netled.py             - fait des appels de fonction sur le core 
                          pour controler des LED sur le core via le 
                          programme netled.ino
                          
* lecture-tmp36.py      - fait des lectures de variable sur le core
                          pour lire la valeur du senseur de température
                          tmp36. Voir le programme lecture-tmp36.ino 

* buttoncounter.py      - fait des appels sur un core faisant fonctionner le
                          programme buttoncounter.ino.
                          
* magneticswitch        - fait des appels sur un core faisant fonctionner
                          le programme magneticswitch.ino
                          
* core-info.py          - Obtenir plus d'information sur un core.
						  Les fonctions et les variables publiées.  
                          
* core-tinkering.py     - Comment définir une classe SparkCoreTinker
						  et utiliser ses méthodes pour faciliter les
						  appel sur l'API publié par le Spark Core.
						  Exemple basé sur Tinker de SPARK :-)
						  Vous pouvez donc controler directement Tinker
						     depuis Python :-)

== Fichiers (Requête sur API Spark Cloud) ==

* cores-list.py			- Lister les cores associé à votre compte
                          Spark Cloud
						     
* access-tokens-list.py - S'adresse à l' API pour lister tous les access
						  token liés à votre compte Spark Cloud.
						  
* access-token-create.py - Crée/ajoute un access_token lié à votre compte
						    Spark Cloud. Utilise le client_id 'xytest'
						    
* access-token-delete.py - Efface un access_token lié à votre compte
						    Spark Cloud. Efface les token liés au 
						    client_id 'xytest'


== Les Tutoriels Spark Core ==

Vous trouverez nos tutoriels et nombreuses autres informations sur notre wiki.

http://wiki.mchobby.be/index.php?title=Spark.IO-Accueil
