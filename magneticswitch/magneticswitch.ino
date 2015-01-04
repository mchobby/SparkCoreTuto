// -------------------------------------------------
// Internet Magnetic - Détection d'ouverture de contact Reed
// -------------------------------------------------
//
// Exemple didactique dont le but est:
// 1) De détecter l'ouverture de contact reed (switch magnetic) avec
//    avec déparasitage logiciel.
// 2) Reporte cette information dans une variable "counter" sur Spark Cloud
//    (le nombre d'ouverture) permettant à un autre logiciel comme
//    un SmartPhone de détecter l'événement.
// 3) Reporte le statut actuel du senseur dans la variable "close".
//    Permet de savoir si le contact/porte est fermé. 
//    Pratique par exemple pour la cabane de jardin, chambre froide, 
//    box du cheval (s'il est de sortie... donc porte ouverte), etc
// 3) Offrir une fonction "reset" sur Spark Cloud permettant
//    a un autre logiciel de remettre le compteur "counter" à zéro.
//    Force la relecture de l'entrée digital et la mise à jour
//    de la variable "open"
//
// Voyez le tutoriel MCHobby
//   http://wiki.mchobby.be/index.php?title=Spark-Core-Switch-Magnetic
// Produit disponible chez MCHobby:
//   http://shop.mchobby.be/product.php?id_product=60
//
// contact magnétique/contact reed branché sur la broche D4
#define btnPin 4

// Créer une variable qui pour stocker la valeur
// du compteur de pression
int counter = 0; 

// Créer les variables internes au programme
int contactState; // etat du bouton

/* Exécuté une fois au démarrage */
void setup()
{
  // Enregistrer la variable compteur sur Spark Cloud
  Spark.variable("counter", &counter, INT );
  // Publie l'état du contact  dans la variable "close" sur Spark Cloud
  Spark.variable("close", &contactState, INT );
  
  // Enregistrer la fonction "reset compteur" sur Spark Cloud
  Spark.function("reset", resetCounter );
  
  // Active la broche D4 comme entrée
  pinMode(btnPin, INPUT);
  // lecture de l'état initial
  contactState = digitalRead( btnPin );
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
      
      // Si le contact a changé d'état? (passe du HIGH->LOW ou de LOW->HIGH)
      if( val != contactState ){
          
          // Si le contact est ouvert
          if( val == LOW ){
              
              counter = counter +1; // incrémenter le compteur
          }
          
          // Se souvenir du nouvel état de l'entrée
          contactState = val; 
      }
  
  }
  
}

// Cette fontion est appelée lorqu'il y a un appel correspondant sur l'API
// Pas de chaine de commande.
// a) Réinitialise le compteur "counter" à zéro.
// b) mise-à-jour de la variable open.
int resetCounter( String command ){
    counter = 0;
    
    // relecture de l'entrée
    contactState = digitalRead( btnPin );
    delay( 10 ); // déparasitage logiciel
    contactState = digitalRead( btnPin );
    
    return 1; // retour de valeur pour l'API
}
