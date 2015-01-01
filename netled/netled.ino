// -------------------------------------------------
// Net Led - Commande de LED via Internet
// -------------------------------------------------
//
// Exemple didactique dont le but est:
// 1) De commander 2 LED via Internet (sortie digitale sur le Core).
// 2) Se familiariser avec la publication de fonction sur SPARK CLOUD
// 3) Faire des appels de fonction avec paramètres sur votre CORE 
//    via Spark Cloud
// 4) Récuperer le résultat de la fonction exécutée sur votre Spark core
//
// Voyez le tutoriel MCHobby
//   http://wiki.mchobby.be/index.php?title=Spark-Core-NetLED

// LEDs branchées sur les broches D0 et D1, voir tutoriel 
// pour le cablage.

// Donner un nom aux broches
int led1 = D0;
int led2 = D1;

void setup() {
    // Enregistrez votre fonction Spark ici
   // Le point de contact de l'API est "led" et la 
   // fonction appelée est "ledControl"
   Spark.function("led", ledControl);

   // Configureer les broches en Sortie (output)
   pinMode(led1, OUTPUT);
   pinMode(led2, OUTPUT);

   // Initialiser les deux LEDs pour qu'elles soient éteintes
   digitalWrite(led1, LOW);
   digitalWrite(led2, LOW);

}

void loop() {
  // rien à faire dans loop
}

// Cette fonction est appelée lorsqu'il y a un appel correspondant sur l'API
// Le format de la chaine de commande est l<numero de led>,<état>
// Par exemple: l1,HIGH ou l1,LOW  pour allumer ou éteindre la LED1
//              l2,HIGH or l2,LOW  pour allumer ou éteindre la LED2
//
int ledControl(String command)
{
   int state = 0;
   // Trouver le numéro de broche dans la commande ET convertir 
   // la valeur du caractere ASCII en valeur entière (en integer)
   int pinNumber = (command.charAt(1) - '0') - 1;

   // Vérifier que la valeur de la broche est bien dans
   // les limites acceptables SINON on quitte de la fonction ledControl
   if (pinNumber < 0 || pinNumber > 1) return -1;

   // Trouver l'état de la Led dans la commande
   // SI l'état n'est pas identifié ALORS on quitte la fonction ledControl
   if(command.substring(3,7) == "HIGH") state = 1;
   else if(command.substring(3,6) == "LOW") state = 0;
   else return -1;

   // Modifier l'état de la broche 
   digitalWrite(pinNumber, state);
   return 1;
}
