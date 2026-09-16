---
name: mobile-simulator-setup
description: Install and verify the toolchain needed to boot a mobile simulator/emulator and control it programmatically — Xcode + Simulator + idb for iOS (macOS only), Android Studio SDK + platform-tools (adb) for Android (works on macOS/Linux/Windows). Use when setting up a new machine for mobile QA/testing, or when idb/adb commands fail because the toolchain isn't installed yet.
---

# Mobile Simulator/Emulator Environment Setup

One-time setup so a machine can run a mobile app in a simulator/emulator
and be driven by Claude. Two independent tracks — do whichever platform(s)
the team member needs. Android works on any OS (including Windows); iOS
requires a Mac.

## iOS — macOS only

Requires Xcode (from the App Store) and its command line tools:

```bash
xcode-select -p                    # sanity check — prints a path if installed
xcode-select --install             # if the above errored
sudo xcodebuild -license accept    # accept the Xcode license non-interactively
```

Install the iOS Simulator runtime (Xcode ships a default one; add others via
Xcode → Settings → Platforms, or):

```bash
xcodebuild -downloadPlatform iOS
```

Boot and verify a simulator:

```bash
open -a Simulator
xcrun simctl list devices          # confirm at least one device shows "Booted"
```

If nothing is booted:

```bash
DEVICE=$(xcrun simctl list devices available | grep -m1 'iPhone' | grep -oE '[A-F0-9-]{36}')
xcrun simctl boot "$DEVICE"
open -a Simulator
```

Install `idb` (Facebook's iOS Development Bridge — this is what gives
programmatic tap/swipe/type/screenshot control):

```bash
brew tap facebook/fb
brew install idb-companion
pip3 install fb-idb
```

Verify:

```bash
idb --version
idb list-targets       # should list the booted simulator's UDID, state "Booted"
```

If `idb list-targets` doesn't show the booted device, restart its daemon:
`killall idb_companion` (it auto-restarts on the next `idb` call).

### Getting the app under test onto the simulator

- Have a `.app` bundle already (e.g. a CI build artifact): `xcrun simctl
  install booted /path/to/YourApp.app`
- Only have source: build it first with whatever that project uses
  (`flutter build ios --simulator`, `xcodebuild -scheme ... -sdk
  iphonesimulator`, etc.) — this skill doesn't cover app builds, only the
  simulator + control tooling.
- Launch: `xcrun simctl launch booted <bundle-id>` (bundle id is in the
  app's `Info.plist`, or `unzip -p YourApp.app/Info.plist | plutil -p -`).

## Android — any OS (macOS / Linux / Windows)

Requires Android Studio (installs the SDK, `platform-tools`, and the
`emulator` binary by default) — or a standalone `cmdline-tools` install if
a full IDE isn't wanted.

Put `platform-tools` and `emulator` on `PATH`:

| OS | Typical SDK location |
|---|---|
| macOS | `~/Library/Android/sdk` |
| Linux | `~/Android/Sdk` |
| Windows | `%LOCALAPPDATA%\Android\Sdk` |

Verify:

```bash
adb version
emulator -version
```

Create and boot an emulator (AVD) — or use Android Studio's Device Manager
GUI, which does the same thing:

```bash
avdmanager create avd -n test-device -k "system-images;android-34;google_apis;x86_64"
emulator -avd test-device
```

Verify the device is visible to adb:

```bash
adb devices     # should list e.g. "emulator-5554   device"
```

### Getting the app under test onto the emulator

- **Only have an APK, no source** (the common case for testing a
  teammate's build or a release candidate): this works fine —
  ```bash
  adb install -r /path/to/app.apk
  ```
  To find the package name and launch activity of an APK you didn't build
  (needs Android SDK build-tools' `aapt` on PATH):
  ```bash
  aapt dump badging /path/to/app.apk | grep -E "package:|launchable-activity:"
  ```
  Then launch it:
  ```bash
  adb shell am start -n <package>/<launchable-activity>
  ```
- **Have source** (e.g. Flutter): the project's own run command
  (`flutter run`) builds, installs, and launches in one step — no separate
  `adb install` needed unless you specifically want to test a pre-built APK
  instead of a fresh build.

## Common gotchas

- **iOS has no Windows/Linux path.** `idb-companion` wraps Apple's own
  Simulator/XCTest frameworks — there is no workaround on a non-Mac
  machine. Android is the cross-platform option.
- **Multiple booted devices/emulators** make target selection ambiguous —
  always pass `--udid <UDID>` (idb) or `-s <serial>` (adb) explicitly once
  more than one could be running.
- **`adb devices` shows nothing**: the emulator is still booting (first
  boot can take a minute+) — poll `adb devices` until the state changes
  from blank to `device`, not `offline`.
- **Windows PATH**: `adb`/`emulator` not found usually means
  `platform-tools`/`tools`/`emulator` under the SDK root were never added
  to `PATH` — check `%LOCALAPPDATA%\Android\Sdk` exists and add its
  `platform-tools` and `emulator` subfolders.

## Load this skill when

- A machine doesn't yet have the iOS (Xcode + idb) or Android (SDK + adb)
  toolchain installed or verified for simulator/emulator control.
- `idb` or `adb` commands are failing and the cause looks like a missing
  install rather than a usage error.
- Getting a teammate's APK or `.app` build onto a simulator/emulator for
  the first time on a given machine.
