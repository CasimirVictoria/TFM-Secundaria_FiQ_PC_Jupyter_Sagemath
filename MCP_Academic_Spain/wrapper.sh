#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PATH="$DIR/venv/bin:$PATH"
export PYTHONPATH="$DIR"
"$DIR/venv/bin/python" "$DIR/server.py" "$@" 2>> "$DIR/error.log"
