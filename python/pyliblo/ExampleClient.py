#!/usr/bin/env python3

import liblo, sys

# send all messages to port 1234 on the local machine
try:
    target = liblo.Address("10.0.1.14",7770)
    print(target.get_url())
except liblo.AddressError(msg) as foo:
    print(foo)
    sys.exit()

pitch = 4.0
deck = 0

# send message "/foo/message1" with int, float and string arguments
liblo.send(target, "/xwax/pitch", 0, 4.4)

liblo.send(target, "/xwax/position", 0, 121)

print("All done.")
# wrap a message in a bundle, to be dispatched after 2 seconds
#bundle = liblo.Bundle(liblo.time() + 2.0, liblo.Message("/blubb", 123))
#liblo.send(target, bundle)
