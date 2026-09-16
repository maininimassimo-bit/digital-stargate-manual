#!/bin/sh
set -eu

python /app/dsg/container/preflight.py

if [ "$#" -eq 0 ]; then
  echo "NOT_EXECUTED: scientific runner is not materialized" >&2
  exit 78
fi

exec "$@"
