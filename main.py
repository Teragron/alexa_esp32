import network
import socket
import ujson
from machine import Pin
import time

# WiFi Credentials
SSID = "xx"
PASSWORD = "xx"

# LED Setup
LED_PIN = 2
led = Pin(LED_PIN, Pin.OUT)

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi", end="")
    for _ in range(10):  # Wait for max 5 seconds
        if wlan.isconnected():
            break
        print(".", end="")
        time.sleep(0.5)

    if wlan.isconnected():
        print("\nWiFi Connected:", wlan.ifconfig())
    else:
        print("\nFailed to connect to WiFi")

# Simple HTTP Server for Alexa
def start_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    print("Listening on", addr)

    while True:
        conn, addr = s.accept()
        print("Connection from:", addr)

        request = conn.recv(1024)
        request = str(request)
        print("Request:", request)

        # Serve XML for Alexa device discovery
        if "description.xml" in request:
            response = """HTTP/1.1 200 OK
Content-Type: text/xml

<?xml version="1.0"?>
<root>
    <device>
        <deviceType>urn:schemas-upnp-org:device:Basic:1</deviceType>
        <friendlyName>ESP32 Light</friendlyName>
        <manufacturer>ESPHome</manufacturer>
        <modelName>ESP32</modelName>
        <UDN>uuid:esp32-1234</UDN>
        <serviceList>
            <service>
                <serviceType>urn:schemas-upnp-org:service:SwitchPower:1</serviceType>
                <controlURL>/api</controlURL>
            </service>
        </serviceList>
    </device>
</root>"""
            conn.send(response)

        # Handle Alexa ON/OFF commands
        elif "/api" in request:
            if "on" in request:
                led.value(1)
                response = ujson.dumps({"status": "ON"})
            elif "off" in request:
                led.value(0)
                response = ujson.dumps({"status": "OFF"})
            else:
                response = ujson.dumps({"error": "Invalid Request"})

            conn.send("HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + response)

        conn.close()

# Run Everything
connect_wifi()
start_server()

