#!/bin/sh
set -eu

if [ "$(id -u)" -ne 0 ]; then
  echo "build-iso.sh must run as root inside a disposable Debian build environment" >&2
  exit 1
fi

command -v lb >/dev/null 2>&1 || {
  echo "live-build is required" >&2
  exit 1
}

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"
mkdir -p .build
lb clean --purge
lb config
lb build

image=$(find . -maxdepth 1 -type f -name 'live-image-*.hybrid.iso' -print -quit)
if [ -z "$image" ]; then
  echo "live-build completed without producing an ISO" >&2
  exit 1
fi
mv "$image" .build/forgeos-amd64.hybrid.iso
sha256sum .build/forgeos-amd64.hybrid.iso > .build/forgeos-amd64.hybrid.iso.sha256
echo "built .build/forgeos-amd64.hybrid.iso"
