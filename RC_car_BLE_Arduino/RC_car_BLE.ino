/*
  NeOCampus RC Car

  The circuit:
  - Arduino MKR WiFi 1010, Arduino Uno WiFi Rev2 board, Arduino Nano 33 IoT,
    Arduino Nano 33 BLE, or Arduino Nano 33 BLE Sense board.

  You can use a generic BLE central app, like LightBlue (iOS and Android) or
  nRF Connect (Android), to interact with the services and characteristics
  created in this sketch.

  NeOCampus RcCar code ( Red BMW )
  Made for use on Arduino Nano 33 BLE Sense ( or Arduino Nano 33 BLE )
  
  ---- Compatible with Android application : BLE Simple Remote - Ferdinand Stueckler ----
  Author: Sebastian Lucas - 2019-2020
*/

#include "LedControl.h" //  need the library
LedControl lc=LedControl(11,13,10,1); // 

// pin 11 is connected to the MAX7219 pin 1
// pin 13 is connected to the CLK pin 13
// pin 10 is connected to LOAD pin 12
// 1 as we are only using 1 MAX7219

#include <ArduinoBLE.h>

BLEService carService("1101");
BLEWordCharacteristic carMove("2101", BLERead | BLEWrite);

unsigned long oldmillis = 0;
boolean TickTock = false;

void setup() {
  
Serial.begin(9600);

//Setup the control pins
pinMode(2, OUTPUT);
pinMode(3, OUTPUT);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);

//Led control setup
// the zero refers to the MAX7219 number, it is zero for 1 chip
lc.shutdown(0,false);// turn off power saving, enables display
lc.setIntensity(0,8);// sets brightness (0~15 possible values)
lc.clearDisplay(0);// clear screen

if (!BLE.begin()) 
{
Serial.println("starting BLE failed!");
while (1);
}

BLE.setLocalName("RCCar");
BLE.setAdvertisedService(carService);
carService.addCharacteristic(carMove);

BLE.addService(carService);

BLE.advertise();
Serial.println("Bluetooth device active, waiting for connections...");

}

void loop() {

  //Flash the back lights until we are connected
  if(millis() > oldmillis+1000)
  {
    TickTock = !TickTock;
    Serial.println("Toggling led col: 0, row 5");
    lc.setLed(0,0,5,TickTock); // turns on LED at col, row
    Serial.println("Toggling led col: 0, row 4");
    lc.setLed(0,0,4,TickTock); // turns on LED at col, row
    Serial.println("Toggling led col: 0, row 6");
    lc.setLed(0,0,6,TickTock); // turns on LED at col, row
    Serial.println("Toggling led col: 0, row 7");
    lc.setLed(0,0,7,TickTock); // turns on LED at col, row
    oldmillis=millis();
  }
  
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());

    //Flash leds to say we are connected
    
    //Turn on all the lights
    Serial.println("Toggling led col: 0, row 5");
    lc.setLed(0,0,5,true); // turns on LED at col, row
    Serial.println("Toggling led col: 0, row 4");
    lc.setLed(0,0,4,true); // turns on LED at col, row
    Serial.println("Toggling led col: 0, row 6");
    lc.setLed(0,0,6,true); // turns on LED at col, row
    Serial.println("Toggling led col: 0, row 7");
    lc.setLed(0,0,7,true); // turns on LED at col, row
    
    //Toggle the lights 3 times
    for (int led_counter = 0; led_counter < 3; led_counter++)
    {
      lc.shutdown(0,true);
      delay(100);
      lc.shutdown(0,false);
      delay(100);
    }

    //Turn off all the lights
    Serial.println("Turning off led col: 0, row 5");
    lc.setLed(0,0,5,false); // turns on LED at col, row
    Serial.println("Turning off led col: 0, row 4");
    lc.setLed(0,0,4,false); // turns on LED at col, row
    Serial.println("Turning off led col: 0, row 6");
    lc.setLed(0,0,6,false); // turns on LED at col, row
    Serial.println("Turning off led col: 0, row 7");
    lc.setLed(0,0,7,false); // turns on LED at col, row

    
    // while the central is still connected to peripheral:
    while (central.connected())
    {
      if (carMove.written())
      {
        //Forward
        if( (highByte(carMove.value()) < 100) && (highByte(carMove.value()) > 0) )
        {
          Serial.println("Car Forward, power: ");
          Serial.println(highByte(carMove.value()));
          analogWrite(3, ( (int)( ( (int)highByte(carMove.value()) )*2.55) ) ); // sets the digital pin 21 on

          //Turn on front lights
          Serial.println("Turning on led col: 0, row 6");
          lc.setLed(0,0,6,true); // turns on LED at col, row
          Serial.println("Turning on led col: 0, row 7");
          lc.setLed(0,0,7,true); // turns on LED at col, row
        }

        //Backward
        if( (highByte(carMove.value()) < 256) && (highByte(carMove.value()) > 156) )
        {
          Serial.println("Car Backward, power: ");
          Serial.println(highByte(carMove.value()));
          Serial.println(( (int) ((int) ( ( ( (-1)*highByte(carMove.value()) )+256)*2.55 ) )  ) );
          analogWrite(5, ( (int) ((int) ( ( ( (-1)*highByte(carMove.value()) )+256)*2.55 ) )  ) ); // sets the digital pin 23 on

          //Turn on back lights
          Serial.println("Turning on led col: 0, row 5");
          lc.setLed(0,0,5,true); // turns on LED at col, row
          Serial.println("Turning on led col: 0, row 4");
          lc.setLed(0,0,4,true); // turns on LED at col, row
        }

        //Left
        if( (lowByte(carMove.value()) < 256) && (lowByte(carMove.value()) > 156) )
        {
          Serial.println("Car Left, power: ");
          Serial.println(lowByte(carMove.value()));
          digitalWrite(4, HIGH); // sets the digital pin 20 on
        }

        //Right
        if( (lowByte(carMove.value()) < 100) && (lowByte(carMove.value()) > 0) )
        {
          Serial.println("Car Right, power: ");
          Serial.println(lowByte(carMove.value()));
          digitalWrite(2, HIGH); // sets the digital pin 22 on
        }

        //Stop
        if( (highByte(carMove.value()) == 0) && (lowByte(carMove.value()) == 0) )
        {
          Serial.println("Car Stopped, power: ");
          Serial.println(highByte(carMove.value()));
          digitalWrite(2, LOW);
          analogWrite(3, 0);
          digitalWrite(4, LOW);
          analogWrite(5, LOW);

          //Lights
          //Turn off back lights
          Serial.println("Turning off led col: 0, row 5");
          lc.setLed(0,0,5,false); // turns on LED at col, row
          Serial.println("Turning off led col: 0, row 4");
          lc.setLed(0,0,4,false); // turns on LED at col, row

           //Turn off front lights
          Serial.println("Turning off led col: 0, row 6");
          lc.setLed(0,0,6,false); // turns on LED at col, row
          Serial.println("Turning off led col: 0, row 7");
          lc.setLed(0,0,7,false); // turns on LED at col, row
          
        }
      }
    }

    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}
