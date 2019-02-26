import glib
import os
import glob

from pyudev import Context, Monitor
from usb_path import Usb

try:
    from pyudev.glib import MonitorObserver
  
    def device_event(observer, device):
        if device.action == 'add':
            # some function to run on insertion of usb
            if(device.device_type=='usb_interface'):
                #print usb.get_mount_points()
                path=usb.get_mount_points()
                print path
                if not path[0][1]:
                    print('empty')
                else:
                    print find_that_file_latest(path[0][1])

except:
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver
   
    def device_event(observer, action, device):
        print 'event {0} on device {1}'.format(action, device)

def find_that_file(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                return os.path.join(root, file)

def find_that_file_latest(path):
    list_of_files = glob.glob(path+"*.csv") # * means all if need specific format then *.csv
    print list_of_files
    latest_file = max(list_of_files, key=os.path.getctime)
    print latest_file

def get_usb_devices():
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    observer = MonitorObserver(monitor)
    observer.connect('device-event', device_event)
    monitor.start()
    glib.MainLoop().run()

if __name__ == '__main__':
    usb = Usb()
    get_usb_devices()
