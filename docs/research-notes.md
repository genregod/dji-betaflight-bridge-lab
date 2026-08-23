# Research Notes

## Scope and boundary

These notes track public-source reverse-engineering findings for the DJI controller side and Betaflight side.
They intentionally avoid any guidance for bypassing signed firmware, anti-tamper, or other protection mechanisms.

## DJI controller side

### Public board and firmware references
- `o-gs/dji-firmware-tools` wiki page: [GL300 Main board](https://github.com/o-gs/dji-firmware-tools/wiki/GL300-Main-board)
- DJI official download page for Phantom 4 Advanced / controller firmware:
  - [Phantom 4 Advanced Download Center](https://www.dji.com/downloads/products/phantom-4-adv)

### What the public board notes say
- The GL300 transmitter board reads sticks/switches, does ADC conversion, transmits control data, and also handles Lightbridge video/telemetry and USB-based reconfiguration.
- The page distinguishes multiple GL300 variants, including GL300A, GL300B, GL300C, and GL300E.
- The board-level notes point to specific board revisions such as P01024.07, P01298.01, P01298.05, and P01298.08.
- The wiki notes that P01298.05 introduced a GL300C-era board revision and replaced several larger parts with LQFP packages.

### Public firmware-modification context
- `dji-firmware-tools` explicitly says the tools can extract, inspect, and in some cases re-pack DJI firmware packages.
- The project also notes that firmware changes may require additional knowledge and, in some cases, firmware packages are signed and private keys are not available.
- That means the public materials are useful for analysis and board mapping, but do not themselves prove a safe or authorized path to custom-flashing a GL300 controller into Betaflight-compatible firmware.

### Relevant community clues
- A public DJI firmware-tools issue discusses FCC/CE power zone behavior on GL300A/B/C controller firmware and notes that different firmware modules changed between versions.
- This is useful as a reverse-engineering clue, but it is not evidence of a clean controller-to-Betaflight port.
- A public non-English search trail also points to DJI simulator / virtual-joystick bridge ideas, which are more realistic for interoperability than controller-firmware replacement.

## Betaflight side

### Public protocol surfaces
- Betaflight MSP protocol docs: [MSP Protocol Reference for Developers](https://betaflight.com/docs/development/MSP-Protocol-Reference-Dev)
- Betaflight source protocol header: `src/main/msp/msp_protocol.h`
- Betaflight RC input handler: `src/main/rx/msp.c`
- Betaflight MSP override helper: `src/main/rx/msp_override.c`

### What the source shows
- `MSP_SET_RAW_RC` is the key public input path for raw RC channel values.
- Betaflight’s RX-MSP path stores up to the supported channel count and zero-fills missing tail channels.
- The override path only uses fresh data when the frame is recent enough and the requested channel was present in the latest frame.
- The freshness window is 300 ms in the current source tree.
- The override logic is gated by `BOXMSPOVERRIDE`, `msp_override_channels_mask`, and `msp_override_failsafe`.

### Compatibility implication
- From a bridge perspective, Betaflight already exposes a viable public path for external RC data.
- That makes an external translator or bridge much more practical than trying to replace the DJI controller firmware itself.

## Bridge projects and non-English leads

### Bridge / simulator references
- `Matsemann/mDjiController` maps DJI controller data into a Windows virtual joystick.
- `Limitex/DJI-RC201-Simulator-for-vJoy` shows another public vJoy-style simulator bridge pattern.
- Chinese community tooling also describes reading DJI controller data and forwarding it to a virtual joystick for simulator use.

### Takeaway
- The strongest public path so far is a **data bridge**:
  1. observe controller telemetry,
  2. normalize it,
  3. emit Betaflight-safe MSP RC frames or a simulator-vJoy equivalent.
- That is a much more grounded target than claiming a confirmed flashable DJI controller firmware port.

## Current working hypothesis

If the goal is to make the controller "compatible" with Betaflight, the most plausible route is:
- a host-side translator,
- a small embedded bridge,
- or a virtual-joystick/simulator path that can later feed MSP or another RC interface.

A direct custom-firmware rewrite of the controller remains unproven in the public material reviewed so far.

## Open questions

- Which controller transport is best exposed on the exact hardware in hand?
- Can we capture a stable sample format from the controller without modifying its firmware?
- Which channel mapping and failsafe behavior should the bridge enforce by default?
- Is the bridge intended for simulator-only use, or for a live Betaflight RX path?
