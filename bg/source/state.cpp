#include "state.h"

#include <3ds.h>

#include "common/frame/frame.pb.h"
#include "common/frame/pb_encode.h"

namespace gamepad {
State::State() : frame(GamepadFrame_init_zero) {
    hidInit();  // Initialize HID (and IRRST by proxy)
}

State::~State() {
    hidExit();  // Deinitialize HID and IRRST
}

void State::scan() {
    hidScanInput();

    u32 held = hidKeysHeld();

    frame.du     = held & KEY_DUP;
    frame.dd     = held & KEY_DDOWN;
    frame.dl     = held & KEY_DLEFT;
    frame.dr     = held & KEY_DRIGHT;
    frame.a      = held & KEY_A;
    frame.b      = held & KEY_B;
    frame.x      = held & KEY_X;
    frame.y      = held & KEY_Y;
    frame.start  = held & KEY_START;
    frame.select = held & KEY_SELECT;
    frame.l      = held & KEY_L;
    frame.r      = held & KEY_R;
    frame.zl     = held & KEY_ZL;
    frame.zr     = held & KEY_ZR;

    circlePosition cpos;
    hidCircleRead(&cpos);
    frame.lx = cpos.dx;
    frame.ly = cpos.dy;

    circlePosition cspos;
    irrstCstickRead(&cspos);
    frame.rx = cspos.dx;
    frame.ry = cspos.dy;

    frame.seqno++;
}

void State::print(Console& c) const {
    c.printf("LX: %4d LY: %4d\n", frame.lx, frame.ly);
    c.printf("RX: %4d RY: %4d\n", frame.rx, frame.ry);

    c.printf("A: %d B: %d X: %d Y: %d\n", frame.a, frame.b, frame.x, frame.y);
    c.printf("U: %d D: %d L: %d R: %d\n", frame.du, frame.dd, frame.dl,
             frame.dr);
    c.printf("L: %d ZL: %d ZR: %d R: %d\n", frame.l, frame.zl, frame.zr,
             frame.r);
    c.printf("START: %d SELECT: %d\n", frame.start, frame.select);
}

std::vector<uint8_t> State::serialize() const {
    std::vector<uint8_t> out(GamepadFrame_size);
    auto stream = pb_ostream_from_buffer(out.data(), out.size());
    auto status = pb_encode(&stream, GamepadFrame_fields, &frame);

    out.resize(status ? stream.bytes_written : 0);
    return out;
}
}  // namespace gamepad
