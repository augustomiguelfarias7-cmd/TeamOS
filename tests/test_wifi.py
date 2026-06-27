import subprocess
import unittest
from unittest.mock import patch

from system.teamos_internal.wifi import NetworkManagerWifiService, WifiError


class NetworkManagerWifiServiceTest(unittest.TestCase):
    def test_parse_networks_from_nmcli_output(self):
        service = NetworkManagerWifiService()
        output = "yes:HomeWifi:88:WPA2\nno:Cafe:61:WPA1 WPA2\nno::30:--\n"

        networks = service._parse_networks(output)

        self.assertEqual(len(networks), 2)
        self.assertEqual(networks[0].ssid, "HomeWifi")
        self.assertEqual(networks[0].signal, 88)
        self.assertEqual(networks[0].security, "WPA2")
        self.assertTrue(networks[0].active)
        self.assertEqual(networks[1].ssid, "Cafe")
        self.assertFalse(networks[1].active)

    @patch("system.teamos_internal.wifi.subprocess.run")
    def test_connect_uses_nmcli_without_shell(self, run):
        run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        service = NetworkManagerWifiService()

        service.connect("HomeWifi", "secret-password")

        run.assert_called_once_with(
            ["nmcli", "device", "wifi", "connect", "HomeWifi", "password", "secret-password"],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_connect_requires_ssid(self):
        service = NetworkManagerWifiService()

        with self.assertRaises(WifiError):
            service.connect("   ")


if __name__ == "__main__":
    unittest.main()
