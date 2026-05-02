#define BLYNK_PRINT Serial
#define BLYNK_TEMPLATE_ID "TMPL3pdLhLo_a"
#define BLYNK_TEMPLATE_NAME "PLANT STRESS LANGUAGE DECODER"
#define BLYNK_AUTH_TOKEN "thA5Vc7-J4UzBeOhx43z2EDtSy5pT0cJ"

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <SimpleTimer.h>
#include <DHT.h>

char auth[] = "thA5Vc7-J4UzBeOhx43z2EDtSy5pT0cJ";
char ssid[] = "Galaxy A14 5G 041E";
char pass[] = "Priya Jeni";

#define DHTPIN 2
#define DHTTYPE DHT11
#define SOIL_PIN A0
#define RAIN_PIN 16

DHT dht(DHTPIN, DHTTYPE);
SimpleTimer timer;

void sendSensor()
{
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  int soilValue = analogRead(SOIL_PIN);
  int rainValue = digitalRead(RAIN_PIN);

  if (!isnan(humidity) && !isnan(temperature))
  {
    Blynk.virtualWrite(V0, temperature);
    Blynk.virtualWrite(V1, humidity);
  }

  Blynk.virtualWrite(V2, soilValue);

  if (rainValue == LOW)
  {
    Blynk.virtualWrite(V3, 1);
    Serial.println("Rain Detected");
  }
  else
  {
    Blynk.virtualWrite(V3, 0);
    Serial.println("No Rain");
  }

  Serial.print("Temp: ");
  Serial.println(temperature);

  Serial.print("Humidity: ");
  Serial.println(humidity);

  Serial.print("Soil: ");
  Serial.println(soilValue);
}

void setup()
{
  Serial.begin(9600);

  pinMode(RAIN_PIN, INPUT);

  dht.begin();

  Blynk.begin(auth, ssid, pass);

  timer.setInterval(2000L, sendSensor);
}

void loop()
{
  Blynk.run();
  timer.run();
}