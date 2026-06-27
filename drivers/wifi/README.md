# Wi-Fi Driver Plan

TeamOS uses the Linux Wi-Fi stack instead of writing custom Wi-Fi drivers.

Expected Linux pieces:

- `cfg80211`
- `mac80211`
- `rfkill`
- device-specific kernel Wi-Fi drivers
- NetworkManager in userland

TeamOS service:

- `system.teamos_internal.wifi.NetworkManagerWifiService`

The settings UI should call the TeamOS Wi-Fi service, and that service should
call NetworkManager instead of touching drivers directly.
