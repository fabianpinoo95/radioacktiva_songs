#!/usr/bin/env bash
set -o errexit  # para que falle si algo falla

apt-get update
apt-get install -y chromium chromium-driver

pip install -r requirements.txt