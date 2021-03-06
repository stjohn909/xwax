#!/usr/bin/env python3

from liblo import *
import sys
from itertools import cycle


try:
    target = Address("10.0.1.14",7770)
    controlTarget = Address("10.0.1.2",4321)

    print("xwax url: %s", target.get_url())
    print("controller url: %s", controlTarget.get_url())
except AddressError(msg) as foo:
    print(foo)
    sys.exit()

class MyServer(ServerThread):
    allTheTracks = []
    curTrackNum = 9
    def __init__(self):
        ServerThread.__init__(self, 1234)

    @make_method('/iphone/trackload', 'i')
    def xwax_pitch_callback(self, path, args):
        deck = 0
        tp = server.allTheTracks[server.curTrackNum][1]
        ta = server.allTheTracks[server.curTrackNum][2]
        tt = server.allTheTracks[server.curTrackNum][3]
        args = [deck, tp, ta, tt]
        send(target, "/xwax/load_track", 0, tp, ta, tt)
    
    @make_method('/client/get_record', 'isss')
    def xwax_get_record_callback(self, path, args):
        num = args[0]
        pathname = args[3]
        artist = args[2]
        title = args[1]
        entry  = [num, pathname, artist, title]
        
        server.allTheTracks.append(entry)
        print("Record: ", entry)

    @make_method('/iphone/library', 'i')
    def xwax_track_up_callback(self, path, args):
        print("Calling library...")
        i = 1
        server.allTheTracks.clear()
        send(target, "/xwax/library", i)

    @make_method('/iphone/trackname', 's')
    def iphone_update_label(self, path, args):
        s = args[0]
        mytarget = Address("10.0.1.2",4321)
        send(mytarget, "/iphone/trackname" , s)

    @make_method('/iphone/trackencoder', 'i')
    def iphone_track_up_down(self, path, args):
        i = args[0]
        server.curTrackNum += i
        if (server.curTrackNum < 0):
            server.curTrackNum = len(server.allTheTracks)-1

        if (server.curTrackNum > len(server.allTheTracks)-1):
            server.curTrackNum = 0

        s = server.allTheTracks[server.curTrackNum][2]
        print(server.curTrackNum)
        send(controlTarget, '/iphone/trackname', s)



    @make_method(None, None)
    def fallback(self, path, args):
        print("received unknown message '%s'" % path)



try:
    server = MyServer()
except ServerError(msg) as bar:
    print(bar)

server.start()
input("Press any key....")
