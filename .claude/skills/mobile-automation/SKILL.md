---
name: mobile-automation
description: Control Android and iOS devices, emulators and simulators via the mobile-mcp MCP server — launch apps, tap, swipe, type, take screenshots, read the accessibility tree. Prefer this over the raw idb/adb `mobile-simulator-interact` skill: it drives apps from the accessibility tree instead of screenshots, which is faster and more reliable. Use when a task involves a mobile device or app, mobile UI testing, or reproducing a bug on a phone.
---

# Mobile Automation with mobile-mcp

Tools for driving real phones, emulators and simulators through the
`mobile-mcp` MCP server (`.mcp.json` -> `"mobile-mcp"`, runs via
`bunx @mobilenext/mobile-mcp@latest`). All tools are prefixed `mobile_`.

This is the **preferred** path over `.claude/skills/mobile-simulator-interact/SKILL.md`'s
raw `idb`/`adb` commands — it reads the native accessibility tree instead
of relying on screenshots + guessed pixel coordinates, so it's faster,
cheaper (no vision tokens), and doesn't hit the iOS point-vs-pixel scale
gotcha that skill documents. Fall back to the raw `idb`/`adb` skill only
if `mobile-mcp` isn't enabled locally, or for an edge case it doesn't
cover.

## Prerequisites (same as before)

The simulator/emulator toolchain itself is unchanged — see
`mobile-simulator-setup` (Xcode + Simulator + `idb` for iOS, macOS only;
Android Studio SDK + `adb` for Android, any OS) if it isn't installed yet.
`mobile-mcp` drives an already-booted simulator/emulator; it doesn't
install the SDKs for you.

Each developer must also add `"mobile-mcp"` to their own
`enabledMcpjsonServers` in `.claude/settings.local.json` (gitignored,
per-developer) before its tools are callable — see
`.claude/rules/mobile-device-testing.md`.

## Workflow

1. **Pick a device.** Call `mobile_list_available_devices` and use one of
   the returned devices for every subsequent call. If no device is
   available, ask the user to connect one (Android: `adb devices` must
   show it; iOS: simulator booted or device paired).
2. **See the screen.** Prefer `mobile_list_elements_on_screen` — it
   returns the accessibility tree with element labels and coordinates. It
   is faster, cheaper, and more reliable than screenshots. Fall back to
   `mobile_take_screenshot` only when elements are missing or you need
   visual confirmation (games, canvas-drawn UI, image content — same
   Flutter/canvas caveat as the raw-command skill).
3. **Act.** `mobile_click_on_screen_at_coordinates`, `mobile_swipe_on_screen`,
   `mobile_type_keys`, `mobile_press_button` (HOME, BACK, VOLUME, ENTER),
   `mobile_launch_app` / `mobile_terminate_app` / `mobile_list_apps`,
   `mobile_open_url`.
4. **Verify after every action.** Re-list elements (or re-screenshot) to
   confirm the UI changed as expected before the next step. Mobile UIs
   animate; if the expected element is not there yet, wait briefly and
   check again rather than tapping blind.

## Tips

- Click the **center** of an element's bounds, not its top-left corner.
- To type, first tap the input field, confirm it is focused, then
  `mobile_type_keys`.
- Use `mobile_save_screenshot` when the user wants the image as a file;
  `mobile_start_screen_recording` / `mobile_stop_screen_recording` for
  videos.
- App crashed? `mobile_list_crashes` and `mobile_get_crash` fetch crash
  logs; `mobile_get_device_logs` streams live logcat/unified-log output.
- Screen size from `mobile_get_screen_size`; coordinates are in that
  space.
- Real devices in the cloud (no local hardware): `mobile_login_to_cloud_provider`,
  then `mobile_list_remote_devices` / `mobile_allocate_remote_device`, and
  release with `mobile_release_remote_device` when done — this reaches
  Mobile Next's cloud service, a third party outside this repo's
  infrastructure; confirm with the user before using it.

## Load this skill when

- A teammate wants Claude to actually interact with a mobile app under
  test — tap something, fill a form, navigate a multi-step flow, verify a
  screen visually — or read its logs, and `mobile-mcp` is available.
- Triggers: "test this on the simulator/emulator", "tap the button", "fill
  in this field", "navigate to X and check", "check the app logs", "does
  this screen look right".

## Skip when

- The simulator/emulator or toolchain isn't set up yet — use
  `mobile-simulator-setup` first.
- `mobile-mcp` isn't enabled in this session (`ToolSearch` finds no
  `mobile_*` tools) and enabling it isn't an option right now — use
  `mobile-simulator-interact` instead.
- Pure source-code review with no device involved.
