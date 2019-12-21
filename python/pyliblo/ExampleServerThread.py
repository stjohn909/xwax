#!/usr/bin/env python3

from liblo import *
import sys
from itertools import cycle


try:
    target = Address("10.0.1.14",8887)
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
    def xwax_track_load_callback(self, path, args):
        for arg in args:
            print(arg)
        
        deck = args[0] - 1
        tp = server.allTheTracks[server.curTrackNum][1]
        ta = server.allTheTracks[server.curTrackNum][2]
        tt = server.allTheTracks[server.curTrackNum][3]
        tb = server.allTheTracks[server.curTrackNum][4]
        args = [deck, tp, ta, tt, tb]
        send(target, "/xwax/load_track", deck, tp, ta, tt, tb)
    
    @make_method('/client/get_record', 'isssd')
    def xwax_get_record_callback(self, path, args):
        num = args[0]
        pathname = args[1]
        artist = args[2]
        title = args[3]
        bpm = args[4]
        entry  = [num, pathname, artist, title, bpm]
        
        server.allTheTracks.append(entry)
        print("Record: ", entry)

    @make_method('/iphone/library', 'i')
    def xwax_track_up_callback(self, path, args):
        print("Calling library...")
        i = 1
        server.allTheTracks.clear()
        send(target, "/xwax/all_records", i)
        print("Sent call to library...")

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

        s = server.allTheTracks[server.curTrackNum][3]
        print(server.curTrackNum)
        send(controlTarget, '/iphone/trackname', s)

    @make_method('/ue4_client/ue4_testmessage', 's')
    def ue4_testmessage(self,path,args):
        print("received from UE4: '%s' " % args[0] )

        ue4Target = Address("10.0.1.6", 9999)
        send(ue4Target, '/us4_client/testreply')


    @make_method(None, None)
    def fallback(self, path, args):
        print("received unknown message '%s'" % path)


        

try:
    server = MyServer()
except ServerError(msg) as bar:
    print(bar)

server.start()
input("Press any key....")
