#!/usr/bin/env bash

# Build python image
podman build -t python-source:3.11.4 -f ./Dockerfile.Python