# ForgeOS implementation status

Last reviewed: 24 November 2026

## Implemented

- Debian 13 amd64 ISO-hybrid `live-build` configuration.
- KDE Plasma developer package profile and Calamares installer packages.
- ForgeOS system identity, icon, desktop launcher, and Forge Hub prototype.
- Versioned read-only Go API over a bounded Unix socket.
- `forged` systemd socket/service units with sandboxing.
- `forge status` human and JSON output.
- Unit tests for status, version rejection, and action rejection.
- Configuration validation and CI build/test workflow.
- Manual ISO workflow with downloadable image and checksum artifacts.
- Architecture, security, build, roadmap, blueprint, and screenshot evidence.

## Demonstrated but not yet integrated

- Forge Hub uses representative local state and does not yet subscribe to the daemon.
- The Polkit file defines inspection only; mutations have no policy or implementation.
- Concept screens remain product references and are clearly labeled as such.

## Not implemented

- Tested disk installation or upgrade from a previous ForgeOS release.
- Btrfs snapshot creation, rollback, or boot-entry integration.
- Workspace creation, update transactions, repair, diagnostics export, or package rollback.
- Signed repositories, Secure Boot signing, SBOM publication, or image attestation.
- Hardware qualification, accessibility lab validation, or QEMU fault matrix.
- ARM64 images.

## Milestone-zero release gate

The repository is ready to publish as an engineering foundation when CI passes on GitHub and the manual ISO workflow produces an image. It is not a stable operating-system release and must not be represented as one.
