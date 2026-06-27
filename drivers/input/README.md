# Input Driver Plan

TeamOS expects touchscreen and button input from the Linux input stack.

Expected Linux pieces:

- input subsystem
- evdev
- touchscreen drivers
- power-button input events

The power-button triple press for ChatGusto should be implemented as a TeamOS
input service above Linux input events, not inside a device driver.
