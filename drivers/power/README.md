# Power and Battery Driver Plan

TeamOS expects power and battery data from Linux power management subsystems.

Expected Linux pieces:

- `power_supply`
- thermal sensors
- charger/battery drivers
- UPower-style userland integration

TeamOS will later add a battery service for percentage, charging state, battery
saver, and power warnings.
