# Feasibility Notes

## Direct firmware flashing on GL300A / GL300C

No public, credible example has been found that shows a **GL300A** or **GL300C** being flashed with custom firmware and then used as a generic Betaflight transmitter.

What *has* been found:

- DJI firmware downgrade / region-power discussions
- controller board teardowns and module analysis
- simulator joystick bridges
- GL300E custom-ROM / Android-root threads

## Likely realistic bridge path

The likely workable architecture is **not** to flash the DJI controller into an FPV radio.
Instead:

- read controller stick data from the DJI controller transport
- normalize it into a common control schema
- map it into a bridge output understood by the target system
- optionally read Betaflight status back over MSP

## Feasible integration points

### Controller side
- USB / COM / HID / Wi-Fi depending on controller family and model
- existing simulator bridges show that some DJI controllers can be read as input devices

### Betaflight side
- MSP over serial for status/configuration
- receiver-style input at the FC boundary
- CLI / blackbox for validation

## What would make this easier

- a known packet format for the controller
- a confirmed transport that is stable on the target model
- a receiver-emulation target that Betaflight accepts cleanly
- a test bench that can compare live control values with Betaflight state

## Risk / uncertainty

- GL300A / GL300C may expose controller data differently from newer DJI RC products
- controller firmware is closed and model-specific
- a direct custom firmware path remains unproven
