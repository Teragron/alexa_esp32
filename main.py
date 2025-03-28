import network
import ujson
import socket
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
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)

    print("\nWiFi Connected:", wlan.ifconfig())

# Simple HTTP Server to handle Alexa and browser requests
def start_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    print("Listening on", addr)

    while True:
        conn, addr = s.accept()
        print("Connection from:", addr)

        request = conn.recv(1024).decode("utf-8")
        print("Request:", request)

        # Extract the requested path
        first_line = request.split("\n")[0]  # First line of HTTP request
        path = first_line.split(" ")[1]      # Extract path after GET

        response = ""

        # Check if the request is for turning the LED on/off
        if "/api" in path:
            if "on" in path:
                led.value(1)
                response = ujson.dumps({"status": "ON"})
            elif "off" in path:
                led.value(0)
                response = ujson.dumps({"status": "OFF"})
            else:
                response = ujson.dumps({"error": "Invalid Request"})

        # Send HTTP response
        conn.send("HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + response)
        conn.close()

# Run Everything
connect_wifi()
start_server()

