#!/usr/bin/python
#-*- encoding: utf8 -*-
""" Configuration management for PrestaConsole and others """

from ConfigParser import ConfigParser

CONFIG_FILENAME = 'sparkapi.ini'

# Sections names
CONFIG_SECTION_SPARK_API = 'SPARK-API'
CONFIG_SECTION_CORES     = 'CORES'

# Keynames for section SPARK-API
CONFIG_KEY_ACCESS_TOKEN = 'access_token'

class Config(object):
	"""read paramters from the "sparkapi.ini" configuration file"""
	_access_token = 'None'
	_cores = None # Liste de vos cores (pour ne pas les hardcoder dans votre programme) 

	
	def __init__( self ):
		config = ConfigParser()
		config.read( CONFIG_FILENAME )
		
		self._access_token = config.get( CONFIG_SECTION_SPARK_API, CONFIG_KEY_ACCESS_TOKEN )
		self._cores = dict( config.items( CONFIG_SECTION_CORES ) )
		
	@property
	def access_token( self ):
		""" l' Access_Token permet d'accéder à votre compte Spark Cloud"""
		return self._access_token

	@property
	def cores( self ):
		""" Liste de vos cores sous la forme de dictionnaire.
			Retourne une structure sous la forme:
			{'core0': '0123456789abcdef'} """
		return self._cores
