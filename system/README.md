# TeamOS Internal System

This folder contains the first internal TeamOS services that sit between the Android-style interface and the Linux-based system internals.

TeamOS will import most low-level behavior from Linux. The files here focus on the parts TeamOS needs to control directly:

- **Agent Mode guard**: validates ChatGusto system-access requests before any permission prompt is shown.
- **Wi-Fi service**: wraps Linux NetworkManager commands so the TeamOS settings UI can list networks and connect to Wi-Fi.

These modules are intentionally small and testable. They are not a full operating system yet, but they define the internal service contracts the interface can call later.

## Services

```text
system/teamos_internal/
├── agent_mode.py  # ChatGusto Agent Mode checks and permission grants
├── models.py      # shared internal data models
└── wifi.py        # Linux Wi-Fi operations through nmcli
```

## Safety rules

Agent Mode must never grant broad system access automatically. It should:

1. verify the requesting origin;
2. reject unknown or unsafe origins;
3. review requested permissions;
4. return a result that the UI can show to the user;
5. only create an agent session after explicit user approval.

Wi-Fi operations must go through Linux system tools instead of custom drivers. The initial implementation targets NetworkManager through `nmcli`.
