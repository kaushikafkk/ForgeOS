# ForgeOS implementation status

Last reviewed: 24 November 2026

## Implemented

- Debian 13 amd64 ISO-hybrid `live-build` configuration.
- KDE Plasma developer package profile and Calamares installer packages.
- ForgeOS system identity, wallpaper, boot splash, desktop launchers, and native GTK 4 Forge Hub.
- Versioned read-only Go API over a bounded Unix socket.
- `forged` systemd socket/service units with sandboxing.
- `forge status` human and JSON output.
- Unit tests for status, version rejection, and action rejection.
- Configuration validation and CI build/test workflow.
- ISO workflow with downloadable image and checksum artifacts, El Torito inspection, and a privileged Debian build environment.
- QEMU boot-proof workflow with checksum verification and timed native framebuffer captures.
- Latest QEMU proof reached KDE, opened Forge Hub, and reported a healthy response from `forged`.
- Architecture, security, build, roadmap, blueprint, and screenshot evidence.

## Demonstrated but not yet integrated

- Forge Hub reads daemon health from the versioned Unix socket; workspace, update, and recovery panels remain guarded placeholders.
- The Polkit file defines inspection only; mutations have no policy or implementation.
- Concept screens remain product references and are clearly labeled as such; the README now leads with a native screenshot captured from the built image.

## Not implemented

- Tested disk installation or upgrade from a previous ForgeOS release.
- Btrfs snapshot creation, rollback, or boot-entry integration.
- Workspace creation, update transactions, repair, diagnostics export, or package rollback.
- Signed repositories, Secure Boot signing, SBOM publication, or image attestation.
- Hardware qualification, accessibility lab validation, or QEMU fault matrix.
- ARM64 images.

## Milestone-zero release gate

The repository is published as an engineering foundation with passing CI, a built hybrid ISO, inspected boot records, and QEMU boot evidence. It is not a stable operating-system release and must not be represented as one.
