#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""access-tokens-list.py

Appel d'API sur Spark Cloud pour lister les access_tokens, identifié 
les access_token ayant un client_id 'xytest' (créé par access_token_create.py) 
et les effaces de votre compte votre compte Spark Cloud.
  
Copyright 2015 DMeurisse <info@mchobby.be>

Voir tutoriel:
  http://wiki.mchobby.be/index.php?title=Spark-Could-API-Auth
     
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
  10 jan 2015 - Dominique - v 0.1 (première release)
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
		
	# Afficher la liste des acces_tokens liés au compte spark core
	print( '----- Delete the \'xytest\' access_tokens -----' ) 
	print( 'Warning:' )
	print( '   Trying to delete the last created access token will always' )
	print( '   raise an httplib.BadStatusLine exception re-casted to ' ) 
	print( '   SparkApiError exception!' )
	print( '' )
	print( 'Spark Account needed to access such API' ) 
	user = raw_input( 'Your Spark Account: ' )
	passwd = raw_input( 'Your Spark Password: ' )
		
	result = api.api_get_access_tokens( user, passwd )
	access_token_list = result[1]
	# print( access_token_list )
	
	for access_token in access_token_list:
		if( access_token['client'] == 'xytest' ): 
			print( 'Delete Access Token: %s' % access_token['token'] )
			result = api.api_delete_access_token( user, passwd, access_token['token'] ) 
			print( 'API Result: %s ' % result[1] )
			print( '' )
			
	return 0

if __name__ == '__main__':
	main()
