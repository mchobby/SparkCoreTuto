#!/usr/bin/env python
# -*- coding: utf8 -*-
#
"""lecture-tmp36.py

Appel d'API sur un Spark Core faisant fonctionner le programme
  lecture-tmp36.ino 
  
  retourne les valeurs publiées par la programme: temperature, voltage,
  reading.

Copyright 2015 DMeurisse <info@mchobby.be>

Voir tutoriel:
  http://wiki.mchobby.be/index.php?title=Spark-Core-Bouton
     
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
  01 jan 2015 - Dominique - v 0.1 (première release)
"""  
from sparkapi import SparkApi
from sparkapi import Config 

# Ouvre le fichier sparkapi.ini pour éviter de Hard Coder des données
# sensible comme l'access_token dans les programmes d'exemple publié sur
# le Net.
# 
# Créez votre propre fichier sparkapi.ini à partir du fichier 
# sparkapi-sample.ini
config = Config()


def main():
	# Execute le programme qui récupère le température lue sur un 
	#  Spark Core
	api = SparkApi( access_token = config.access_token, debug = False )
	# ou utiliser directement votre access_token
	#api = SparkApi( access_token = '123412341234', debug = False )
		
	# Créer un objet Core à partir du core_id 
	#   le core_id provient du fichier de configuration sparkapi.ini
	#   dans la section [CORES]
	core = api.get_core( config.cores['core0'] ) 
	# ou utiliser directement votre core_id
	#core = api.get_core( '0123456789abcdef' )
	
	# Lire les variables publiées par le code
	# retourne un tuple (connected, valeur)
	value = core.value_of( 'temperature' )
	print( 'le Core n est pas connecté' if value[0] == False else 'Température = %2f' % value[1] )
	
	value = core.value_of( 'voltage' )
	print( 'le Core n est pas connecté' if value[0] == False else 'Tension = %2f' % value[1] )
	
	value = core.value_of( 'reading' )
	print( 'le Core n est pas connecté' if value[0] == False  else 'lecture = %i' % value[1] )
		
	return 0

if __name__ == '__main__':
	main()
