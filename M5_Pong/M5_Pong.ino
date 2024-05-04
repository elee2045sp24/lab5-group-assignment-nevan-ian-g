#include "M5StickCPlus2.h"
#include <ArduinoMqttClient.h>
#include "WiFi.h"
//MQTT variables
const char broker[] = "mqtt.ugavel.com";
int mqtt_port = 1883;
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
const char powUp1_topic[] = "ugaelee2045sp24/ikg61117/powUp1";

void setup() {
  pinMode(4, OUTPUT); // Set HOLD pin 04 as output
  digitalWrite(4, HIGH);  //IMPORTANT, Set HOLD pin to high to maintain power supply or M5StickCP2 will turn off
  auto cfg = M5.config();
  StickCP2.begin(cfg);
  //connectWifi(); // runs a captive portal (very opinionated)
  //connectToEnterpriseWifi(); // note, must modify SimpleWifi.ino
  connectToPersonalWifi(); //this launches an opinionated wifi setup (see WiFiParts.ino)
  StickCP2.Display.clear(); //clear stuff from wifi connect

  //MQTT setup
  mqttClient.onMessage(onMqttMessage);
  mqttClient.setUsernamePassword("class_user", "class_password");
  mqttClient.connect(broker, mqtt_port);
  mqttClient.subscribe(powUp1_topic);

  Serial.println("Setup finished");

}

void loop() {
  auto imu_update = StickCP2.Imu.update();
  mqttClient.poll(); 
  StickCP2.update(); 
  if(StickCP2.BtnA.wasPressed()){                      //if button pressed, send message on fire topic to main.py
    mqttClient.beginMessage(powUp1_topic);
    mqttClient.print("player_1");            //change to "player_2" for second stick
    mqttClient.endMessage();
  }
}

void onMqttMessage(int messageSize) {
  Serial.print("Received a message from topic '");
  Serial.print(mqttClient.messageTopic());
  Serial.print("', length ");
  Serial.print(messageSize);
  Serial.println(" bytes:");
  if (mqttClient.messageTopic() == powUp1_topic) {
      Serial.println(mqttClient.readString()); 
  }
}