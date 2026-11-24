#!/bin/sh
set -eu

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"

required='config/auto/config
config/package-lists/forgeos.list.chroot
config/includes.chroot/etc/os-release
config/includes.chroot/etc/systemd/system/forged.service
config/includes.chroot/etc/systemd/system/forged.socket
config/includes.chroot/usr/bin/forge-hub
config/includes.chroot/usr/bin/forgeos-session-setup
config/includes.chroot/usr/bin/forge-shell-welcome
config/includes.chroot/usr/share/forgeos/forge-hub.css
config/includes.chroot/usr/share/applications/forge-hub.desktop'

printf '%s\n' "$required" | while IFS= read -r path; do
  [ -s "$path" ] || { echo "missing or empty: $path" >&2; exit 1; }
done

grep -q '^ID=forgeos$' config/includes.chroot/etc/os-release
grep -q 'mutations_enabled.*false' config/includes.chroot/etc/forgeos/release.json
grep -q '^ListenStream=/run/forgeos/forged.sock$' config/includes.chroot/etc/systemd/system/forged.socket
grep -q '^NoNewPrivileges=true$' config/includes.chroot/etc/systemd/system/forged.service
grep -q 'forgeos-layoutEnabled=true' config/includes.chroot/etc/skel/.config/kwinrc
grep -q 'System healthy' config/includes.chroot/usr/bin/forge-hub

echo "ForgeOS configuration validation passed"
