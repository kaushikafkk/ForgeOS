# Security Policy

ForgeOS has not reached a stable security-support release. Do not use it as the only operating system on a machine containing important data.

## Reporting

Report suspected vulnerabilities privately through GitHub Security Advisories when the repository is published. Do not include secrets, personal files, or complete diagnostic archives in public issues.

## Security invariants

- The desktop and CLI are unprivileged clients.
- `forged` exposes named operations, never an arbitrary shell API.
- Mutations require separate Polkit actions and produce audit records.
- Release metadata, packages, container images, and ISO artifacts are authenticated before trust.
- Diagnostic export is local, previewable, redacted, and explicitly initiated.
- The last known-good boot state is never deleted by an incomplete operation.

