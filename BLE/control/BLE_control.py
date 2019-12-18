#!/usr/bin/env python

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
import time
import sys
import cv2
import dbus, dbus.mainloop.glib
import subprocess
import threading
import multiprocessing
from gi.repository import GObject
from example_advertisement import Advertisement
from example_advertisement import register_ad_cb, register_ad_error_cb
from example_gatt_server import Service, Characteristic
from example_gatt_server import register_app_cb, register_app_error_cb
from auto_drive import auto_drive

'''car control setup'''
GPIO.setmode(GPIO.BOARD)  # choose BCM or BOARD numbering schemes. We use BOARD  
  
GPIO.setup(38, GPIO.OUT) # set GPIO 38 as an output.  
GPIO.setup(36, GPIO.OUT) # set GPIO 36 as an output.
GPIO.setup(31, GPIO.OUT) # set GPIO 31 as an output.
GPIO.setup(29, GPIO.OUT) # set GPIO 29 as an output.

FR = GPIO.PWM(38, 1000)    # create an object for PWM on port 38 at 1000 Hertz
BR = GPIO.PWM(36, 1000)    # create an object for PWM on port 36 at 1000 Hertz
FL = GPIO.PWM(29, 1000)    # create an object for PWM on port 29 at 1000 Hertz
BL = GPIO.PWM(31, 1000)    # create an object for PWM on port 31 at 1000 Hertz  
                        # you can have more than one of these, but they need  
                        # different names for each port   
                        # e.g. p1, p2, motor, servo1 etc.
 
BLUEZ_SERVICE_NAME =           'org.bluez'
DBUS_OM_IFACE =                'org.freedesktop.DBus.ObjectManager'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
GATT_MANAGER_IFACE =           'org.bluez.GattManager1'
GATT_CHRC_IFACE =              'org.bluez.GattCharacteristic1'
UART_SERVICE_UUID =            '00001101-0000-1000-8000-00805f9b34fb'
UART_RX_CHARACTERISTIC_UUID =  '00002101-0000-1000-8000-00805f9b34fb'
UART_TX_CHARACTERISTIC_UUID =  '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
LOCAL_NAME =                   'RCCAR-PI'
mainloop = None

''' 
class TxCharacteristic(Characteristic):
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, UART_TX_CHARACTERISTIC_UUID,
                                ['notify'], service)
        self.notifying = False
        GObject.io_add_watch(sys.stdin, GObject.IO_IN, self.on_console_input)
 
    def on_console_input(self, fd, condition):
        s = fd.readline()
        if s.isspace():
            pass
        else:
            self.send_tx(s)
        return True
 
    def send_tx(self, s):
        if not self.notifying:
            return
        value = []
        for c in s:
            value.append(dbus.Byte(c.encode()))
        self.PropertiesChanged(GATT_CHRC_IFACE, {'Value': value}, [])
 
    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
 
    def StopNotify(self):
        if not self.notifying:
            return
        self.notifying = False
''' 
class RxCharacteristic(Characteristic):

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, UART_RX_CHARACTERISTIC_UUID,
                                ['write'], service)
    def bytes(num):
        return hex(num >> 8), hex(num & 0xFF)    

    def WriteValue(self, value, options):
       
        try:
            global auto_drive_on
            auto_drive_on = False
            print("------")
            print("Data Received !")
            print("------")
            #print('remote: {}'.format(bytearray(value).decode()))
            #print("is str")

            #print(value)
            #print("is raw")        
            
            lowb = int(value[0])
            highb = int(value[1])
            if((highb < 100) and (highb > 0)):
                if (auto_drive_on == True):
                    auto_drive_on = False
                    x.join() 
                    print("Autonomous mode off !")

                print("Fowards !")
                FR.stop()
                FL.stop()
                BR.stop()
                BL.stop()
                power = highb
                print("Power : ")
                print(power)
                FR.start(power)
                FL.start(power)

            if( (highb < 256) and (highb > 156) ):
                if (auto_drive_on == True):
                    auto_drive_on = False
                    x.join() 
                    print("Autonomous mode off !")

                print("Backwards !")
                FR.stop()
                FL.stop()
                BR.stop()
                BL.stop()
                power = (((-1)*highb)+256)
                print("Power : ")
                print(power)
                BR.start(power)
                BL.start(power)

            if( (lowb < 256) and (lowb > 156) ):
                if (auto_drive_on == True):
                    auto_drive_on = False
                    x.join() 
                    print("Autonomous mode off !")

                print("Left !")
                FR.stop()
                FL.stop()
                BR.stop()
                BL.stop()
                power = (((-1)*lowb)+256)
                print("Power : ")
                print(power)
                FR.start(power)
                BL.start(power)

            if( (lowb < 100) and (lowb > 0) ):
                if (auto_drive_on == True):
                    auto_drive_on = False
                    x.join() 
                    print("Autonomous mode off !")

                print("Right !")
                FR.stop()
                FL.stop()
                BR.stop()
                BL.stop()
                power = lowb
                print("Power : ")
                print(power)
                BR.start(power)
                FL.start(power)

            if( (highb == 0) and (lowb == 0) ):
                if (auto_drive_on == True):
                    auto_drive_on = False
                    x.join() 
                    print("Autonomous mode off !")    

                print("Stop !")
                FR.stop()
                FL.stop()
                BR.stop()
                BL.stop()

            if( (highb == 100) ):
                if (auto_drive_on == True):
                   auto_drive_on = False
                   x.join() 
                   print("Autonomous mode off !")  

                print("Autonomous !")
                FR.stop()
                FL.stop()
                BR.stop()
                BL.stop()
                auto_drive_on = True
                x = threading.Thread(target=auto_drive, args=(FR,FL,BR,BL,lambda : auto_drive_on,))
                x.daemon = True
                x.start()

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
 
class UartService(Service):
    def __init__(self, bus, index):
        Service.__init__(self, bus, index, UART_SERVICE_UUID, True)
        #self.add_characteristic(TxCharacteristic(bus, 0, self))
        self.add_characteristic(RxCharacteristic(bus, 1, self))
 
class Application(dbus.service.Object):
    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)
 
    def get_path(self):
        return dbus.ObjectPath(self.path)
 
    def add_service(self, service):
        self.services.append(service)
 
    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
        return response
 
class UartApplication(Application):
    def __init__(self, bus):
        Application.__init__(self, bus)
        self.add_service(UartService(bus, 0))
 
class UartAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(UART_SERVICE_UUID)
        self.add_local_name(LOCAL_NAME)
        self.include_tx_power = True
''' 
def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()
    for o, props in objects.items():
        for iface in (LE_ADVERTISING_MANAGER_IFACE, GATT_MANAGER_IFACE):
            if iface not in props:
                continue
        return o
    return None
'''

def find_adapter(bus):

    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if LE_ADVERTISING_MANAGER_IFACE in props:
            return o

    return None

def main():
    global mainloop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    adapter = find_adapter(bus)
    if not adapter:
        print('BLE adapter not found')
        return
 
    service_manager = dbus.Interface(
                                bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                GATT_MANAGER_IFACE)
    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)
 
    app = UartApplication(bus)
    adv = UartAdvertisement(bus, 0)
 
    mainloop = GObject.MainLoop()
 
    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
    ad_manager.RegisterAdvertisement(adv.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)
    try:
        mainloop.run()
    except KeyboardInterrupt:
        adv.Release()
 
if __name__ == '__main__':
    main()
