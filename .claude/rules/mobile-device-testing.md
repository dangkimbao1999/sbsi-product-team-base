# Mobile Device Testing (Simulator/Emulator)

Claude can run and control a mobile app in a simulator/emulator for
QA-style testing — boot it, tap/swipe/type through flows, screenshot to
verify, and read logs — the mobile equivalent of how `claude-in-chrome`
drives a browser. iOS uses `idb`/`mobile-mcp` (macOS only); Android uses
`adb`/`mobile-mcp` (any OS, including the team's Windows machines).

## Boot — get a device ready first

Load the `mobile-boot` skill **before** `mobile-automation` /
`mobile-simulator-interact`, unless a simulator/emulator is already
confirmed booted and visible this session. It verifies the toolchain,
boots or reuses a running iOS Simulator / Android Emulator, and confirms
the interaction layer (`mobile-mcp` or `idb`/`adb`) can see it — so no
mobile task starts against a cold environment. It hands off to
`mobile-simulator-setup` on its own if the toolchain isn't installed at
all, so don't skip straight to that skill unless you already know
that's the problem.

## Interaction: mobile-mcp (preferred) — MCP server

`.mcp.json` -> `"mobile-mcp"` runs
[mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp) via
`bunx @mobilenext/mobile-mcp@latest` — one MCP server driving both iOS
Simulator and Android Emulator from the native **accessibility tree**
instead of screenshots + guessed pixel coordinates, which is faster and
more reliable than the raw `idb`/`adb` loop. Added 2026-09-16 because the
raw-command interaction flow was slow and error-prone (screenshot +
vision-guessed taps, manual scale-factor math on iOS).

**Enable it** (per-developer, not inherited from the repo): add
`"mobile-mcp"` to `enabledMcpjsonServers` in your own gitignored
`.claude/settings.local.json`, same pattern as `stitch`/`TalkToFigma`.
Then `ToolSearch("select:mobile_list_available_devices")` (or similar)
should return its tools once connected.

Load the `mobile-automation` skill when:
- A teammate wants Claude to actually interact with a mobile app under
  test — tap something, fill a form, navigate a flow, verify a screen —
  or read its logs (crashes, exceptions, HTTP errors) — and `mobile-mcp`
  is enabled.
- Triggers: "test this on the simulator/emulator", "tap the button", "fill
  in this field", "check the app logs", "does this screen look right".

## Interaction: raw idb/adb (fallback)

Load the `mobile-simulator-interact` skill instead when `mobile-mcp` isn't
enabled in this session, or for an edge case it doesn't cover — same
trigger phrases as above.

## Setup

Load the `mobile-simulator-setup` skill when:
- A machine doesn't yet have Xcode + idb (iOS) or Android Studio SDK + adb
  (Android) installed/verified for simulator/emulator control.
- `idb`/`adb`/`mobile-mcp` commands are failing because the toolchain
  isn't set up, or a teammate's APK/`.app` build needs to get onto a
  device for the first time on this machine. `mobile-mcp` drives an
  already-booted simulator/emulator — it doesn't install the platform
  SDKs for you.

## Skip when

- Toolchain already verified working this session and no device
  interaction is needed yet.
- Pure code reading/writing with no device involved.
