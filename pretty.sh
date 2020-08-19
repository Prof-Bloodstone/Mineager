#!/usr/bin/env bash

set -euo pipefail

if (( $# == 0 )); then
  args=( mineager/ )
else
  args=("${@}")
fi

isort --profile black "${args[@]}"
autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports --exclude '__init__.py' "${args[@]}"
black "${args[@]}"
