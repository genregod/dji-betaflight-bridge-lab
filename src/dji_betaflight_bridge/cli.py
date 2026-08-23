from __future__ import annotations

import argparse
import json
from typing import Sequence

from .bridge import Bridge, BridgeMode
from .models import ControllerSample


def _sample_from_args(args: argparse.Namespace) -> ControllerSample:
    return ControllerSample(
        source="cli",
        roll=args.roll,
        pitch=args.pitch,
        yaw=args.yaw,
        throttle=args.throttle,
        aux=tuple(args.aux or ()),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dji-bf-bridge", description="Bridge scaffold for controller samples and Betaflight MSP frames")
    parser.add_argument("--mode", choices=[mode.value for mode in BridgeMode], default=BridgeMode.OBSERVE.value)
    parser.add_argument("--channel-order", nargs=4, default=("throttle", "roll", "pitch", "yaw"), help="Order used when emitting MSP raw RC channels")

    subparsers = parser.add_subparsers(dest="command", required=True)

    encode = subparsers.add_parser("encode-rc", help="Encode a normalized controller sample into an MSP_SET_RAW_RC frame")
    encode.add_argument("--throttle", type=float, required=True)
    encode.add_argument("--roll", type=float, required=True)
    encode.add_argument("--pitch", type=float, required=True)
    encode.add_argument("--yaw", type=float, required=True)
    encode.add_argument("--aux", nargs="*", type=float, default=())

    describe = subparsers.add_parser("describe", help="Print a normalized bridge decision for the supplied sample")
    describe.add_argument("--throttle", type=float, required=True)
    describe.add_argument("--roll", type=float, required=True)
    describe.add_argument("--pitch", type=float, required=True)
    describe.add_argument("--yaw", type=float, required=True)
    describe.add_argument("--aux", nargs="*", type=float, default=())

    args = parser.parse_args(list(argv) if argv is not None else None)
    bridge = Bridge(mode=args.mode, channel_order=args.channel_order)
    sample = _sample_from_args(args)

    if args.command == "encode-rc":
        print(bridge.build_rc_frame(sample).hex())
        return 0

    decision = bridge.decide(sample)
    print(json.dumps(decision.to_dict(), indent=2, sort_keys=True))
    return 0
