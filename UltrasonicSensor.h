#ifndef ULTRASONICSENSOR_H
#define ULTRASONICSENSOR_H

#include "Arduino.h"

 class UltrasonicSensor
{
  private:
    int pinEcho;
    int pinTrigger;
    int duration;
    int distance;

  public:
    UltrasonicSensor(int pinEcho, int pinTrigger);

    void SetPinEcho(int pinEcho) {this -> pinEcho = pinEcho;}
    void SetPinTrigger(int pinTrigger) {this -> pinTrigger = pinTrigger;}
    long GetDistance();
};

#endif
