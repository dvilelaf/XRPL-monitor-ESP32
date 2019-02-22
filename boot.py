# This file is executed on every boot (including wake-boot from deepsleep)
import XRPLmonitor
import sys
import machine

sys.path[1] = '/flash/lib'

def connect():

    import network
    import display

    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():

        print('Connecting to network...')

        # Connect
        sta_if.active(True)
        sta_if.connect('<WIFI_ESSID>', '<WIFI_PASSWORD>')
        
        # Wait until connection is established
        while not sta_if.isconnected():
            pass

    print('Network config:', sta_if.ifconfig())

    # Turn the led on
    led = machine.Pin(5, machine.Pin.OUT)
    led.value(0)

connect()
XRPLmonitor.run()