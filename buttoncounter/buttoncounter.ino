// -------------------------------------------------
// Internet ButtonCounter - Compteur Bouton Internet
// -------------------------------------------------
//
// Exemple didactique dont le but est:
// 1) De détecter la pression d'un bouton, relais reed ou autre senseur
//    a contact franc (avec déparasitage logiciel).
// 2) Reporte cette information dans une variable "counter" sur Spark Cloud
//    (le nombre de pressions) permettant à un autre logiciel comme
//    un SmartPhone de détecter l'événement.
// 3) Offrir une fonction "reset" sur Spark Cloud permettant
//    a un autre logiciel de remettre le compteur "counter" à zéro?
//
// Voyez le tutoriel MCHobby
//   http://wiki.mchobby.be/index.php?title=Spark-Core-Bouton

// bouton branché sur la broche D4
#define btnPin 4

// Créer une variable qui pour stocker la valeur
// du compteur de pression
int counter = 0; 

// Créer les variables internes au programme
int buttonState; // etat du bouton

/* Exécuté une fois au démarrage */
void setup()
{
  // Enregistrer la variable compteur sur Spark Cloud
  Spark.variable("counter", &counter, INT );
  
  // Enregistrer la fonction "reset compteur" sur Spark Cloud
  Spark.function("reset", resetCounter );
  
  // Active la broche D4 comme entrée
  pinMode(btnPin, INPUT);
  // lecture de l'état initial
  buttonState = digitalRead( btnPin );
}

/* la fonction loop() est executée encore et encore */
void loop()
{
  int val, val2; // variable pour stocker la valeur lue sur la broche D4
  
  val = digitalRead( btnPin );
  delay( 10 ); // delai de 10ms pour déparasitage logiciel
  val2 = digitalRead( btnPin );
  
  // si val = val2 --> lecture de l'entrée est consistante
  // l'état de l'entrée est définit avec certitude... ce n'est pas 
  // un parasite.
  if( val == val2 ){ 
      
      // Si le bouton a changé d'état? (passe du HIGH->LOW ou de LOW->HIGH)
      if( val != buttonState ){
          
          // Si le bouton est pressé
          if( val == HIGH ){
              
              counter = counter +1; // incrémenter le compteur
          }
          
          // Se souvenir du nouvel état du bouton
          buttonState = val; 
      }
  
  }
  
}

// Cette fontion est appelée lorqu'il y a un appel correspondant sur l'API
// Pas de chaine de commande.
// Réinitialise le compteur "counter" à zéro
int resetCounter( String command ){
    counter = 0;
    return 1; // retour de valeur pour l'API
}
