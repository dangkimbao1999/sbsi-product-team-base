---
description: Install and verify the iOS Simulator toolchain (Xcode, idb) for mobile testing. macOS only.
---

Set up this Mac for iOS Simulator testing, per the iOS section of the
`mobile-simulator-setup` skill:

1. If this machine is not macOS, say so and stop — this path has no
   Windows/Linux equivalent.
2. Check whether Xcode command line tools, an iOS Simulator runtime, and
   `idb` (`idb-companion` + `fb-idb`) are already installed. Only
   install/configure what's missing.
3. Boot a simulator if none is currently running.
4. Confirm success with `idb list-targets` showing it.

Report what was already in place vs. what you installed/fixed, and the
final `idb list-targets` output.
