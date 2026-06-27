# TeamOS Driver Layer

TeamOS imports most hardware support from Linux. This folder documents the driver
categories TeamOS expects and how the interface/internal services should connect
to Linux-backed driver stacks.

TeamOS should not rewrite Wi-Fi, display, touchscreen, audio, battery, or USB
drivers from scratch unless a small TeamOS-specific adapter is truly needed.

## Driver manifests

```text
drivers/manifests/mobile.toml
```

The manifest lists the first driver categories TeamOS expects from Linux:

- Wi-Fi through cfg80211/mac80211 and NetworkManager userland.
- Display through DRM/KMS.
- Touch input through evdev/libinput-style input events.
- Audio through ALSA/PipeWire.
- Power and battery through Linux power_supply and UPower-style userland.

## Category folders

Each category folder contains a small README describing the Linux components
TeamOS plans to use.
