import unittest

from dji_betaflight_bridge.msp import MSP_SET_RAW_RC, build_api_version_request, build_set_raw_rc, decode_msp_v1


class MSPTests(unittest.TestCase):
    def test_raw_rc_roundtrip(self) -> None:
        frame = build_set_raw_rc([1000, 1500, 1500, 2000, 1500, 1500, 1500, 1500])
        command, payload = decode_msp_v1(frame)

        self.assertEqual(command, MSP_SET_RAW_RC)
        self.assertEqual(len(payload), 16)
        self.assertEqual(int.from_bytes(payload[0:2], "little"), 1000)
        self.assertEqual(int.from_bytes(payload[6:8], "little"), 2000)

    def test_api_version_request(self) -> None:
        frame = build_api_version_request()
        command, payload = decode_msp_v1(frame)

        self.assertEqual(command, 1)
        self.assertEqual(payload, b"")


if __name__ == "__main__":
    unittest.main()
