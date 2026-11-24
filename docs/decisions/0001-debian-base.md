# ADR 0001 Debian Stable base

## Status

Accepted for milestone zero

## Decision

ForgeOS derives from Debian 13 and uses Debian `live-build`, packages, repositories, kernel, systemd, Plasma, and installer components.

## Rationale

The project is about a coherent developer experience, controlled privileged operations, and visible recovery. Replacing mature infrastructure would consume the project without improving those differentiators. Debian provides reproducible inputs, broad hardware support, a conservative security model, and a well-understood derivative path.

## Consequences

ForgeOS must track Debian licensing, security advisories, derivative requirements, and release cadence. Product branding cannot imply that Debian upstream supports ForgeOS.
