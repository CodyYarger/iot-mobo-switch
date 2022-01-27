# start webrepl
import machine
import time
import network
import gc
import webrepl
webrepl.start()
gc.collect()

# instantiate station object to connect to router
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# print network settings of interface
print(ap_if.ifconfig())

# read passwords.txt file
try:
    with open("passwords.txt") as f:
        connections = f.readlines()
except OSError:
    print("No passwords.txt file!")
    connections = []

# for connections in passwords.txt try to connect
for connection in connections:
    station, password = connection.split()

    print("Connecting to {}.".format(station))

    sta_if.connect(station, password)

    for i in range(15):
        print(".")

        if sta_if.isconnected():
            break

        time.sleep(1)

    if sta_if.isconnected():
        break
    else:
        print("Connection could not be made.\n")
