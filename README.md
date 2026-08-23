# DJI Betaflight Bridge Lab

Research scaffold for examining whether DJI controller telemetry can be bridged into a Betaflight flight-controller workflow.

## What we know so far

- There is **no solid public evidence** that a **DJI GL300A / GL300C** can be flashed into a truly Betaflight-compatible transmitter firmware.
- The practical path people have actually used is to **read controller data** and map it into a simulator or virtual input layer.
- The reverse-engineering path that looks most promising is:
  1. identify the controller transport
  2. capture controller data
  3. probe Betaflight via MSP / serial / CLI
  4. translate between the two

## Repository goal

This repo is a place to collect:

- controller teardown / reverse-engineering notes
- Betaflight protocol notes
- non-English forum leads
- bridge / simulator projects that can be reused
- a realistic proof-of-concept for data interlock

## Important scope note

This repo does **not** claim to flash custom firmware onto a GL300A / GL300C controller.

That would require a verified boot-chain exploit or a documented vendor-supported path, and no such public path has been confirmed here.

## Starter docs

- `docs/feasibility.md`
- `docs/research-notes.md`
- `docs/architecture.md`
- `src/bridge_stub.py`

## Suggested next steps

1. Confirm the exact DJI controller model and transport.
2. Confirm the Betaflight data source you want to interlock with.
3. Choose a bridge target:
   - virtual joystick for simulator testing
   - SBUS / CRSF-style output for a receiver chain
   - a proxy MCU between controller and flight stack
4. Implement the bridge in a small, testable loop before any firmware work.
