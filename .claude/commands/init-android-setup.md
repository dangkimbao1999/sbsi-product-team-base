---
description: Install and verify the Android emulator toolchain (SDK, adb, emulator) for mobile testing.
---

Set up this machine for Android Emulator testing, per the Android section
of the `mobile-simulator-setup` skill:

1. Check whether Android Studio's SDK, `platform-tools` (`adb`), and
   `emulator` are already installed and on `PATH`. Only install/configure
   what's missing.
2. Boot an AVD if none is currently running.
3. Confirm success with `adb devices` showing a booted emulator.

Report what was already in place vs. what you installed/fixed, and the
final `adb devices` output.
