#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

if ! command -v docker >/dev/null 2>&1; then
  if [[ "$(uname -s)" != Linux ]] || [[ ! -f /etc/os-release ]]; then
    echo "Install Docker Desktop on macOS/Windows, then rerun this script. Linux Debian/Ubuntu installation is automatic." >&2
    exit 1
  fi
  source /etc/os-release
  if [[ "${ID:-}" != ubuntu && "${ID:-}" != debian ]]; then
    echo "Automatic Docker installation supports Debian/Ubuntu. Install Docker Engine and the Compose plugin, then rerun." >&2
    exit 1
  fi
  SUDO=()
  if [[ "$EUID" -ne 0 ]]; then SUDO=(sudo); fi
  "${SUDO[@]}" apt-get update
  "${SUDO[@]}" apt-get install -y ca-certificates curl
  "${SUDO[@]}" install -m 0755 -d /etc/apt/keyrings
  "${SUDO[@]}" curl -fsSL "https://download.docker.com/linux/$ID/gpg" -o /etc/apt/keyrings/docker.asc
  "${SUDO[@]}" chmod a+r /etc/apt/keyrings/docker.asc
  ARCH="$(dpkg --print-architecture)"
  CODENAME="${UBUNTU_CODENAME:-${VERSION_CODENAME}}"
  printf 'Types: deb\nURIs: https://download.docker.com/linux/%s\nSuites: %s\nComponents: stable\nArchitectures: %s\nSigned-By: /etc/apt/keyrings/docker.asc\n' "$ID" "$CODENAME" "$ARCH" | "${SUDO[@]}" tee /etc/apt/sources.list.d/docker.sources >/dev/null
  "${SUDO[@]}" apt-get update
  "${SUDO[@]}" apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  "${SUDO[@]}" service docker start
fi

DOCKER=(docker)
if ! docker info >/dev/null 2>&1; then
  if command -v sudo >/dev/null 2>&1 && sudo docker info >/dev/null 2>&1; then DOCKER=(sudo docker)
  else echo "Docker is installed but its daemon is not available. Start Docker and rerun." >&2; exit 1; fi
fi
"${DOCKER[@]}" compose version >/dev/null
"${DOCKER[@]}" run --rm --user "$(id -u):$(id -g)" -v "$PROJECT_ROOT:/workspace" -w /workspace python:3.12-alpine python scripts/configure_env.py
"${DOCKER[@]}" compose up --build -d --wait --wait-timeout 240
echo "Nour is ready. Open http://localhost:3000 and create your account."
echo "If WEB_PORT was customized in .env, use that port instead. No demo credentials are created."
