# Research Notes

## English / reverse-engineering references

- **o-gs/dji-firmware-tools**
  - GL300 main-board wiki
  - RC firmware issues and downgrade / power-zone discussions
  - useful for board mapping and firmware analysis, not a confirmed Betaflight port

- **Matsemann/mDjiController**
  - turns a DJI controller into a Windows simulator joystick via COM + vJoy
  - useful as a data-capture / bridge reference

- **EEVblog: Phantom remote controller as a game controller**
  - reads controller data and maps it to a virtual HID device
  - bridge inspiration, not a firmware flash path

- **XDA: DJI Phantom 4 Pro + Custom Rom**
  - focuses on the GL300E Android controller
  - shows root / custom-ROM interest, but not Betaflight transmitter firmware

## Non-English leads

- **German DJI forums**
  - GL300A / GL300B update behavior and firmware version boundaries
  - confirms the controller family is tied to DJI's own update flow

- **Chinese DJI community and simulator posts**
  - DJI simulator support and USB controller behavior
  - mostly relevant as input/driver references

- **Russian / Chinese Betaflight tutorials**
  - useful for Betaflight flashing/configuration flow on actual flight controllers
  - not evidence of DJI RC firmware conversion

## Takeaway

The strongest lead is a **bridge project**, not a controller-flash project.
