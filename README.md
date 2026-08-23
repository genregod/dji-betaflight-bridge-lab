# DJI Betaflight Bridge Lab

Research scaffold for examining whether DJI controller telemetry can be bridged into a Betaflight flight-controller workflow.

## Status

- No credible public evidence yet shows a GL300A / GL300C controller being flashed into a genuinely Betaflight-compatible transmitter firmware.
- This repo now starts with a lawful reverse-engineering and bridge-development scaffold instead of claiming a finished firmware port.
- The first implementation target is a small, testable loop: controller sample -> normalized bridge model -> Betaflight MSP output.

## Repo layout

- `docs/firmware-analysis-plan.md` — staged reverse-engineering and validation plan
- `src/dji_betaflight_bridge/` — Python package for samples, MSP framing, bridge logic, and CLI helpers
- `src/bridge_stub.py` — legacy scaffold stub kept for reference
- `tests/test_msp.py` — minimal protocol verification

## Development path

1. Capture or import controller telemetry in a normalized sample format.
2. Query Betaflight state via public MSP interfaces.
3. Translate controller samples into MSP `SET_RAW_RC` frames.
4. Add logging, safety gates, and replayable tests before any live actuation path.

## Scope note

If firmware images are available and the user has rights to inspect them, document hashes, provenance, and extraction steps in `docs/firmware-analysis-plan.md`. This repo does not assume any vendor boot-chain bypass or secret extraction path.
