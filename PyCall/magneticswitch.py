#!/usr/bin/env python
# -*- coding: utf8 -*-
#
"""magneticswitch.py

Appel d'API sur un Spark Core faisant fonctionner le programme
  magneticswitch.ino 
  
  Affiche la valeur du compteur (nombre d'ouverture). 
  Affiche l'état actuel du contact (contact reed).
  Demande un reset du compteur et force la relecture du contact sur
     le spark core lorsque sa valeur dépasse 5.

Copyright 2015 DMeurisse <info@mchobby.be>

Voir tutoriel:
   http://wiki.mchobby.be/index.php?title=Spark-Core-Switch-Magnetic
     
Ou acheter Spark Core -- et soutenir nos travaux --

   http://shop.mchobby.be/category.php?id_category=54

Ou acheter un contact magnetique

   http://shop.mchobby.be/category.php?id_category=60

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
  04 jan 2015 - Dominique - v 0.1 (première release)
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
	# Execute le programme qui récupère le nombre de pression sur 
	#  le Spark Core
	api = SparkApi( access_token = config.access_token, debug = False )
	# ou utiliser directement votre access_token
	#api = SparkApi( access_token = '123412341234', debug = False )
		
	# Créer un objet Core à partir du core_id 
	#   le core_id provient du fichier de configuration sparkapi.ini
	#   dans la section [CORES]
	core = api.get_core( config.cores['core0'] ) 
	# ou utiliser directement votre core_id
	#core = api.get_core( '0123456789abcdef' )
	
	# Lire une variable sur le core
	# retourne un tuple (connected, valeur)
	value = core.value_of( 'counter' )
	
	if( value[0] == False ):
		print( 'le Core n est pas connecté' )
	else:
		print( 'compteur = %i' % value[1] )
		close = core.value_of( 'close' ) # retourne le tuple (connected, close)
		print( 'Etat de la variable "close": %i ' % close[1] )
		print( 'Le contact est %s' % ('fermé' if close[1] == 1 else 'OUVERT' ) )
	
	# Si connecté et 'valeur > 5' ???
	if( value[0] and value[1]>5 ):
		print( 'Envoyer ordre "reset" compteur' )
		# Faire un reset du compteur sur le core.
		# En utilisant sa fonction "reset" publier sur Spark Cloud
		result = core.call( 'reset' ) 
		if( result[0] == False ):
			print( 'le Core n est pas connecté' )
		else:
			print( 'La fonction à répondu %i' % result[1] )
	
	return 0

if __name__ == '__main__':
	main()
