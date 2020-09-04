#!/usr/bin/env bash
##
## Copyright (C) 2020 Prof_Bloodstone.
##
## This file is part of mineager
## (see https://github.com/Prof-Bloodstone/Mineager).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##
##

set -euo pipefail

if (( $# == 0 )); then
  args=( mineager/ )
else
  args=("${@}")
fi

licenseheaders -t ./LICENSE_TEMPLATE.md -y 2020 -o "Prof_Bloodstone" -n "mineager" -u 'https://github.com/Prof-Bloodstone/Mineager'
isort --profile black "${args[@]}"
autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports --exclude '__init__.py' "${args[@]}"
black "${args[@]}"
