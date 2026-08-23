# Firmware Analysis Plan

This repository is a research scaffold for a bridge between DJI controller data and Betaflight.
It does **not** assume any secret vendor boot-chain bypass or a finished custom firmware port.

## Scope

- Study controller telemetry formats and transports that can be observed or lawfully extracted
- Study Betaflight's public MSP, CLI, receiver, and arming surfaces
- Build a small bridge that converts normalized controller samples into Betaflight-safe outputs
- Keep every step replayable and testable before any live actuation path

## Inputs to document

### Controller side

- Controller model and board identifiers
- Firmware image provenance, hash, and acquisition method if a lawful dump is available
- Transport type: USB HID, USB CDC, UART, SPI, Wi-Fi, or another public interface
- Frame captures or logs that show raw stick data, calibration data, or pairing metadata
- Any non-English teardown or modding notes that describe the transport or data layout

### Betaflight side

- Betaflight version and target board
- MSP API version reported by the flight controller
- Receiver channel order and any custom mappings
- Arming, failsafe, and mode-state behavior
- CLI and configuration settings relevant to input routing

## Recommended phases

### Phase 1: Observe

- Capture controller samples without sending anything to Betaflight
- Identify the field order and units used by the controller
- Normalize the values into a simple sample model

### Phase 2: Translate

- Compare sample normalization against Betaflight's `SET_RAW_RC` semantics
- Verify channel order, min/max values, and safe defaults
- Add a log-only bridge decision object that explains every transformation

### Phase 3: Validate

- Test the bridge against replay captures
- Confirm that the MSP frame encoder matches Betaflight's framing rules
- Add unit tests before any live device path

### Phase 4: Expand

- Add telemetry reads from Betaflight for closed-loop experiments
- Add persistent context logging for captures and outputs
- Document any firmware analysis findings that are derived from sources the user is authorized to inspect

## Non-goals

- Bypassing secure boot, anti-tamper, or access controls
- Redistributing proprietary firmware blobs
- Claiming a working flash path before one has been demonstrated

## Deliverables

- A normalized controller sample schema
- MSP frame encoders/decoders
- A bridge decision layer with log-only default behavior
- A clean handoff path from research notes to implementation
