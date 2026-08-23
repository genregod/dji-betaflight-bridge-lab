# Bridge Architecture

## Goal

Interlock DJI controller data with Betaflight-side data in a way that is testable and reversible.

## Proposed flow

```text
DJI controller transport
        |
        v
controller sampler ---> normalized control frame ---> bridge/mapping layer
                                                         |
                                                         v
                                      Betaflight input target / simulator / proxy MCU
                                                         |
                                                         v
                                         Betaflight MSP status / config sampler
```

## Layers

### 1. Controller sampler
Responsible for:
- connecting to the DJI controller transport
- decoding stick / switch values
- timestamping samples
- detecting disconnects and bad frames

### 2. Normalization layer
Responsible for:
- converting raw bytes into axes / buttons / switches
- scaling values to a common range
- applying deadbands and calibration

### 3. Betaflight probe
Responsible for:
- talking MSP to the flight controller
- reading status / arming state / modes / battery / attitude
- optionally writing safe configuration values in a lab setting

### 4. Bridge output
Possible outputs:
- virtual joystick for simulator testing
- SBUS / CRSF-style emulation through a microcontroller proxy
- a logging-only mode for protocol validation

## Implementation rule

Start with **logging only** before any write path.

That means:
- no arming
- no motor output
- no configuration writes
- no live flight test until the data path is stable
