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
  03 jan 2015 - Dominique - v 0.2 ajout de fonctionnalités + consistance
  06 jan 2015 - Dominique - v 0.3 Ajout de la classe SparkCoreTinker
  07 jan 2015 - Dominique -       Refactoring
  10 jan 2015 - Dominique -       get_api_access_tokens
								  SPARK_API_URL_V1 *** changed !! ***
------------------------------------------------------------------------
Remarks:
  Doc Python sur urllib2
     https://docs.python.org/2/howto/urllib2.html
"""
from urllib2 import HTTPError
from httplib import BadStatusLine 
import urllib2, urllib
import json, base64

# --- API Spark Cloud ---
SPARK_API_URL    = 'https://api.spark.io/'
SPARK_API_URL_V1 = SPARK_API_URL+'v1/'

# --- Spark Cloud Errors ---
# Voyez la documentation en français sur
#     http://wiki.mchobby.be/index.php?title=Spark-Could-API-Errors
#
#   { Http_error : (Http_Error_Text, Spark_Error_description), ... ]
SPARK_HTTP_ERRORS = { 

    400 : ( 'Bad Request'  , 'Your request is not understood by the Core, or the requested subresource (variable/function) has not been exposed. wrong access token may also cause this error!' ), 
	401 : ( 'Unauthorized' , 'Your access_token/account_info is not valid.' ),
	403 : ( 'Forbidden'    , 'Your access token is not authorized to interface with this Core.' ),
	404 : ( 'Not Found'    , 'The requested Core is not currently connected to the cloud OR exposed variable/function does not match!' ),
	408 : ( 'Timed Out'    , 'The cloud experienced a significant delay when trying to reach the Core.' ),
	500 : ( 'Server errors', 'Spark Server Failure. Something went wrong on Spark end.' ) 
	}

class SparkApiError( HTTPError ):
	""" Erreur d'appel sur l'API Spark. Contient des infos complémentaires
	
	Les erreurs sur l'API Spark retourne des HTTPError. Dans
	certains cas de figure (et suivant l'erreur HTTP), il est possible 
	de fournir des informations pertinantes dans l'erreur.
	Dans ce cas, la classe HTTPError est surclassée dans une classe
	SparkApiError. 
	
	Le traitement des cas d'erreur est assuré par SparkApi.api_manage_error()
	"""
	__tip_msg = None # Info complémentaire sur la cause de l'erreur
	 
	def __init__( self, err, sTipMsg ):
		""" Crée un objet d'erreur HTTPError + info complémentaire 
		
		Args:
			err (HTTPError) - Classe à la source de l'erreur
			sTipMsg (str) - Message complémentaire ou raison possible
							  de l'erreur sur l'API Spark."""

		assert isinstance( err, HTTPError ) or isinstance( err, BadStatusLine ), 'err parameter must be HttpError or BasStatusLine type' 
		assert isinstance( sTipMsg, str ), 'sTipError (additional info on Spark Api error) must be str type!' 
		
		if isinstance( err, HTTPError ):
			HTTPError.__init__( self, err.url, err.code, err.msg, err.hdrs, err.fp )
		else:
			# When Having BadStatusLine error, just encapsulate it
			# into the SparkApiError anyway!
			HTTPError.__init__( self, 'none', -1, 'Source exception class: %s, with message \'%s\'' % (err.__class__.__name__,err.message ), None, None )
		self.__tip_msg = sTipMsg
		
	def __str__( self ):
		return self.__tip_msg +'. '+HTTPError.__str__(self)

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
		
	def get_core_by_class( self, core_id, spark_core_class ):
		""" Créee et initialise un objet de la classe spark_core_class 
		    (SparkCore ou dérivé) pour un Core_id donné.
		    
		    Permet de créer une classe Spark Core avec des methodes 
		    spécialisées."""
		assert issubclass( spark_core_class, SparkCore ), 'spark_core_class must be a SparkCore (or derivated) class'
		_obj = spark_core_class( self, core_id )
		
		return _obj 

	def get_core( self, core_id ):
		""" Créer un objet SparkCore pour un Core_id donné """
		# _obj = SparkCore( self, core_id )
		# return _obj
		return self.get_core_by_class( core_id, SparkCore ) # create a SparkCore object
		
	def api_core_get_variable( self, core_id, variable_name ):
		""" Faire une requête sur l'API Spark Cloud pour retrouver une
		variable publiée par le Core interrogé.
		
		retourne la structure json renvoyé par l'api Spark """
		
		assert isinstance( core_id, basestring), 'core_id must be str/unicode type' # basestring match str & unicode
		assert isinstance( variable_name, basestring), 'variable_name must be str/unicode type' # basestring match str & unicode
		
		url = self.__api_base_url+'devices/'+core_id+'/'+variable_name+'?access_token='+self.__access_token
		self.printdebug( url )
		try:
			try:
				response = urllib2.urlopen( url )
			except HTTPError, err:
				# gère les cas d'erreur Http Error et fait une surcharge si
				# approprié
				self.api_manage_error( err )
		except SparkApiError, err:
			if( err.code == 408 ): # time-out
				return ( False, None )
			raise err
				
		html = response.read()
		data = json.loads( html )
		       
		# Retourne un information similaire à ceci
		# {u'coreInfo': {u'connected': True, u'last_heard': u'2015-01-01T15:17:09.082Z', 
		#  u'last_app': u'', u'deviceID': u'54xxxxxxxxxxxxxxxxxxxx67'}, 
		# u'cmd': u'VarReturn', u'name': u'counter', u'result': 0}
		
		assert (data['cmd'] == u'VarReturn'), 'Spark Cloud API did not return VarReturn content'  
		if( data['coreInfo']['connected'] == True ):
			return ( True, data['result'] )
		else:
			return ( False, None )


	def api_core_call_function( self, core_id, function_name, params ):
		""" Faire une requête sur l'API Spark Cloud pour exécuté une
		fonction publiée par le Core interrogé.
		
		retourne la structure json renvoyée par l'api Spark """
		assert isinstance( core_id, basestring), 'core_id must be str/unicode type' # basestring match str & unicode
		assert isinstance( function_name, basestring), 'function_name must be str/unicode type' # basestring match str & unicode
		assert isinstance( params, basestring), 'params must be str/unicode type' # basestring match str & unicode

		url =  self.__api_base_url+'devices/'+core_id+'/'+function_name
		values = {'access_token' : self.__access_token,
			'params' : params }
		self.printdebug( 'POST to %s' % url )
		self.printdebug( values )
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		try:
			try:
				response = urllib2.urlopen(req)
			except HTTPError, err:
				# gère les cas d'erreur Http Error et fait une surcharge si
				# approprié
				self.api_manage_error( err )
		except SparkApiError, err:
			if( err.code == 408 ): # time-out
				return ( False, None )
			raise

		html = response.read()
		
		jsonData = json.loads( html )
		
		# {u'connected': True, u'last_app': None, u'id': u'54xxxxxxxxxxxxxxxxxxxx67', 
		# u'return_value': 1, u'name': u'mch-demo'}
		assert isinstance( jsonData['return_value'], int ), 'Spark Cloud API did not return the expected return_value' 
		
		if( jsonData['connected'] == True ):
			return ( True, jsonData['return_value'] )
		else:
			return ( False, None )
			
	def api_core_get_info( self, core_id ):
		""" retrouver les informations sur Core, y compris les 
		    fonctions & variables publiée sur Spark Cloud"""
		assert isinstance( core_id, basestring), 'core_id must be str/unicode type' # basestring match str & unicode
		
		url = self.__api_base_url+'devices/'+core_id+'?access_token='+self.__access_token
		self.printdebug( url )
		try:
			try:
				response = urllib2.urlopen( url )
			except HTTPError, err:
				# gère les cas d'erreur Http Error et fait une surcharge si
				# approprié
				self.api_manage_error( err )
		except SparkApiError, err:
			if( err.code == 408 ): # time-out
				return ( False, None )
			raise err
				
		html = response.read()
		data = json.loads( html )
		       
		# {u'functions': [], u'name': u'mch-demo', u'variables': 
		# {u'reading': u'int32', u'temperature': u'double', u'voltage': u'double'}, 
		# u'connected': True, u'cc3000_patch_version': u'1.29', u'id': u'54xxxxxxxxxxxxxxxxxxxx67'}
		
		if( data['connected'] == False ):
			return ( False, None )
			
		return ( True, data )
				
	def api_manage_error( self, err ):
		""" Gere les cas d'erreur HTTP sur les appels d'API Spark Cloud.
		
		Certaines erreurs HTTP ont une signification particulière 
		lors d'un appel Spark Cloud. Dans ce cas, classe d'erreur 
		HTTPError est surclassée en SparkApiError pour contenir des 
		informations complémentaires (vachement pratique). """
		assert isinstance( err, HTTPError ), 'err must be HttpError type!'
		
		if( err.code in SPARK_HTTP_ERRORS ):
			# relancer l'erreur avec le texte d'aide !
			apierror = SparkApiError( err, SPARK_HTTP_ERRORS[err.code][1] )
			raise apierror
			 					
		# re-lancer l'exception
		raise err
		
	def api_get_access_tokens( self, spark_username, spark_password ):
		""" Obtenir la liste des access_token liés à votre compte Spark
		
		Parameters:
			spark_username (str) - votre compte utilisateur utilisé 
				sur Spark Cloud. Habituellement une adresse email
			spark_password (str) - votre mot de passe du compte spark
				cloud.
		
		Returns:
		retourne le tuple (connected, api_result) avec api_result tel
		que renvoyées par l'API Spark Cloud.
		S'il n'y a pas d'exception alors l'API est connectée... le 
		premier élément du tuple est toujours True.
		
		api_result est une liste de dictionnaire semblable à
		{'token': '12xxxxxxxxxxxxxxxxxxxxxxx75', 'client': 'spark', 
		  'expires_at': '2015-02-16T20:04:45.728Z'}
		  
		Remarks:
			Basic Authorization avec urllib en Python
			http://www.voidspace.org.uk/python/articles/authentication.shtml
		
		La structure tuple est utilisé pour rester consistant avec 
		les autres appels
		"""
		url = self.__api_base_url+'access_tokens'
		self.printdebug( url )
		
		base64UserPassword = base64.encodestring( '%s:%s' % (spark_username, spark_password) )[:-1]
		req = urllib2.Request( url ) # No DATA parameter
		# Ajout basic authorization à l'entête
		req.add_header( "Authorization", "Basic %s" % base64UserPassword )

		try:
			response = urllib2.urlopen(req)
		except HTTPError, err:
			if( err.code == 400 ):
				# Eviter le confusion de lecture sur erreur 400
				# relancer l'erreur avec le texte d'aide SPARK_HTTP_ERRORS 
				# orienté Core!
				apierror = SparkApiError( err, 'Spark Account may be invalid' )
				raise apierror				
			else:
				# gère les cas d'erreur Http Error et fait une surcharge si
				# approprié
				self.api_manage_error( err )
				
		html = response.read()
		data = json.loads( html )
		
		return ( True, data ) # No exception means API connected
		
	def api_create_access_token( self, spark_username, spark_password, client_id, client_pswd = None):
		""" Crée un nouvel access token pour votre compte spark. 

		Parameters:
			spark_username (str) - votre compte utilisateur utilisé 
				sur Spark Cloud. Habituellement une adresse email
			spark_password (str) - votre mot de passe du compte spark
				cloud.
				
			client_id (str) - Identification du client.
			client_pswd (str) - Mot de passe pour le client.
						Non utilisé par Spark pour le moment au moment
						de la création du token "client_id:client_id"
						sera utilisé comme recommandé dans la doc Spark.
		
		Returns:
		Retourne le tuple (connected, api_result) avec api_result tel
		que renvoyées par l'API Spark Cloud.
		S'il n'y a pas d'exception alors l'API est connectée... le 
		premier élément du tuple est toujours True. 
		
		Remarks:
		La structure tuple est utilisé pour rester consistant avec 
		les autres appels		
		"""
		url = SPARK_API_URL+'oauth/token' # pas de versionning pour cette URL!

		values = {'grant_type' : 'password',
			'username' : spark_username,
			'password' : spark_password }
		self.printdebug( 'POST to %s' % url )
		self.printdebug( values )
		data = urllib.urlencode(values)
				
		base64ClientPassword = base64.encodestring( '%s:%s' % (client_id, client_id if client_pswd == None else client_pswd) )[:-1]
		req = urllib2.Request( url, data ) 
		# Ajout basic authorization à l'entête
		req.add_header( "Authorization", "Basic %s" % base64ClientPassword )

		try:
			response = urllib2.urlopen(req)
		except HTTPError, err:
			if( err.code == 400 ):
				# Eviter le confusion de lecture sur erreur 400
				# relancer l'erreur avec le texte d'aide SPARK_HTTP_ERRORS 
				# orienté Core!
				apierror = SparkApiError( err, 'Spark Account may be invalid' )
				raise apierror				
			else:
				# gère les cas d'erreur Http Error et fait une surcharge si
				# approprié
				self.api_manage_error( err )
				
		html = response.read()
		data = json.loads( html )
		
		return ( True, data ) # No exception means API connected
		
	def api_delete_access_token( self,  spark_username, spark_password, access_token ):
		""" effacer un access token pour votre compte spark. 

		Parameters:
			spark_username (str) - votre compte utilisateur utilisé 
				sur Spark Cloud. Habituellement une adresse email
			spark_password (str) - votre mot de passe du compte spark
				cloud.
				
			access_token (str) - l'access token à effacer.
		
		Returns:
		Retourne le tuple (connected, api_result) avec api_result tel
		que renvoyées par l'API Spark Cloud.
		S'il n'y a pas d'exception alors l'API est connectée... le 
		premier élément du tuple est toujours True. 
		
		Remarks:
		La structure tuple est utilisé pour rester consistant avec 
		les autres appels		
		"""		
		url = self.__api_base_url+'access_tokens/'+access_token
		self.printdebug( url )
		
		base64UserPassword = base64.encodestring( '%s:%s' % (spark_username, spark_password) )[:-1]
		req = urllib2.Request( url ) # No DATA parameter
		# Ajout basic authorization à l'entête
		req.add_header( "Authorization", "Basic %s" % base64UserPassword )
		# Changer la methode en DELETE
		req.get_method = lambda: 'DELETE'
		try:
			response = urllib2.urlopen(req)
		except HTTPError, err:
			if( err.code == 400 ):
				# Eviter le confusion de lecture sur erreur 400
				# relancer l'erreur avec le texte d'aide SPARK_HTTP_ERRORS 
				# orienté Core!
				apierror = SparkApiError( err, 'Spark Account may be invalid' )
				raise apierror				
			else:
				# gère les cas d'erreur Http Error et fait une surcharge si
				# approprié
				self.api_manage_error( err )
		except BadStatusLine, err:
			apierror = SparkApiError( err, 'Maybe are you trying to drop the last created access_token!' )
			raise apierror
				
		html = response.read()
		data = json.loads( html )
		
		
		return ( True, data ) # No exception means API connected 
			
	def api_get_core_list( self ):
		""" Obtenir la liste des Cores liées au compte spark
		
		Returns: 
		Retourne le tuple (connected, api_result) avec api_result tel
		que renvoyées par l'API Spark Cloud.
		S'il n'y a pas d'exception alors l'API est connectée... le 
		premier élément du tuple est toujours True. 
		
		Remarks:
		La structure tuple est utilisé pour rester consistant avec 
		les autres appels
		"""	     
		url = self.__api_base_url+'devices/'+'?access_token='+self.__access_token
		self.printdebug( url )
		try:
			response = urllib2.urlopen( url )
		except HTTPError, err:
			# gère les cas d'erreur Http Error et fait une surcharge si
			# approprié
			self.api_manage_error( err )
				
		html = response.read()
		data = json.loads( html )
		       
		# [{u'connected': True, u'last_heard': u'2015-01-02T23:47:31.555Z', 
		# u'last_app': None, u'id': u'54xxxxxxxxxxxxxxxxxxx67', u'name': u'mch-demo'}]
					
		return ( True, data ) # Not Exception MEANS API is connected
			
	def core_list( self ):
		""" Obtenir une liste simplifiée des Cores liées au compte Spark.
		
		Returns:
		Compile le résultat de l'API Spark Cloud et construit une liste
		simplifiée avec l'identification des Cores et l'état de connexion
		tel que connu sur Spark Cloud [ (core_id, core_name, connected), ... ]"""	     
		content = self.api_get_core_list() 
		result = list()
		
		for aCore in content[1]:
			item = ( aCore['id'], aCore['name'], aCore['connected'] )
			result.append( item )
			
		return result
		
	def dump_core_list( self ):
		""" liste les cores sur le compte Spark Cloud et affiche
		le résultat sur l ecran."""
		cores = self.core_list()
		
		print( '%25s %23s %s' % ('Core ID', 'Core Name', 'Connecté?' ) )
		for core in cores:
			print( '%25s %23s %s' % ( core[0], core[1], core[2] ) ) 
		return
		
	def printdebug( self, sMsg ):
		""" Afficher le message sur la console si le mode de deboggage 
		est activé.
		ATTENTION: affiche aussi des informations sensibles, ne publiez 
		pas les messages de ddebug sur internet sans masquer vos 
		access_token et core_id!"""
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
	
	@property
	def api( self ):
		""" Renvoi une reference vers l'instance SparkApi. Permettra 
		l'écriture d'un code plus propre """
		return self.__owner
		
	@property
	def core_id( self ):
		""" Retourne le core_id """
		return self.__core_id
		
	def value_of( self, variable_name ):
		""" Interroge le core pour retrouver la valeur de la variable 
		variable_name.
		
		Args:
			variable_name (str) - Nom de la variable à retrouver
			
		returns:
			tuple (connecté,valeur/None) - permet de savoir si le Core
				est en ligne et la valeur de la variable"""
			
		assert isinstance( variable_name, basestring), 'variable_name must be str/unicode type' # basestring match str & unicode
		
		content = self.api.api_core_get_variable( self.__core_id, variable_name )
		return content

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
			    
		assert isinstance(function_name, basestring), 'function_name must be str/unicode type' # basestring match str & unicode
		assert isinstance(params, basestring), 'params must be str/unicode type' # basestring match str & unicode
		
		content = self.api.api_core_call_function( self.__core_id, function_name, params )
		
		return content

	def info( self ):
		""" obtenir les informations sur le core, tel que retrouné par
			l'API. Contient également les informations sur les 
			fonctions et variables publiées """
		content = self.api.api_core_get_info( self.__core_id )
		
		return content
		
	def dump_info( self ):
		""" Affiche les informations sur le core """
		content = self.info()
		
		if( content[0] == False ):
			print( 'Core not connected' )
			return 
		
		print( 'Core ID  : %s' % content[1]['id'] )
		print( 'Core Name: %s' % content[1]['name'] )
		print( 'Connected: %s (not always reliable)' % content[1]['connected'] ) 
		# Les variables sont contenue dans un dictionnaire.
		print( 'Variables:' )
		for varname,vartype in content[1]['variables'].iteritems(): # itération dictionnaire clé, valeur
			print ( '   %s - %s' % (varname,vartype) )
		print( 'functions:' )
		for func in content[1]['functions']:
			print ( '   %s' % (func) )

		# {u'functions': [], u'name': u'mch-demo', u'variables': {u'reading': u'int32', u'temperature': u'double', u'voltage': u'double'}, u'connected': True, u'cc3000_patch_version': u'1.29', u'id': u'54ff6c066667515111481467'}

class TinkerError( Exception ):
	""" Specific error class linked to SparkCoreTinker class """
	pass
	
class SparkCoreTinker( SparkCore ):
	""" Specialized class that can be used with Core running Tinker """
	
	__signatureChecked = False # permet de savoir si la signature de Tinker à bien été verifiée sur le core  
	
	def __init__( self, spark_api, core_id ):
		# Initialisation de la classe de base
		SparkCore.__init__( self, spark_api, core_id )
		# Initialisation locale
		__signatureChecked = False
		
	def check_tinker_signature( self ):
		""" verifie si le Core fait bien tourner Tinker.
		Si le test est déjà positif alors ne plus retester. """
		if self.__signatureChecked == True:
			return True
		
		# obtenir l'interface publiée sur le core
		info = self.api.api_core_get_info( self.core_id )
		if( info[0] == False ):
			# Core not connected -> retourner False
			return False
		
		# Verifier que les fonctions de Tinker soient bien présentes
		functions = info[1]['functions']
		try:
			functions.index('digitalread') # will raise exception if missing
			functions.index('digitalwrite') 
			functions.index('analogread')
			functions.index('analogwrite')
			
			self.__signatureChecked = True
		except ValueError:
			self.__signatureChecked = False

		# Faire le test de la signature
		return self.__signatureChecked
		
	def assert_tinker_signature( self ):
		""" Vérifie la signature de Tinker sur le Core sous forme 
		assertion """
		assert self.check_tinker_signature()==True, 'Tinker is not running on the Core' 
		
	def digitalread( self, pin_name ):
		""" permet de lire l'état d'une broche digitale via Tinker.
		
		Parameters:
			pin_name (str) - Nom de la broche sur Tinker (ex: D4)
		
		Returns:
			1 / 0 en fonction de l'état de la broche.
		"""
		self.assert_tinker_signature()
		
		value = self.call( 'digitalread', pin_name )
		if( value[0] == False ):
			raise TinkerError( 'Core is not connected!' )
		return value[1]  

	def digitalwrite( self, pin_name, activate ):
		""" permet de modifier l'état d'une broche digitale via tinker 
		
		Parameters:
			pin_name (str) - Nom de la broche sur Tinker (ex: D4)
			activate (bool) - activer/désactiver la broche
		
		Returns:
			Le résultat de la fonction digitalwrite() exécutée sur le core.
		"""
		self.assert_tinker_signature()
		
		value = self.call( 'digitalwrite', pin_name+','+('HIGH' if activate else 'LOW') )
		if( value[0] == False ):
			raise TinkerError( 'core is not connected!' )
		return value[1] 

	def analogread( self, pin_name ):
		""" permet de lire la valeur d'une des broches analogiques via tinker
		
		Parameters:
			pin_name (str) - nom de la broche analogique (ex: A0)
			
		Returns:
			Le résultat sous forme d'un entier entre 0 et 4095
		"""
		self.assert_tinker_signature()
		
		value = self.call( 'analogread', pin_name )
		if( value[0] == False ):
			raise TnikerError( 'core is not connected!' )
		return value[1]
		
	def analogread_voltage( self, pin_name ):
		""" Permet de lire la valeur EN VOLTS d'une broche analogique via 
		tinker.
		
		Parameters:
			pin_name (str) - nom de la broche analogique (ex: A0)
			
		Returns:
			Le résultat sous forme d'un entier entre 0 et 4095
		"""
		return (3.3 * self.analogread( pin_name ))/4095

	def analogwrite( self, pin_name, value ):
		""" Permet d'activer une sortie PWM sur le core (conformément
		au standard mis en place par le Framework Wiring dans Arduino).
		
		Parameters:
			pin_name (str) - nom de la broche pour laquelle le signal PWM
							 est activé. Voir graphe des broches sur 
							 http://mchobby.be/wiki/index.php?title=Spark-Core-Brochage
							 
			value (int) - représente le cycle utile (duty cycle) du signal
						  en 255ieme (ex: 128 -> 50% de cycle utile)
		"""
		assert 0 <= value <= 255, 'invalid PWM value' 
		
		self.assert_tinker_signature()
		
		value = self.call( 'analogwrite', pin_name+','+str(value) )
		if( value[0] == False ):
			raise TnikerError( 'core is not connected!' )
		return value[1]
