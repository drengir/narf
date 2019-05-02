#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nfc
import sys

verbose = True
max_device_count = 16

class Nfc():

    def __init__(self):
        self.context = None
        self.device = None
        try:
            self.open_device()
        except:
            self.shutdown()

    def open_device(self):
        # return if device is already initialized
        if self.device:
            return
        # make sure everything is shut down before initalizing
        self.shutdown()
        
        self.context = nfc.init()
        print("{} uses libnfc {}".format(sys.argv[0], nfc.__version__))

        connstrings = nfc.list_devices(self.context, max_device_count)
        szDeviceFound = len(connstrings)
        if szDeviceFound == 0:
            raise Exception("No NFC reader found!")
        
        for i in range(szDeviceFound):
            self.device = nfc.open(self.context, connstrings[i])
            if self.device is None:
                continue
            if(nfc.initiator_init(self.device)<0):
                nfc.perror(self.device, "nfc_initiator_init")
                raise Exception("Init of device failed!")
            print("NFC reader:", nfc.device_get_name(self.device), "opened")
            break
    
    def shutdown(self):
        if self.device:
            nfc.close(self.device)
            self.device = None
        if self.context:
            nfc.exit(self.context)
            self.context = None
        
    def get_id(self):
        try:
            self.open_device()
            uid = None
            modulation = nfc.modulation()

            modulation.nmt = nfc.NMT_ISO14443A
            modulation.nbr = nfc.NBR_106
            # List ISO14443A targets
            target = nfc.target()
            target_count = nfc.initiator_poll_target(self.device, modulation, 1, 30, 1, target)
            if (target_count >= 0):
                if (verbose):
                    print(target_count, 'ISO14443A passive target(s) found')
                nfc.print_nfc_target(target, verbose)
                uid_len = target.nti.nai.szUidLen
                uid = target.nti.nai.abtUid[:uid_len]
                print("UID byte: {}".format(uid))
                uid = str(int.from_bytes(uid, byteorder='little'))
                print("UID int: {}".format(uid))

            return uid
        except:
            self.shutdown()
