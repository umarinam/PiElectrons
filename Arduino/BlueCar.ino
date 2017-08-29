#define LED 13  // Pin 13 has built in resistor so we can directly attach LED to ground
#define LED_FWD 7
#define LED_RVS 6
#define LED_LFT 5
#define LED_RGT 4

  char incomingByte;
  void ResetAll()
{
  digitalWrite(LED_FWD, LOW);
  digitalWrite(LED_RVS, HIGH);
  digitalWrite(LED_LFT, LOW);
  digitalWrite(LED_RGT, HIGH);
}


void setup() {
  // put your setup code here, to run once:
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);

  // Set the digital pin as output
  pinMode(LED, OUTPUT);
  pinMode(LED_FWD, OUTPUT);
  pinMode(LED_RVS, OUTPUT);
  pinMode(LED_LFT, OUTPUT);
  pinMode(LED_RGT, OUTPUT);

  ResetAll();
}

void Forward (bool bState)
{
  if ( bState )
    digitalWrite(LED_FWD, HIGH);
  else
    digitalWrite(LED_FWD, LOW);
}

void Reverse (bool bState)
{
  if ( bState )
    digitalWrite(LED_RVS, LOW);
  else
    digitalWrite(LED_RVS, HIGH);
}

void Left (bool bState)
{
  if ( bState )
    digitalWrite(LED_LFT, HIGH);
  else
    digitalWrite(LED_LFT, LOW);

}

void Right (bool bState)
{
  if ( bState )
    digitalWrite(LED_RGT, LOW);
  else
    digitalWrite(LED_RGT, HIGH);

}



void loop() {
  // put your main code here, to run repeatedly:

  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    switch (incomingByte) {
      case '0':
        Forward(false);
        break;
      case '1':
        Forward(true);
        break;
      case '2':
        Reverse(false);
        break;
      case '3':
        Reverse(true);
        break;
      case '4':
        Left(false);
        break;
      case '5':
        Left(true);
        break;
      case '6':
        Right(false);
        break;
      case '7':
        Right(true);
        break;
      default :
        ResetAll();
        break;
    }
  }
}

