import os
from glob import glob
from subprocess import check_output, CalledProcessError
import time # For pausing

class Usb:

    def get_usb_devices(self):
        sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
        usb_devices = (dev for dev in sdb_devices
            if 'usb' in dev.split('/')[5])
        return dict((os.path.basename(dev), dev) for dev in usb_devices)

    def get_mount_points(self,devices=None):
        time.sleep(2)
        devices = devices or self.get_usb_devices() # if devices are None: get_usb_devices
        output = check_output(['mount']).splitlines()
        is_usb = lambda path: any(dev in path for dev in devices)
        usb_info = (line for line in output if is_usb(line.split()[0]))
        #device name having whitespace- solution is below
        fullInfo = []
        for info in usb_info:
            mountURI = info.split()[0]
            usbURI = info.split()[2]
            print(info.split().__sizeof__())
            for x in range(3, info.split().__sizeof__()):
                if info.split()[x].__eq__("type"):
                    for m in range(3, x):
                        usbURI += " "+info.split()[m]
                    break
            fullInfo.append([mountURI, usbURI])
        return fullInfo
        #return [(info.split()[0], info.split()[2]) for info in usb_info]

