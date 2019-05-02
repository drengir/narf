#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Lists the first target present of each found device"""

from __future__ import print_function
import nfc
import sys
import ctypes

verbose = True
mask = 0xff
max_device_count = 16
max_target_count = 16

class Nfc():

    def get_id(self):
        uid = None
        context = nfc.init()

        # Display libnfc version
        print("%s uses libnfc %s" %( sys.argv[0], nfc.__version__))

        # TODO
        connstrings = nfc.list_devices(context, max_device_count)
        szDeviceFound = len(connstrings)

        if szDeviceFound == 0:
            print("No NFC device found.")
        
        for i in range(szDeviceFound):
            device = nfc.open(context, connstrings[i])
            if device is None:
                continue

            if(nfc.initiator_init(device)<0):
                nfc.perror(device, "nfc_initiator_init")
                nfc.close(device)
                nfc.exit(context)
                exit()

            print("NFC reader:", nfc.device_get_name(device), "opened")

            modulation = nfc.modulation()
            if mask & 0x1:
                modulation.nmt = nfc.NMT_ISO14443A
                modulation.nbr = nfc.NBR_106
                # List ISO14443A targets
                target = nfc.target()
                target_count = nfc.initiator_poll_target(device, modulation, 1, 30, 2, target)
                if (target_count >= 0):
                    if (verbose):
                        print(target_count, 'ISO14443A passive target(s) found')
                    nfc.print_nfc_target(target, verbose)
                    uid = target.nti.nai.abtUid
                    print("UID byte: {}".format(uid))
                    uid = int.from_bytes(uid, byteorder='little')
                    print("UID int: {}".format(uid))

                    #for n in range(target_count):
                        #print('Waiting for card removing...')
                        #target = nfc.target()
                        #res = nfc.initiator_target_is_present(device, target)
                        #nfc_perror(device, "nfc_initiator_target_is_present")
                        #printf("done.\n")

            nfc.close(device)
        nfc.exit(context)
        return uid
