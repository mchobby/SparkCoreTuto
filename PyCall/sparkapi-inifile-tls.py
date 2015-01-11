#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from sparkapi.sparkapi import SparkApi
""" sparkapi-inifile-tls.py

    This program will help you to collect the information to place
    in your sparkapi.ini file
"""

def main():
	print( 'This program will help you to grab the needed information' )
	print( 'to help you in creating the sparkapi.ini file ')
	print( '' )
	print( 'Spark Account needed to access such API' ) 
	user = raw_input( 'Your Spark Account: ' )
	passwd = raw_input( 'Your Spark Password: ' )	
	
	fake_access_token = '123456'
	user_access_token = None 
	# The access_token is not required when edit a list of the 
	# access_token from Spark_account
	api = SparkApi( access_token = fake_access_token, debug = False )
	result = api.api_get_access_tokens( user, passwd )
	access_token_list = result[1]
	for token in access_token_list:
		if( token['client'] == 'user' ):
			user_access_token = token['token']
			print( '[SPARK-API]' )
			print( 'access_token=%s' % user_access_token )
			print( '' )
			break
	
	if user_access_token == None:
		raise Exception( 'No access_token found for client_id = user' )
	
	api = None
	iIndex = 0
	api = SparkApi( access_token = user_access_token, debug = False )
	cores = api.core_list()
	print( '[CORES]' )
	for core in cores:
		print( '# core%i is named %s' % (iIndex, core[1]) ) # Core Name @ position 1
		print( 'core%i=%s' % (iIndex, core[0]) ) # Core ID @ position 0
		iIndex += 1 
		
		
	
	return 0
	
if __name__ == '__main__':
	main()
