# Contributing to ForgeOS

ForgeOS is currently an experimental distribution. Changes should stay small, reviewable, and aligned with the blueprint.

## Development flow

1. Open an issue describing the user-visible outcome and failure behavior.
2. Record architectural tradeoffs in `docs/decisions` for storage, privilege, update, installer, or security changes.
3. Add tests before privileged behavior is enabled.
4. Run `go test ./...` and `./scripts/validate-config.sh` on Linux.
5. Include screenshots for interface changes and QEMU evidence for boot changes.

Generated ISO images and build caches must not be committed. Release artifacts belong in a signed GitHub release.

