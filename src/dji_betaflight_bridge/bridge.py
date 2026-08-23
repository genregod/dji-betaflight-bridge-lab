from __future__ import annotations

from enum import Enum
from typing import Sequence

from .models import BetaflightSnapshot, BridgeDecision, ControllerSample
from .msp import build_set_raw_rc


class BridgeMode(str, Enum):
    OBSERVE = "observe"
    ACTUATE = "actuate"


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def normalize_axis(value: float, *, minimum: int = 1000, maximum: int = 2000) -> int:
    value = _clamp(value, -1.0, 1.0)
    midpoint = (minimum + maximum) / 2
    span = (maximum - minimum) / 2
    return int(round(midpoint + (value * span)))


def normalize_throttle(value: float, *, minimum: int = 1000, maximum: int = 2000) -> int:
    value = _clamp(value, 0.0, 1.0)
    return int(round(minimum + (value * (maximum - minimum))))


def sample_to_raw_rc(sample: ControllerSample, *, channel_order: Sequence[str] = ("throttle", "roll", "pitch", "yaw")) -> list[int]:
    values = {
        "throttle": normalize_throttle(sample.throttle),
        "roll": normalize_axis(sample.roll),
        "pitch": normalize_axis(sample.pitch),
        "yaw": normalize_axis(sample.yaw),
    }

    channels: list[int] = []
    for name in channel_order:
        if name not in values:
            raise ValueError(f"Unsupported channel name: {name}")
        channels.append(values[name])

    aux_limit = max(0, 8 - len(channels))
    channels.extend(normalize_axis(value) for value in sample.aux[:aux_limit])
    channels.extend([1500] * (8 - len(channels)))
    return channels[:8]


class Bridge:
    def __init__(self, mode: BridgeMode | str = BridgeMode.OBSERVE, *, channel_order: Sequence[str] = ("throttle", "roll", "pitch", "yaw")) -> None:
        self.mode = BridgeMode(mode)
        self.channel_order = tuple(channel_order)

    def build_rc_frame(self, sample: ControllerSample) -> bytes:
        return build_set_raw_rc(sample_to_raw_rc(sample, channel_order=self.channel_order))

    def decide(self, sample: ControllerSample, betaflight: BetaflightSnapshot | None = None) -> BridgeDecision:
        if self.mode is BridgeMode.OBSERVE:
            action = "log-only"
            reason = "observe mode; no write path enabled"
        else:
            action = "emit-msp-set-raw-rc"
            reason = "controller sample normalized and ready for Betaflight raw RC output"

        return BridgeDecision(
            mode=self.mode.value,
            action=action,
            reason=reason,
            controller=sample,
            betaflight=betaflight,
        )
