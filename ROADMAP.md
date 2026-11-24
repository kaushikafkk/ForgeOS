# ForgeOS Roadmap

The roadmap follows the sequence defined in the product and engineering blueprint.

## Milestone 0 Foundation

- Reproducible repository layout and documented decisions.
- Console and KDE live-image configuration.
- Versioned Forge API and read-only daemon.
- Forge CLI, status model, tests, and CI.
- Browser-based Forge Hub interaction prototype.

## Milestone 1 Live Desktop

- Boot the generated image in UEFI QEMU.
- KDE Plasma on Wayland with ForgeOS defaults.
- NetworkManager, PipeWire, Flatpak, and rootless Podman.
- First-boot experience and reference hardware evidence.

## Milestone 2 Workspace Core

- Versioned workspace manifests and lock files.
- Rootless Podman lifecycle and resource controls.
- Go, Rust, Node, Python, Java, PostgreSQL, and Redis templates.
- Code, Test, and Ship modes with health checks.

## Milestone 3 System Control

- D-Bus API and Polkit actions for named operations.
- Btrfs snapshot inventory and verified snapshot creation.
- Diagnostic bundles with preview and redaction.
- Forge Hub native shell integration.

## Milestone 4 Installer

- Guided encrypted installation and advanced partitioning.
- Stable disk identity and destructive-operation review.
- First-boot account and configuration flow.

## Milestone 5 Update and Recovery

- Snapshot-protected APT transactions.
- Boot health verification and rollback entry.
- Offline recovery environment and boot repair.
- Power-loss, disk-full, corrupt-metadata, and failed-service tests.

## Milestone 6 Release

- Signed ISO, checksums, SBOM, source packages, and provenance.
- Accessibility and hardware test matrix.
- Five-minute portfolio demonstration from released artifacts.
- Public beta with known limitations and support matrix.

