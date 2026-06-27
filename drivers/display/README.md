# Display Driver Plan

TeamOS expects display support from the Linux DRM/KMS stack.

Expected Linux pieces:

- DRM
- KMS
- panel drivers
- backlight drivers

TeamOS will later add a display service for brightness, theme, resolution, and
screen state. The interface should not talk to DRM directly.
