"""
This module contains a MicroPython webserver for the NodeMCU microcontroller that
interfaces a PC motherboard. The 'button' view can be accessed by the user to close
a transistor switch, executing a forced shutdown or startup of a computer.
"""
# pylint: disable=E0001
# pylint: disable=C0103
# pylint: disable=W0612


# import modules
try:
    import machine
    import usocket as socket
    from time import sleep
except:
    import socket

response_404 = """
HTTP/1.0 404 NOT FOUND

<h1>404 Not Found</h1>
"""

response_500 = """
HTTP/1.0 500 INTERNAL SERVER ERROR

<h1>500 Internal Server Error</h1>
"""

response_template = """HTTP/1.0 200 OK

%s
"""


def button():
    """ button view for power switch activation via request """
    body = """
<head>
<title>IoT PC Switch</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
h1{color: #0F3376; padding: 2vh;}p {font-size: 1.5rem;}
.button{width: 400px; display: inline-block; background-color: #A9A9A9; border: none;border-radius: 4px;
padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style>
</head>
<body>

<h1>IoT Motherboard Switch</h1>

<p>
<a href="/power=on">
<button id = "pwr" onclick= "color();label()" class="button">---- STARTUP ----</button>
</a>
</p>

<script>
function label() {document.getElementById("pwr").innerHTML = "---- POWERING ON ----";}
</script>

<p>
<a href="/power=off">
<button id = "pwroff" onclick= "color();label1()" class="button">--- SHUTDOWN ---</button>
</a>
</p>

<script>
function label1() {document.getElementById("pwroff").innerHTML = "---- POWERING OFF ----";}
</script>
</body>
"""
    return response_template % body


# pin objects for transistor collector and base
pin_D1_base = machine.Pin(05, machine.Pin.OUT)
# pin_SD2 = machine.Pin(09, machine.Pin.OUT)


def power_on():
    """
    activates transistor switch with 1 second delay for startup.
    serves up success page and then redirects back to button view.
    """
    pin_D1_base.value(1)
    sleep(1)
    pin_D1_base.value(0)

    body = """
    <head>
    <title>-- Powered On --</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #008000; padding: 2vh;}p{font-size: 1.5rem;}
    </style>
    </head>
    <body>
    <h1>--- PC Powered On! ---</h1>
    <meta http-equiv="refresh" content="1; URL=/button" />
    </body>
    """
    return response_template % body


def power_off():
    """
    activates transistor switch with 5 second delay to force shutdown pc,
    serves up success page and then redirects back to button view.
    """
    pin_D1_base.value(1)
    sleep(5)
    pin_D1_base.value(0)

    body = """
    <head>
    <title>-- Powered Off --</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #008000; padding: 2vh;}p{font-size: 1.5rem;}
    </style>
    </head>
    <body>
    <h1>--- PC Powered Off! ---</h1>
    <meta http-equiv="refresh" content="1; URL=/button" />
    </body>
    """
    return response_template % body


# handler dictionary
handlers = {
    'button': button,
    'power=on': power_on,
    'power=off': power_off,
}


def main():
    """ micropython web server """

    #  server socket and listen for connections
    s = socket.socket()

    # bind to all interfaces
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080")

    while True:
        sleep(1)
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)

        # parse request for downstream condition on pwr_on and pwr_off
        request = str(req).split('/')[-1]
        print("switch call criteria: " + request)

        try:
            path = req.decode().split("\r\n")[0].split(" ")[1]
            handler = handlers[path.strip('/').split('/')[0]]
            response = handler()
            pwr_on = request.find('/power=on')
            pwr_off = request.find('/power=off')

            if pwr_on >= 0:
                power_on()
                response = handler()

            elif pwr_off >= 0:
                power_off()
                response = handler()

        except KeyError:
            response = response_404
        except Exception as e:
            response = response_500
            print(str(e))

        client_s.send(b"\r\n".join([line.encode() for line in response.split("\n")]))

        client_s.close()
        print()


# module called automatically by micropython after boot.py
main()
