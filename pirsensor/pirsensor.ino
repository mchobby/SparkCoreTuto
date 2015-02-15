// -------------------------------------------------
// Internet PIR - Détection de mouvement avec senseur PIR
// -------------------------------------------------
//
// Exemple didactique dont le but est:
// 1) De détecter l'activation d'un senseur PIR avec
//    avec déparasitage logiciel.
// 2) Reporte cette information dans une variable "counter" sur Spark Cloud
//    (le nombre de détection) permettant à un autre logiciel comme
//    un SmartPhone de détecter l'événement.
// 3) Reporte le statut actuel du senseur dans la variable "actif".
//    Permet de savoir si le senseur est actuellement actif. 
//    Pratique par exemple pour savoir s'il y a de l'activité dans une 
//    pièce (ex: surveiller un stock en pleine nuit).
// 3) Offrir une fonction "reset" sur Spark Cloud permettant
//    a un autre logiciel de remettre le compteur "counter" à zéro.
//    Force la relecture de l'entrée digital et la mise à jour
//    de la variable "actif"
//
// Voyez le tutoriel MCHobby
//   http://wiki.mchobby.be/index.php?title=Spark-Core-PIR
// Produit disponible chez MCHobby:
//   http://shop.mchobby.be/product.php?id_product=61
//
// Sortie du senseur PIR branché sur la broche D4
#define pirPin 4

// Créer une variable qui pour stocker la valeur
// du compteur de pression
int counter = 0; 

// Créer les variables internes au programme
int pirState; // etat du senseur PIR

/* Exécuté une fois au démarrage */
void setup()
{
  // Enregistrer la variable compteur sur Spark Cloud
  Spark.variable("counter", &counter, INT );
  // Publie l'état du contact  dans la variable "close" sur Spark Cloud
  Spark.variable("actif", &pirState, INT );
  
  // Enregistrer la fonction "reset compteur" sur Spark Cloud
  Spark.function("reset", resetCounter );
  
  // Active la broche D4 comme entrée
  pinMode(pirPin, INPUT);
  // lecture de l'état initial
  pirState = digitalRead( pirPin );
}

/* la fonction loop() est executée encore et encore */
void loop()
{
  int val, val2; // variable pour stocker la valeur lue sur la broche D4
  
  val = digitalRead( pirPin );
  delay( 10 ); // delai de 10ms pour déparasitage logiciel
  val2 = digitalRead( pirPin );
  
  // si val = val2 --> lecture de l'entrée est consistante
  // l'état de l'entrée est définit avec certitude... ce n'est pas 
  // un parasite.
  if( val == val2 ){ 
      
      // Si le contact a changé d'état? (passe du HIGH->LOW ou de LOW->HIGH)
      if( val != pirState ){
          
          // Si le PIR est actif
          if( val == HIGH ){
              
              counter = counter +1; // incrémenter le compteur
          }
          
          // Se souvenir du nouvel état de l'entrée
          pirState = val; 
      }
  
  }
  
}

// Cette fontion est appelée lorqu'il y a un appel correspondant sur l'API
// Pas de chaine de commande.
// a) Réinitialise le compteur "counter" à zéro.
// b) mise-à-jour de la variable actif. 
int resetCounter( String command ){
    counter = 0;
    
    // relecture de l'entrée
    pirState = digitalRead( pirPin );
    delay( 10 ); // déparasitage logiciel
    pirState = digitalRead( pirPin );
    
    return 1; // retour de valeur pour l'API
}
