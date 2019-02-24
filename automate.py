import glib

from pyudev import Context, Monitor
from usb_path import Usb
import time # For pausing

try:
    from pyudev.glib import MonitorObserver

    def device_event(observer, device):
        print 'event {0} on device {1}'.format(device.action, device)
         if device.action == 'add':
                # some function to run on insertion of usb
                print "added"
            else:
                # some function to run on removal of usb
                print "removed"
        #time.sleep(2)
        #print usb.get_mount_points()
except:
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver

    def device_event(observer, action, device):
        print 'event {0} on device {1}'.format(action, device)


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
