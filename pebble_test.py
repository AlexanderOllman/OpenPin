from libpebble2.communication import PebbleConnection
from libpebble2.communication.transports.serial import SerialTransport
pebble = PebbleConnection(SerialTransport("/dev/rfcomm0"))
pebble.connect()
pebble.run_async()

print(pebble.watch_info.serial)