#!/usr/bin/env bash
set -euo pipefail

repo="https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git"
branch="linux-6.12.y"
destination="external/linux"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="$2"
      shift 2
      ;;
    --branch)
      branch="$2"
      shift 2
      ;;
    --destination)
      destination="$2"
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -e "$destination" ]]; then
  echo "destination already exists: $destination" >&2
  exit 1
fi

mkdir -p "$(dirname "$destination")"
git clone --depth 1 --branch "$branch" "$repo" "$destination"

echo "Linux kernel source fetched into $destination"
