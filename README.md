# IoT Motherboard Switch
PC Motherboard Transistor Switch Operated by NodeMCU ESP8266

## Motivation
The IoT motherboard power switch was motivated by the need to remotely force-shutdown a GPU mining-rig to address
stability issues, when offsite. 

## Usage
A user with access to a mining-rig/computer/servers respective local network can activate the switch
by making a request to the socket web-server by visiting the button path and making a request via the OFF/ON button. 

## Installation
1) Flash NodeMCU ESP8266 with MicroPython 
2) Upload boot.py, main.py and passwords.txt (with local network name and password), via WebREPL
3) Built switch circuit on solderless breadboard (circuit diagram will be added)
4) Activate switch by visiting the http://your node mcu ip address:your port/button view.


