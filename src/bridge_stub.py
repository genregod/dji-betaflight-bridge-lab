"""Bridge scaffold for DJI controller samples and Betaflight probes.

This file is intentionally conservative: it documents the shape of the
integration without pretending we already have a working firmware port.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ControllerFrame:
    source: str
    roll: float
    pitch: float
    yaw: float
    throttle: float
    aux: tuple[float, ...] = ()
    ts_ms: Optional[int] = None


@dataclass
class BetaflightFrame:
    source: str
    armed: bool
    mode_flags: tuple[str, ...] = ()
    battery_v: Optional[float] = None
    roll_deg: Optional[float] = None
    pitch_deg: Optional[float] = None
    yaw_deg: Optional[float] = None
    ts_ms: Optional[int] = None


def parse_controller_payload(payload: bytes) -> ControllerFrame:
    raise NotImplementedError("controller transport not yet confirmed for this model")


def parse_msp_payload(payload: bytes) -> BetaflightFrame:
    raise NotImplementedError("MSP parser stub only; bind to a concrete Betaflight message first")


def interlock(controller: ControllerFrame, betaflight: BetaflightFrame) -> dict:
    """Return a normalized bridge decision for logging and later routing."""
    return {
        "controller": asdict(controller),
        "betaflight": asdict(betaflight),
        "decision": "log-only",
    }


if __name__ == "__main__":
    print("DJI/Betaflight bridge scaffold loaded")
