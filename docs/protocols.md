# Protocol Notes

## DJI controller side

The most useful controller-side evidence so far points to two families of approaches:

### 1. Virtual COM / USB controller readers
- Some DJI remote-controller bridge tools read sticks over a DJI USB/COM path and expose them to Windows as a joystick.
- Example bridge project: `Matsemann/mDjiController`.

### 2. Wi-Fi / telemetry-style stick feeds
- The Phantom 3 Standard controller community documented a TCP feed at `192.168.1.1:2345` for stick positions, then mapped it into a virtual joystick.
- That is a simulator bridge pattern, not a Betaflight firmware port.

### 3. GL300 hardware / reverse-engineering notes
- `o-gs/dji-firmware-tools` documents the GL300 main board, including stick/switch reading, control transmission, and USB interface behavior.
- Issue and wiki work there are useful for board mapping, downgrade behavior, and firmware-analysis hints.

## Betaflight side

Betaflight exposes several useful surfaces for a bridge:

### MSP
- Betaflight documents MSP extensions and a developer reference for command IDs and wire behavior.
- MSP is the cleanest way to read FC status and validate that the bridge is behaving correctly.

### CLI
- Betaflight CLI can expose status, serial-port config, and arming flags.
- The CLI is useful for bench verification and setup, but not for a live high-rate control path.

### Arming / safety
- Betaflight arming flags matter for testing.
- The bridge should begin as a **log-only** pipeline to avoid unsafe behavior.

## Bridge implication

A realistic prototype should:
1. acquire DJI-controller input
2. normalize it
3. read Betaflight state via MSP
4. compare both streams in logs
5. only then consider a write path or output emulator
