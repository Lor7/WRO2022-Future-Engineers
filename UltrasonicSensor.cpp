#include "UltrasonicSensor.h"

UltrasonicSensor::UltrasonicSensor(int pinEcho, int pinTrigger) {
  this -> pinEcho = pinEcho;
  this -> pinTrigger = pinTrigger;

  pinMode(pinTrigger, OUTPUT);
  pinMode(pinEcho, INPUT);
}

/**
 * brief This method return the distance measured by the sensor
 * return the distance value in centimeters
 */
long UltrasonicSensor::GetDistance() {
  // Set the trigger output LOW
  digitalWrite(pinTrigger, LOW);
  // Set the trigger output to HIGH for 10 microseconds
  digitalWrite(pinTrigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrigger, LOW);
  
  // Detect the time to return using the pulseIn function
  long duration = pulseIn(pinEcho, HIGH);
  long distance = duration / 58.31;

  return distance;
}
