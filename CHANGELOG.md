# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

## [1.0.0] - 2026-04-24

First tagged release for this maintained fork (`david-leadtech/Android-ga-tracking-debugger`).

### What you get in v1.0.0 (product, as shipped)

**Android GA Tracking Debugger** is a small **desktop** app (Python 3 + Tkinter) for **local** measurement QA while you build. It does **not** call Google’s APIs or show numbers from the cloud: it **tails `adb logcat`**, matches Firebase/GA **debug** lines, and shows them in a single window in near real time.

- **In one place:** `Logging event`, `Setting user property` (including a common `(FE):` line variant), and `Setting storage consent` material.
- **Practical for teams:** search; pick the device when more than one is connected (`adb -s`); status line for ADB / device / capture; **export the session to JSON** (events, user properties, consent history, device serial, app version); **double-click** a row for raw/detail.
- **i18n:** English and Spanish from the app menu.
- **Requirements (non‑negotiable):** [ADB / platform-tools](https://developer.android.com/tools/releases/platform-tools) in your `PATH`, a device or emulator with USB/wireless debugging, and a Python 3.7+ runtime to run `python main.py`. No extra pip packages to run the GUI (dev uses `pytest` from `requirements-dev.txt` for tests/CI only).

**What it is *not*:** a replacement for the Firebase/GA4 console, DebugView in the cloud, or BigQuery. It is the **cable+ADB+logcat** story: *what the SDK is printing on the device right now*.

The bullets below are **technical and fork** changes (tests, CI, and UI) that implement that product.

### Added (technical and fork)

- Pytest coverage for `log_parser` and GitHub Actions CI (Ubuntu, macOS, Windows; Python 3.9 and 3.12).
- `requirements-dev.txt` and README instructions for local tests.
- Device selection when multiple devices are connected (`adb -s <serial>` for logcat and related ADB calls).
- Status strip for ADB / device / capture state; `last_device_serial` persisted in config.
- Export session to JSON (events, user properties, consent history, device serial, app version).
- Double-click on tree rows for event, user property, and consent details.
- Keyboard shortcut to focus search (Ctrl+F / Cmd+F).
- `ttk` theme selection by platform (aqua / vista / clam).
- Parser support for `Setting user property (FE):` log line variant.
- Changelog, release workflow on `v*.*.*` tags, and repository docs for this fork.

### Fixed

- Top-level menu `entryconfig` indices for dynamic language labels.
