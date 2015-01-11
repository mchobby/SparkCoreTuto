#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""core-tinkering.py

Appel d'API sur un Spark Core faisant fonctionner le programme
  tinker. 
  
  Permet d'utiliser les fonctions exposées par tinker. 
  Permet de voir comment instancier une class dérivée de SparkCore et
    comment y implenter des fonctionnalités spécialisées.

Copyright 2015 DMeurisse <info@mchobby.be>

Voir tutoriel:
  http://mchobby.be/wiki/index.php?title=Spark-Python-Call
     
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
  02 jan 2015 - Dominique - v 0.1 (première release)
"""  
from sparkapi.sparkapi import SparkApi
from sparkapi.sparkapi import SparkCoreTinker
from sparkapi.config import Config 
import time

# Ouvre le fichier sparkapi.ini pour éviter de Hard Coder des données
# sensible comme l'access_token dans les programmes d'exemple publié sur
# le Net.
# 
# Créez votre propre fichier sparkapi.ini à partir du fichier 
# sparkapi-sample.ini
config = Config()


def main():
	# Execute le programme interroge le core faisant fonctionner  
	# le programme Tinker
	api = SparkApi( access_token = config.access_token, debug = False )
	# ou utiliser directement votre access_token
	#api = SparkApi( access_token = '123412341234', debug = False )
	
	# Créer un objet Core SPECIFIQUE à partir du core_id 
	#   le core_id provient du fichier de configuration sparkapi.ini
	#   dans la section [CORES]
	core = api.get_core_by_class( config.cores['core0'], SparkCoreTinker )
	# ou utiliser directement votre core_id
	#core = api.get_core_by_class( '0123456789abcdef', SparkCoreTinker )
	
	print( '--- Utilisation de la classe SparkCoreTinker ---' )
	# Lire l'état de la broche 4
	print( "digitalread D4 = %i" % core.digitalread( 'D4' ) )
	
	# Active la broche D0 pendant une seconde puis la désactiver
	print( "digitalwrite D1 HIGH = %i" % core.digitalwrite( 'D0', True ) )
	time.sleep( 1 )
	print( "digitalwrite D1 LOW = %i" % core.digitalwrite( 'D0', False ) )
	
	# Lecture d'une broche analogique
	print( "analogread A0 = %i" % core.analogread( 'A0' ) )
	print( "analogread A0 = %f volts" % core.analogread_voltage( 'A0' ) )
	
	# PWM de la broche D0 par pas increment de 25
	for iPwm in range( 0, 255, 50): # de 0 à 250 (inclus) par pas de 50
		print( 'PWM D0 a %i. analogwrite = %i' % ( iPwm, core.analogwrite( 'D0', iPwm ) ) )
		time.sleep( 2 ) # attendre 2 secondes
	# eteindre la broche D0
	print( 'Extinction D0. digitalwrite D0 LOW = %i' % core.digitalwrite( 'D0', False ) ) 
	
	print( '--- appeler directement les fonctions Tinker ---' )
	# Faire une lecture en appelant directement la fonction d'API
	#   "digitalread" de Tinker sur le Spark Core
	# retourne un tuple (connected, resultat_de_la_fonction)
	value = core.call( 'digitalread', 'D4' )
	print(  'le Core n est pas connecté' if value[0] == False else 'la fonction digitalread à répondu = %i' % value[1] )
	time.sleep( 2 )
		
	return 0

if __name__ == '__main__':
	main()
