#!/usr/bin/env bash
prueba error
set -o errexit  # para que falle si algo falla

apt-get update
apt-get install -y chromium chromium-driver

pip install -r requirements.txt