#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Lists the first target present of each found device"""

from __future__ import print_function
import nfc
import sys
import ctypes

verbose = False
mask = 0xff
max_device_count = 16
max_target_count = 16

class Nfc():

    def get_id(self):
        context = nfc.init()

        # Display libnfc version
        print("%s uses libnfc %s" %( sys.argv[0], nfc.__version__))

        # TODO
        connstrings = nfc.list_devices(context, max_device_count)
        szDeviceFound = len(connstrings)

        if szDeviceFound == 0:
            print("No NFC device found.")
        
        for i in range(szDeviceFound):
            pnd = nfc.open(context, connstrings[i])
            if pnd is None:
                continue

            if(nfc.initiator_init(pnd)<0):
                nfc.perror(pnd, "nfc_initiator_init")
                nfc.close(pnd)
                nfc.exit(context)
                exit()

            print("NFC reader:", nfc.device_get_name(pnd), "opened")

            nm = nfc.modulation()
            if mask & 0x1:
                nm.nmt = nfc.NMT_ISO14443A
                nm.nbr = nfc.NBR_106
                # List ISO14443A targets
                nt = nfc.target()
                res = nfc.initiator_poll_target(pnd, nm, 1, 30, 2, nt)
                if (res >= 0):
                    if (verbose or (res > 0)):
                        print(res, 'ISO14443A passive target(s) found')
                    for n in range(res):
                        nfc.print_nfc_target(nt, verbose)
                        print('Waiting for card removing...')
                        nt = nfc.target()
                        res = nfc.initiator_target_is_present(pnd, nt)
                        #nfc_perror(pnd, "nfc_initiator_target_is_present")
                        #printf("done.\n")

            nfc.close(pnd)
        nfc.exit(context)

        return nt.nti.nai.abtUid
