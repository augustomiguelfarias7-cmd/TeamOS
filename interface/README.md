# TeamOS Interface

This folder starts the TeamOS user interface layer. The interface is planned to use Android-style technologies and structure: Kotlin for shell logic and XML-style layouts for screens.

The first target is not a full Android app or a complete Linux mobile shell yet. It is a clean interface blueprint that can grow into the TeamOS shell.

## Initial screens

- **Login e-mail screen**: first-run entry point that asks only for the user e-mail.
- **Greeting screen**: says hello using the display name derived from the e-mail.
- **PIN creation screen**: asks the user to create a local numeric PIN before opening TeamOS.
- **Home screen**: search-first launcher with recent sites and a settings gear in the top-right corner.
- **Settings screen**: normal operating-system settings area with sections for about, battery, network, display, sound, privacy, assistant, and system.

## Navigation

The settings screen opens from the home screen gear button:

```text
Login e-mail -> greeting -> PIN creation -> Home screen -> top-right gear -> Settings
```

## Language direction

The UI layer is intentionally structured around Android-style interface languages:

- Kotlin for interface state and screen definitions.
- XML-style resources for layouts and strings.

Linux remains the planned internal base for kernel, drivers, services, and lower-level behavior.
