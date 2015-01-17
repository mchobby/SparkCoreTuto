#!/usr/bin/env python
# -*- coding: utf8 -*-
#
"""core-flash.py

Flasher votre Core à partir d'un script Python.

Appel d'API sur un Spark Cloud pour envoyer un code source (fichier 
  ino), le faire compiler par les serveurs de Spark PUIS Flasher
  notre Core avec le binaire obtenu.
  
Copyright 2015 DMeurisse <info@mchobby.be>

Voir nos tutoriels Spark Core:
  http://wiki.mchobby.be/index.php?title=Spark.IO-Accueil
     
Ou acheter Spark Core -- et soutenir nos travaux --

   http://shop.mchobby.be/category.php?id_category=54

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
  
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
  
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.

------------------------------------------------------------------------
History:
  17 jan 2015 - Dominique - v 0.1 (première release)
"""  
from sparkapi import SparkApi
from sparkapi import FLASH_STATUS_TEXT
from sparkapi import Config 

# Ouvre le fichier sparkapi.ini pour éviter de Hard Coder des données
# sensible comme l'access_token dans les programmes d'exemple publié sur
# le Net.
# 
# Créez votre propre fichier sparkapi.ini à partir du fichier 
# sparkapi-sample.ini
config = Config()


def main():
	# Execute le script qui compile le fichier lecture-tmp36.ino
	# disponible sur le disque PUIS flasher le core avec le binaire 
	# Résultant 
	 
	api = SparkApi( access_token = config.access_token, debug = False )
	# ou utiliser directement votre access_token
	#api = SparkApi( access_token = '123412341234', debug = False )
		
	# Créer un objet Core à partir du core_id 
	#   le core_id provient du fichier de configuration sparkapi.ini
	#   dans la section [CORES]
	core = api.get_core( config.cores['core0'] ) 
	# ou utiliser directement votre core_id
	#core = api.get_core( '0123456789abcdef' )
	
	print( '-- Flash le programme lecture-tmp36.ino sur le Core --' )
	
	# Activer la seconde ligne si vous voulez voir le résultat d'une
	# Erreur de compilation
	result = core.flash( '../lecture-tmp36/lecture-tmp36.ino' )
	#result = core.flash( '../wrong/wrong.ino' )
	
	print( 'FLASH : %s ' % 'ok' if result[0] == True else 'FAILED!' )
	print( 'STATUS: %s ' % (FLASH_STATUS_TEXT[ result[1] ]) ) 
	# Si le flash echoue --> afficher les info complémentaires
	if result[0] == False:
		print( result[2] ) 
		
	return 0

if __name__ == '__main__':
	main()
