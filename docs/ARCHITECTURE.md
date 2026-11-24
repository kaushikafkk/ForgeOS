# ForgeOS architecture

ForgeOS milestone zero is a Debian-derived live system with a KDE Plasma desktop, a read-only local control plane, and a browser-based Forge Hub prototype. It intentionally reuses mature upstream components instead of replacing the Linux kernel, init system, package manager, compositor, encryption stack, or container runtime.

## Trust boundaries

```text
unprivileged user
  Forge Hub and forge CLI
          |
  versioned request schema
          |
  Unix socket and group boundary
          |
  forged read-only service
          |
  systemd sandbox and future Polkit checks
          |
  Debian system state
```

The current API exposes `status.read` only. Snapshot, update, repair, and workspace operations are marked as planned capabilities and cannot mutate the host. This is deliberate: privileged actions must gain explicit policy, audit records, idempotency, and tested recovery behavior together.

## Image layer

The `config/` tree is consumed by Debian `live-build`. It selects Debian 13, an amd64 ISO-hybrid image, KDE Plasma, developer tools, Podman, Flatpak, Btrfs utilities, firmware updates, encryption tools, and Calamares. Chroot includes provide ForgeOS identity, systemd units, the Forge Hub prototype, the desktop launcher, and a placeholder inspection policy.

## Control service

`forged` accepts one bounded JSON request per Unix-socket connection. Requests and responses carry the `forgeos.dev/v1` schema version. Input is capped at 64 KiB and unknown versions or actions fail closed. The systemd unit enables a strict filesystem and kernel sandbox.

## Interface

Forge Hub presents system health, reproducible workspaces, planned updates, and recovery as one visual model. The prototype has functional navigation, keyboard focus, responsive layouts, a command shortcut, and a transparent message whenever a requested mutation is not implemented.

## Next architecture gates

1. Add D-Bus transport and complete Polkit action design.
2. Introduce append-only operation records and correlation identifiers.
3. Implement Btrfs snapshot inspection before snapshot creation.
4. Run QEMU update, power-loss, disk-pressure, and rollback scenarios.
5. Sign images and publish an SBOM and build provenance.
