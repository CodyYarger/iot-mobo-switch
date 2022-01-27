"""
This module contains a MicroPython webserver for the NodeMCU microcontroller that
interfaces a PC motherboard. The 'button' view can be accessed by the user to close
a transistor switch, executing a forced shutdown or startup of a computer.

Note: This is currently written for a test circuit with the switch completing
an LED circuit. Updates will be made to power LED, as a feedback, when transistor
switch provides continuety between the motherboard power switch pins.
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


# pin objects for transistor collector and base
pin_collect = machine.Pin(09, machine.Pin.OUT)
pin_base = machine.Pin(05, machine.Pin.OUT)


def button():
    body = """
<head>
<title>IoT PC Switch</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{width: 300px; display: inline-block; background-color: #A9A9A9; border: none;
border-radius: 4px; color: red; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}.full {
 display: block; width: 100%;}
</style>
</head>

<body>
<h1>IoT Motherboard Switch</h1>

<p>Click to turn switch ON to Force-Shutdown or Startup PC</strong></p>
<p>
<a href="/switch=yes">
<button id = "sw" onclick= "color();label()" class="button">---- OFF ----</button>
</a>
</p>
<script>
function color() {
document.getElementById("sw").style.color = "green";
}

function label() {
document.getElementById("sw").innerHTML = "---- ON ----";
}
</script>

</a>
</p>
</body>
"""
    return response_template % body


def switch():
    """ activates transistor switch via NodeMCU and view for success page """
    pin_collect.value(1)
    pin_base.value(1)
    sleep(3)
    pin_base.value(0)

    body = """
<head>
<title>Success</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
</style>
</head>
<body>
<h1>--- Success! ---</h1>
</body>
"""
    return response_template % body


# handler dictionary
handlers = {
    'button': button,
    'switch=yes': switch
}


def main():
    """ micropython web server """

    # define server socket and listen for connections
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
        request = str(req)
        print("Request:")
        print(req)

        try:
            path = req.decode().split("\r\n")[0].split(" ")[1]
            handler = handlers[path.strip('/').split('/')[0]]
            response = handler()
            switch_yes = request.find('/switch=yes')
            if switch_yes >= 0:
                switch()
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
