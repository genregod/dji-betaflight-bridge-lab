from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class ControllerSample:
    source: str
    roll: float
    pitch: float
    yaw: float
    throttle: float
    aux: tuple[float, ...] = ()
    ts_ms: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BetaflightSnapshot:
    source: str
    armed: bool
    mode_flags: tuple[str, ...] = ()
    battery_v: Optional[float] = None
    roll_deg: Optional[float] = None
    pitch_deg: Optional[float] = None
    yaw_deg: Optional[float] = None
    ts_ms: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BridgeDecision:
    mode: str
    action: str
    reason: str
    controller: ControllerSample
    betaflight: Optional[BetaflightSnapshot] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
