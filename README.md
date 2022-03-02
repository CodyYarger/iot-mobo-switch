## IoT Motherboard Switch
PC Motherboard Transistor Switch Operated by NodeMCU ESP8266 microcontroller running MicroPython hosting a socket web server.

### Motivation
The IoT motherboard power switch was motivated by the need for capability to remotely force-shutdown/startup a headless server for situations where the system becomes unstable, and unresponsive, and the user is offsite. The switch can serve any motherboard power terminals.

### Usage
A user with access to a computer/servers respective local network can activate the switch by making a request to the socket web-server by visiting the button path (see 4) of Installation) and making a request via the OFF/ON button.

### Installation
1) Flash NodeMCU ESP8266 with MicroPython (firmware: esp8266-20180511-v1.9.4.bin )
https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html

2) Upload boot.py, main.py and passwords.txt (with local network name and password) to the NodeMCU,
via WebREPL: https://github.com/micropython/webrepl

3) Build switch circuit on solderless breadboard (see circuit diagram below).

4) Activate switch by visiting the (http:// YOUR NODE MCU IP ADDRESS:8080/button) view.

### Circuit Diagram
<p align="center">
  <img src="/images/diagram.png" alt="Diagram" style="height:auto; width:600px;"/>
  <div align="center">Figure 1: IoT Switch Circuit Diagram</div>
</p>
<br>

### Mobile UI Preview
<p align="center">
  <img src="/images/mobile.png" alt="mobile" style="height:400px; width:auto;"/>
  <div align="center">Figure 2: Mobile User Interface Preview</div>
</p>
