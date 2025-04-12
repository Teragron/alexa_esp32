Alexa ESP32

Easily control your ESP32 via Alexa or a web browser! This guide will help you set up and use your ESP32 with MicroPython.

--------------------------------------------------

🚀 How to Use the ESP32

1️⃣ Setting Up in Thonny IDE
1. Open Thonny IDE and connect your ESP32 via USB.
2. Select the correct USB Serial Port from:
   - Run → Configure Interpreter
3. Restart the backend by clicking:
   - Run → Stop/Restart Backend
4. Once the terminal opens, run the main.py script by clicking the Run Current Script button (▶️ green button).
5. Important: Before running, ensure you have configured the Wi-Fi SSID and password in the script.

--------------------------------------------------

🌐 Control via Web Browser

If your device is on the same network as the ESP32, you can turn the light ON/OFF using the following URLs:

🔹 Turn ON the Light:  
http://<ESP32_IP>/api?on

🔹 Turn OFF the Light:  
http://<ESP32_IP>/api?off

💡 Replace <ESP32_IP> with your actual ESP32 IP address (displayed in the terminal when the script runs).

--------------------------------------------------

🎯 Need Help?
If the COM is not visible on the device manager list make sure you are using a USB-Cable capable of transferring data
If the device is busy run the following command with the correct port and the correct firmware path inside a terminal after installing python and esptool:
```bash
python -m esptool --port COM4 write_flash 0x1000 ESP32_GENERIC-20241129-v1.24.1.bin
```
After the firmware update disconnect/connect the device to the same serial port on your pc
Enjoy your ESP32 smart home setup! 🚀💡
