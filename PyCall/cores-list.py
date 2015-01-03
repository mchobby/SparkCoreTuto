#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""cores-list.py

Appel d'API sur un Spark Core pour lister les Cores associés à
votre compte Spark Cloud.
  
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
  03 jan 2015 - Dominique - v 0.1 (première release)
"""  
from sparkapi.sparkapi import SparkApi
from sparkapi.config import Config 

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
		
	# Afficher la liste des cores
	print( '----- dump_core_list -----' ) 	
	api.dump_core_list()
	
	# obtenir une liste des cores 
	#   retourne une liste de (core_id, core_name, connected )
	print( '----- core_list -----' )
	cores = api.core_list()
	for core in cores:
		print( 'core id %s is %s' % (core[0], 'connected' if core[2]==True else 'NOT connected') )
	
	# Données brutes tels que renvoyées par le l'API Spark Cloud
	print( '----- api_get_core_list -----' )
	print( api.api_get_core_list() )
	
	print( '----- Exploration des Cores connectés -----' )
	# Pour le fun... Explorer l'interface des cores connectés
	cores = api.core_list()
	for core in cores:
		print( '--- %s (%s) ----' % (core[0], core[1]) )
		print( 'Connected' if core[2]==True else 'NOT CONNECTED' )
		# Afficher l'API du core s'il est connecté
		if core[2]==True:
			# Créer un objet pour accéder aux fonctionalités du Core
			coreObj = api.get_core( core[0] )
			coreObj.dump_info()
		
	return 0

if __name__ == '__main__':
	main()
