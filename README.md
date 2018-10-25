# CursedAutomation
Automating IoT devices with Python and controlling them through a Curses terminal interface

![Cursed Automation Screenshot](doc/img/2018-10-24-CursedAutomation.png?raw=true "Cursed Automation Screenshot")

CursedAutomation is a set of home automation and monitoring tools that have been assembled into a graphical terminal interface using Python and Curses. It is a work in progress, and currently all device controls are sent from the terminal running the UI. It will be upgraded in the future to contain a client/server relationship.

It is not designed for use as a standalone or particularly flexible project at this point. It uses the pyHS100 library to control the TP-Link smarthome devices and python-nmap to detect what devices are connected to the network.

Current features:
  *  Touchscreen / Mouse controlled UI for adjusting lights
  *  Runs in the terminal using Python (Currently 3.4.3)
  *  Detects devices on the network (e.g. Smartphones on WiFi)

*Interesting Notes:*
Android phones enter a power save mode shortly after having their screen turned off. This causes them to partially drop off of the WiFi network and no longer be detected. They will then regularly, and briefly, recconect to pull notifications or other information before disconnecting again. A future version of this automation software will aim to keep track of these connections so as to use them to more accurately detect if a phone is 'home' or not.

There is currently minimal error checking (other than exiting cleanly back to the command line). The terminal currently requires a size of at least 19x72 in order to run. Later versions will use scrolling or menu panels to get around this current limitation.
