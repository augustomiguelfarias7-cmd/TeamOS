# TeamOS Kernel Layer

TeamOS does not vendor the full Linux kernel source in this repository. Instead,
this folder contains the TeamOS kernel integration files that describe which
Linux kernel baseline TeamOS expects, which configuration fragments it needs,
and where TeamOS-specific patches would live.

## Why the Linux source is not copied here

The Linux kernel and many drivers are very large and already have their own
repositories, build systems, and licenses. TeamOS imports that work instead of
copying millions of lines into this repo.

## Files

```text
kernel/
├── linux.toml                 # Linux kernel source and version target
├── config/team_mobile.conf    # TeamOS mobile kernel config fragment
└── patches/                   # TeamOS-specific Linux patches, if needed later
```

## Planned flow

1. Fetch the Linux kernel source defined in `linux.toml`.
2. Apply TeamOS config fragments.
3. Apply TeamOS patches from `kernel/patches/` when needed.
4. Build the kernel for the selected target device or emulator.

The helper script `tools/fetch_linux_kernel.sh` starts this flow by cloning the
configured Linux repository into an external build directory.
