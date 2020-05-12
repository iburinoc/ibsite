#include "device.h"

#include <libevdev/libevdev-uinput.h>
#include <libevdev/libevdev.h>

#include <iostream>
#include <stdexcept>

#include "external/common/frame/frame.pb.h"

namespace gamepad {

Device::Device() {
    dev = libevdev_new();
    if (!dev)
        throw new std::runtime_error("Failed to create libevdev device");

    libevdev_set_name(dev, "3dsgamepad");

    {
        struct input_absinfo jsinfo = {};
        jsinfo.minimum              = -150;
        jsinfo.maximum              = 150;
        jsinfo.fuzz                 = 4;
        jsinfo.flat                 = 20;
        libevdev_enable_event_code(dev, EV_ABS, ABS_X, &jsinfo);
        libevdev_enable_event_code(dev, EV_ABS, ABS_Y, &jsinfo);
    }
    {
        struct input_absinfo jsinfo = {};
        jsinfo.minimum              = -150;
        jsinfo.maximum              = 150;
        jsinfo.fuzz                 = 4;
        jsinfo.flat                 = 2;
        libevdev_enable_event_code(dev, EV_ABS, ABS_RX, &jsinfo);
        libevdev_enable_event_code(dev, EV_ABS, ABS_RY, &jsinfo);
    }
    {
        struct input_absinfo jsinfo = {};
        jsinfo.minimum              = -1;
        jsinfo.maximum              = 1;
        libevdev_enable_event_code(dev, EV_ABS, ABS_HAT0X, &jsinfo);
        libevdev_enable_event_code(dev, EV_ABS, ABS_HAT0Y, &jsinfo);
    }

    libevdev_enable_event_code(dev, EV_KEY, BTN_SOUTH, nullptr);
    libevdev_enable_event_code(dev, EV_KEY, BTN_EAST, nullptr);
    libevdev_enable_event_code(dev, EV_KEY, BTN_NORTH, nullptr);
    libevdev_enable_event_code(dev, EV_KEY, BTN_WEST, nullptr);

    libevdev_enable_event_code(dev, EV_KEY, BTN_TL, nullptr);
    libevdev_enable_event_code(dev, EV_KEY, BTN_TR, nullptr);
    libevdev_enable_event_code(dev, EV_KEY, BTN_TL2, nullptr);
    libevdev_enable_event_code(dev, EV_KEY, BTN_TR2, nullptr);

    libevdev_enable_event_code(dev, EV_KEY, BTN_SELECT, nullptr);
    libevdev_enable_event_code(dev, EV_KEY, BTN_START, nullptr);

    if (libevdev_uinput_create_from_device(dev, LIBEVDEV_UINPUT_OPEN_MANAGED,
                                           &uinput_dev)) {
        std::cout << errno << std::endl;
        throw std::runtime_error("Failed to create uinput device");
    }
}

Device::~Device() {
    if (uinput_dev)
        libevdev_uinput_destroy(uinput_dev);
    if (dev)
        libevdev_free(dev);
}

void Device::send_events(GamepadFrame& frame) {
    libevdev_uinput_write_event(uinput_dev, EV_ABS, ABS_X, frame.lx);
    libevdev_uinput_write_event(uinput_dev, EV_ABS, ABS_Y, frame.ly);
    libevdev_uinput_write_event(uinput_dev, EV_ABS, ABS_RX, frame.rx);
    libevdev_uinput_write_event(uinput_dev, EV_ABS, ABS_RY, frame.ry);

    int hat0x = frame.dr - frame.dl;
    int hat0y = frame.du - frame.dd;
    libevdev_uinput_write_event(uinput_dev, EV_ABS, ABS_HAT0X, hat0x);
    libevdev_uinput_write_event(uinput_dev, EV_ABS, ABS_HAT0Y, hat0y);

    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_SOUTH, frame.b);
    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_EAST, frame.a);
    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_NORTH, frame.x);
    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_WEST, frame.y);

    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_TL, frame.l);
    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_TR, frame.r);
    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_TL2, frame.zl);
    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_TR2, frame.zr);

    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_SELECT, frame.select);
    libevdev_uinput_write_event(uinput_dev, EV_KEY, BTN_START, frame.start);

    libevdev_uinput_write_event(uinput_dev, EV_SYN, SYN_REPORT, 0);
}

}  // namespace gamepad
