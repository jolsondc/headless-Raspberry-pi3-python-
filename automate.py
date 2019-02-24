import glib

from pyudev import Context, Monitor
from usb_path import Usb
import time # For pausing
from dbus.mainloop.glib import DBusGMainLoop

try:
    from pyudev.glib import MonitorObserver

    def device_event(observer, device):
        print 'event {0} on device {1}'.format(device.action, device)
        time.sleep(2)
        print usb.get_mount_points()
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

def waitforusb():
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    proxy = bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
    iface = dbus.Interface(proxy, "org.freedesktop.UDisks")
    devices = iface.get_dbus_method('EnumerateDevices')()
    iface.connect_to_signal('DeviceAdded', device_event)
    global mainloop
    mainloop = gobject.MainLoop()
    mainloop.run()


if __name__ == '__main__':
    usb = Usb()
    waitforusb()
