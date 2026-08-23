from __future__ import annotations

from typing import Protocol

from .models import ControllerSample


class ControllerSource(Protocol):
    def read(self) -> ControllerSample:
        """Return the next normalized controller sample."""


def decode_controller_payload(payload: bytes) -> ControllerSample:
    """Decode a controller payload into a normalized sample.

    This remains intentionally unimplemented until a lawful capture or
    documented public transport format is available for the target controller.
    """

    raise NotImplementedError(
        "Controller transport decoder not implemented yet; add a lawful capture or public format first."
    )
