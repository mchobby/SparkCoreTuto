// -------------------------
// Lecture de la température
// -------------------------
//
// Exemple didactique dont le but est:
// 1) De lire la température d'un senseur Analogique TMP36.
// 2) Reporte cette information dans une variable "temperature" sur Spark Cloud
// 3) Egalement reporter les autres variables servant au calcul.
//
// Voyez le tutoriel MCHobby
//   http://wiki.mchobby.be/index.php?title=Spark-Core-TMP36

// Senseur de température TMP36 branché sur la broche A0

// Créer une variable qui pour stocker la valeur
// de la température
double temperature = 0.0;
double voltage = 0.0;
int reading = 0;

void setup()
{
  // Enregistrer la variable sur Spark Cloud
  Spark.variable("temperature", &temperature, DOUBLE);
  Spark.variable("voltage", &voltage, DOUBLE );
  Spark.variable("reading", &reading, INT );
  // Active la broche A0 comme entrée (broche
  // sur laquelle le senseur de température est connecté)
  pinMode(A0, INPUT);
}

void loop()
{
  reading = 0;
  voltage = 0.0;

  // Lire continuellement la valeur du senseur. De sorte que
  // lorsque nous faison un appel sur l'API pour lire la valeur
  // nous obtenons la dernière valeur disponible.
  reading = analogRead(A0);

  // La lecture analogique retourne une valeur entre 0 et 4095
  // pour une tension entre 0 et 3.3V.
  // Calculer la tension correspondante 
  voltage = (reading * 3.3) / 4095;

  // Calculer la valeur de la température (formule pour un TMP36)
  // et stocker la valeur dans notre variable statique 'temperature'
  temperature = (voltage - 0.5) * 100;
}
