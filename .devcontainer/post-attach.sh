#!/usr/bin/env bash
echo "starting docker compose up"
bash -x ./start.sh
curl -LsSf https://astral.sh/uv/install.sh | sh