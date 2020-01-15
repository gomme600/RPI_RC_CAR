# NeOCampus RC CAR

NeOCampus RC car example code - both versions (Arduino and Raspberry Pi)
Author Sebastian Lucas - 2019-2020

The following document explains how the whole setup and protocole works
Both versions use the exact same protocole but support different functionality

Protocol:
We use 2 bytes to control the vehicule, the first one for left/right and the second one for fowards/backwards

The range of the positions (power) is between -100 and 100.

UP: 0, power
DOWN: 0, -power
LEFT: -power, 0
RIGHT: power, 0
STOP: 0, 0

For testing purposes we can use an Android / Windows 10 app called "BLE simple remote"
It is important to use the following settings:

  - Byte Mode: Enabled: Positions are transfered as bytes.

  - Zero: Enabled: Car will stop when releasing button.

  - Channel (Ch.): Disabled.
  
https://play.google.com/store/apps/details?id=com.ble.remote.simple&hl=fr
https://www.microsoft.com/fr-fr/p/bluetooth-le-simple-remote/9p83xqvgnbjx?activetab=pivot:overviewtab

# Photos

![Dev Board](/images/dev_board.png)
