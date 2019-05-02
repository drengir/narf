#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import nfc

VERBOSE = True
MAX_DEVICE_COUNT = 4
# indicates the polling period in units of 150 ms (0x01 – 0x0F: 150ms – 2.25s)
POLLING_PERIOD = 1
# specifies the number of polling (0x01 – 0xFE: 1 up to 254 polling, 0xFF: Endless polling)
POLLING_NR = 30

class Nfc():

    def __init__(self):
        self.context = None
        self.device = None
        try:
            self.polling_nr = int(os.environ['POLLING_NR'])
        except:
            self.polling_nr = POLLING_NR
        try:
            self.polling_period = int(os.environ['POLLING_PERIOD'])
        except:
            self.polling_period = POLLING_NR
        print('Using polling_period {} and polling_nr {}'.format(self.polling_period, self.polling_nr))

    def open_device(self):
        self.context = nfc.init()
        print("{} uses libnfc {}".format(sys.argv[0], nfc.__version__))

        connstrings = nfc.list_devices(self.context, MAX_DEVICE_COUNT)
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
        if self.context:
            nfc.exit(self.context)

    def get_id(self):
        try:
            self.open_device()
            modulation = nfc.modulation()
            modulation.nmt = nfc.NMT_ISO14443A
            modulation.nbr = nfc.NBR_106
            # List ISO14443A targets
            target = nfc.target()
            target_count = nfc.initiator_poll_target(self.device, modulation, 1, self.polling_nr, self.polling_period, target)
            if (target_count >= 0):
                if (VERBOSE):
                    print(target_count, 'ISO14443A passive target(s) found')
                nfc.print_nfc_target(target, VERBOSE)
                uid_len = target.nti.nai.szUidLen
                uid = target.nti.nai.abtUid[:uid_len]
                print("UID byte: {}".format(uid))
                uid = str(int.from_bytes(uid, byteorder='little'))
                print("UID int: {}".format(uid))
                return uid
        except:
            # ignore exceptions
            return None
        finally:
            self.shutdown()
