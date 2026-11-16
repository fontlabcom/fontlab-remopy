#!/bin/sh
# this_file: test.sh
# SPDX-License-Identifier: Apache-2.0
set -eu
uv run --extra test python -m pytest "$@"
