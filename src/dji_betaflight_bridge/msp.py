from __future__ import annotations

from typing import Sequence

MSP_API_VERSION = 1
MSP_SET_RAW_RC = 200
MSP_STATUS = 101
MSP_ATTITUDE = 108
MSP_ANALOG = 110


class MSPError(ValueError):
    pass


def _checksum(size: int, command: int, payload: bytes) -> int:
    value = size ^ command
    for byte in payload:
        value ^= byte
    return value & 0xFF


def encode_msp_v1(command: int, payload: bytes = b"", *, response: bool = False) -> bytes:
    if not 0 <= command <= 255:
        raise ValueError("MSP v1 command must fit in one byte")
    if len(payload) > 255:
        raise ValueError("MSP v1 payload is limited to 255 bytes")

    direction = b">" if response else b"<"
    size = len(payload)
    return b"$M" + direction + bytes((size, command)) + payload + bytes((_checksum(size, command, payload),))


def decode_msp_v1(frame: bytes) -> tuple[int, bytes]:
    if len(frame) < 6 or not frame.startswith(b"$M"):
        raise MSPError("invalid MSP v1 frame")
    if frame[2:3] not in {b"<", b">"}:
        raise MSPError("invalid MSP v1 direction byte")

    size = frame[3]
    command = frame[4]
    payload = frame[5 : 5 + size]
    if len(payload) != size:
        raise MSPError("truncated MSP payload")
    if len(frame) != 6 + size:
        raise MSPError("unexpected trailing bytes in MSP frame")

    checksum = frame[5 + size]
    if checksum != _checksum(size, command, payload):
        raise MSPError("checksum mismatch")

    return command, payload


def build_api_version_request() -> bytes:
    return encode_msp_v1(MSP_API_VERSION)


def build_set_raw_rc(channels: Sequence[int]) -> bytes:
    if len(channels) != 8:
        raise ValueError("MSP_SET_RAW_RC expects exactly 8 channels")

    payload = bytearray()
    for channel in channels:
        if not 0 <= int(channel) <= 0xFFFF:
            raise ValueError("RC channel values must fit in uint16")
        payload.extend(int(channel).to_bytes(2, "little", signed=False))

    return encode_msp_v1(MSP_SET_RAW_RC, bytes(payload))
