# Mobile Device Testing (Simulator/Emulator)

Claude can run and control a mobile app in a simulator/emulator for
QA-style testing — boot it, tap/swipe/type through flows, screenshot to
verify, and read logs — the mobile equivalent of how `claude-in-chrome`
drives a browser. iOS uses `idb` (macOS only); Android uses `adb` (any OS,
including the team's Windows machines).

Load the `mobile-simulator-setup` skill when:
- A machine doesn't yet have Xcode + idb (iOS) or Android Studio SDK + adb
  (Android) installed/verified for simulator/emulator control.
- `idb` or `adb` commands are failing because the toolchain isn't set up,
  or a teammate's APK/`.app` build needs to get onto a device for the
  first time on this machine.

Load the `mobile-simulator-interact` skill when:
- A teammate wants Claude to actually interact with a mobile app under
  test — tap something, fill a form, navigate a flow, verify a screen —
  or read its logs (crashes, exceptions, HTTP errors).
- Triggers: "test this on the simulator/emulator", "tap the button", "fill
  in this field", "check the app logs", "does this screen look right".

## Skip when

- Toolchain already verified working this session and no device
  interaction is needed yet.
- Pure code reading/writing with no device involved.
