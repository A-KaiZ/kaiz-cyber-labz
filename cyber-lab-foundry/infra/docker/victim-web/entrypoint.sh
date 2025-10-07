#!/bin/bash
set -Eeuo pipefail

export FLASK_APP=app:app
exec flask run --host=0.0.0.0 --port=5000
