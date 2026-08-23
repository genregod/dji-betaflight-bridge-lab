"""DJI Betaflight bridge scaffold.

This package focuses on a testable bridge layer:
controller samples -> normalized model -> Betaflight MSP frames.
"""

from .bridge import Bridge, BridgeMode, normalize_axis, normalize_throttle, sample_to_raw_rc
from .controller import ControllerSource, decode_controller_payload
from .models import BetaflightSnapshot, BridgeDecision, ControllerSample
from .msp import MSP_API_VERSION, MSP_SET_RAW_RC, build_api_version_request, build_set_raw_rc, decode_msp_v1, encode_msp_v1

__all__ = [
    "BetaflightSnapshot",
    "Bridge",
    "BridgeDecision",
    "BridgeMode",
    "ControllerSample",
    "ControllerSource",
    "MSP_API_VERSION",
    "MSP_SET_RAW_RC",
    "build_api_version_request",
    "build_set_raw_rc",
    "decode_controller_payload",
    "decode_msp_v1",
    "encode_msp_v1",
    "normalize_axis",
    "normalize_throttle",
    "sample_to_raw_rc",
]
