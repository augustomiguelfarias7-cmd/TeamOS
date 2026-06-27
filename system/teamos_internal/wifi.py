"""Linux Wi-Fi integration for TeamOS.

The first TeamOS Wi-Fi service talks to NetworkManager through `nmcli`. This
lets TeamOS import Linux networking behavior instead of implementing Wi-Fi
drivers or connection management from scratch.
"""

from __future__ import annotations

import subprocess
from collections.abc import Sequence

from .models import WifiNetwork


class WifiError(RuntimeError):
    """Raised when a Wi-Fi command fails."""


class NetworkManagerWifiService:
    """Wi-Fi service backed by Linux NetworkManager."""

    def __init__(self, nmcli_path: str = "nmcli") -> None:
        self.nmcli_path = nmcli_path

    def list_networks(self) -> list[WifiNetwork]:
        """Return visible Wi-Fi networks using `nmcli`."""

        output = self._run(
            [
                self.nmcli_path,
                "-t",
                "-f",
                "ACTIVE,SSID,SIGNAL,SECURITY",
                "device",
                "wifi",
                "list",
            ]
        )
        return self._parse_networks(output)

    def connect(self, ssid: str, password: str | None = None) -> None:
        """Connect to a Wi-Fi network by SSID."""

        if not ssid.strip():
            raise WifiError("SSID é obrigatório para conectar ao Wi-Fi.")

        command = [self.nmcli_path, "device", "wifi", "connect", ssid]
        if password:
            command.extend(["password", password])

        self._run(command)

    def disconnect(self) -> None:
        """Disconnect Wi-Fi using NetworkManager radio control."""

        self._run([self.nmcli_path, "radio", "wifi", "off"])

    def enable(self) -> None:
        """Enable Wi-Fi using NetworkManager radio control."""

        self._run([self.nmcli_path, "radio", "wifi", "on"])

    def _run(self, command: Sequence[str]) -> str:
        try:
            completed = subprocess.run(
                list(command),
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise WifiError("nmcli não foi encontrado. NetworkManager é necessário.") from exc
        except subprocess.CalledProcessError as exc:
            message = exc.stderr.strip() or exc.stdout.strip() or "comando Wi-Fi falhou"
            raise WifiError(message) from exc

        return completed.stdout

    def _parse_networks(self, output: str) -> list[WifiNetwork]:
        networks: list[WifiNetwork] = []
        for line in output.splitlines():
            if not line.strip():
                continue

            active, ssid, signal, security = self._split_nmcli_line(line)
            if not ssid:
                continue

            networks.append(
                WifiNetwork(
                    ssid=ssid,
                    signal=self._parse_signal(signal),
                    security=security or "--",
                    active=active == "yes",
                )
            )

        return networks

    def _split_nmcli_line(self, line: str) -> tuple[str, str, str, str]:
        parts = line.split(":")
        padded = [*parts, "", "", "", ""]
        return padded[0], padded[1], padded[2], ":".join(padded[3:]).rstrip(":")

    def _parse_signal(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            return 0
