from libpebble2.communication import PebbleConnection
from libpebble2.communication.transports.serial import SerialTransport

from libpebble2.services import *
from libpebble2.services.notifications import Notifications

pebble = PebbleConnection(SerialTransport("/dev/rfcomm0"))
pebble.connect()
pebble.run_async()

n = Notifications(pebble, None)
n.send_notification("Subject", "Message", "From")
