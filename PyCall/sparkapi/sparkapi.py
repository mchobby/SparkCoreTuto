#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""sparkapi.py

Spark API helper for Python - Version alpha
  
Copyright 2015 DMeurisse <info@mchobby.be>

Voyez nos tutoriel Spark Core sur 
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
  01 jan 2015 - Dominique - v 0.1 (première release)
  
------------------------------------------------------------------------
Remarks:
  Doc Python sur urllib2
     https://docs.python.org/2/howto/urllib2.html
"""
import urllib2, urllib
import json 

# --- API Spark Cloud ---
SPARK_API_URL_V1 = 'https://api.spark.io/v1/devices/'

class SparkApi( object ):
	""" Classe pour gérer/faciliter les appels sur l'API Spark Cloud 
	
	Voir produit: http://shop.mchobby.be/product.php?id_product=518
	Voir tuto: http://wiki.mchobby.be/index.php?title=Spark.IO-Accueil"""
	
	__api_base_url = None # URL pour atteindre l'API du SparkC Cloud
	__debug = False # Affiche des message debug sur la console
	__access_token = None # Access Token sur Spark Cloud
	
	def __init__( self, access_token, spark_api_url = SPARK_API_URL_V1, debug = False ):
		""" Initialise l'objet 
		
			Args:
			    access_token  (str): votre access token lié à votre compte Spark Cloud
									 voir notre tuto http://wiki.mchobby.be/index.php?title=Spark-Core-NetLED#Faire_une_requ.C3.AAte_sur_l.27API
									 pour identifier votre core_id et access_token
				spark_api_url (str): URL de base de l'API SPARK CLOUD
		"""
		self.__debug = debug
		self.__api_base_url = spark_api_url	
		self.__access_token = access_token
		
		self.printdebug( 'Spark API Url: %s' % self.__api_base_url )
		self.printdebug( 'access_token: %s' % self.__access_token )
		
	def get_core( self, core_id ):
		""" Créer un objet SparkCore pour un Core_id donné """
		_obj = SparkCore( self, core_id )
		
		return _obj
		
	def api_get_variable( self, core_id, variable_name ):
		""" Faire une requête sur l'API Spark Cloud pour retrouver une
		variable publiée par le Core interrogé.
		
		retourne la structure json renvoyé par l'api Spark """
		
		assert isinstance( core_id, str ), 'core_id must be str type!'
		assert isinstance( variable_name, str ), 'variable_name must be str type!'
		
		url = self.__api_base_url+core_id+'/'+variable_name+'?access_token='+self.__access_token
		self.printdebug( url )
		response = urllib2.urlopen( url )
		html = response.read()
		data = json.loads( html )
		       
		# Retourne un information similaire à ceci
		# {u'coreInfo': {u'connected': True, u'last_heard': u'2015-01-01T15:17:09.082Z', 
		#  u'last_app': u'', u'deviceID': u'54xxxxxxxxxxxxxxxxxxxx67'}, 
		# u'cmd': u'VarReturn', u'name': u'counter', u'result': 0}
		
		assert (data['cmd'] == u'VarReturn'), 'Spark Cloud API did not return VarReturn content'  
		return data

	def api_call_function( self, core_id, function_name, params ):
		""" Faire une requête sur l'API Spark Cloud pour exécuté une
		fonction publiée par le Core interrogé.
		
		retourne la structure json renvoyée par l'api Spark """
		assert isinstance( core_id, str ), 'core_id must be str type!'
		assert isinstance( function_name, str ), 'function_name must be str type!'
		assert isinstance( params, str ), 'params must be str type!'

		url =  self.__api_base_url+core_id+'/'+function_name
		values = {'access_token' : self.__access_token,
			'params' : params }
		self.printdebug( 'POST to %s' % url )
		self.printdebug( values )
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		html = response.read()
		
		jsonData = json.loads( html )
		
		# {u'connected': True, u'last_app': None, u'id': u'54xxxxxxxxxxxxxxxxxxxx67', 
		# u'return_value': 1, u'name': u'mch-demo'}
		assert isinstance( jsonData['return_value'], int ), 'Spark Cloud API did not return the expected return_value' 
		
		if( jsonData['connected'] == True ):
			return ( True, jsonData['return_value'] )
		else:
			return ( False, None )
		
	def printdebug( self, sMsg ):
		if( self.__debug ):
			print sMsg

class SparkCore( object ):
	""" Classe permettant de faire des appel d'API sur un Core 
	    en particulier """
	__owner = None # référence vers l'objet SparkApi
	__core_id = None # Identification du Spark Core par son Core ID
	    
	def __init__( self, spark_api, core_id ):
		"""  Initialise l'objet Spark Core 
		
		Args: 
			spark_api (SparkApi) - reference vers l'objet permettant
						d'accéder à l'API sur Spark Cloud
						
			core_id (str) - id d'identification du core"""  
		
		assert isinstance(spark_api, SparkApi), 'spark_api must be SparkApi type!'
			
		self.__core_id = core_id
		self.__owner = spark_api
		
		self.__owner.printdebug( 'SparkCore object created for core_id %s' % core_id )
		
	def value_of( self, variable_name ):
		""" Interroge le core pour retrouver la valeur de la variable 
		variable_name.
		
		Args:
			variable_name (str) - Nom de la variable à retrouver
			
		returns:
			tuple (connecté,valeur/None) - permet de savoir si le Core
				est en ligne et la valeur de la variable"""
			
		assert isinstance( variable_name, str ), 'variable_name must be str type!'
		
		content = self.__owner.api_get_variable( self.__core_id, variable_name )
		if( content['coreInfo']['connected'] == True ):
			return ( True, content['result'] )
		else:
			return ( False, None )

	def call( self, function_name, params = '' ):
		""" Appel de fonction 'function_name' sur le Core en passant la
		string de paramètre 'params' lors de l'appel de la fonction.
		
		Args:
			function_name (str) - nom de la fonction a appeler sur le
					core.
			params (str) - chaine de paramètres à envoyer en argument
					à la fonction du core.
		
		returns:
			tuple (connecté,valeur de retour/None) - permet de savoir
			    si le Core est en ligne et la valeur de retour de la
			    fonction appelée"""
			    
		assert isinstance(function_name, str), 'function_name must be str type!'
		assert isinstance(params, str), 'params must be str type!'
		
		content = self.__owner.api_call_function( self.__core_id, function_name, params )
		
		return content
