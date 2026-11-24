# Building and testing ForgeOS

## Core service

Go 1.23 or newer is required.

```bash
go test -race ./...
go build -o bin/forged ./cmd/forged
go build -o bin/forge ./cmd/forge
```

On Linux, start the service against a temporary socket:

```bash
./bin/forged --socket /tmp/forged.sock
./bin/forge status --socket /tmp/forged.sock
./bin/forge status --json --socket /tmp/forged.sock
```

## Configuration validation

```bash
bash scripts/validate-config.sh
```

The validator checks required image files, branded identity, disabled mutations, the socket path, and systemd hardening. CI also runs formatting, race-enabled tests, and builds both binaries.

## ISO build

Build inside a disposable Debian 13 VM or container with root access and at least 30 GB free disk space.

```bash
apt update
apt install live-build debootstrap squashfs-tools xorriso isolinux syslinux-common golang
mkdir -p config/includes.chroot/usr/libexec/forgeos config/includes.chroot/usr/bin
CGO_ENABLED=0 go build -trimpath -o config/includes.chroot/usr/libexec/forgeos/forged ./cmd/forged
CGO_ENABLED=0 go build -trimpath -o config/includes.chroot/usr/bin/forge ./cmd/forge
bash scripts/build-iso.sh
```

The result and checksum are written below `.build/`. The manual GitHub Actions workflow performs the same build and retains the ISO as a short-lived artifact.

## Virtual machine smoke test

Boot the ISO with UEFI enabled, at least 4 GB RAM, two CPU cores, and a 30 GB virtual disk. Confirm KDE loads, Forge Hub opens, networking works, `forge status` reaches `forged`, the live installer starts, and no mutation controls claim to work.

## Native Forge Hub

Forge Hub requires Python GObject bindings and GTK 4. It is included in the live image and can be run in a Debian development environment with:

```bash
sudo apt install python3-gi gir1.2-gtk-4.0
python3 config/includes.chroot/usr/bin/forge-hub
```

Capture release screenshots from this native application or the built ISO. Do not use the retired browser prototype as implementation evidence.
