#!/usr/bin/env bash
set -e

# Enable corepack and pnpm
corepack enable >/dev/null 2>&1 || true

# Ensure Node.js v20
REQUIRED=20
CURRENT=$(node -v 2>/dev/null || true)
if [[ ! "$CURRENT" =~ v${REQUIRED} ]]; then
  if command -v nvm >/dev/null 2>&1; then
    nvm install "$REQUIRED"
    nvm use "$REQUIRED"
  else
    echo "nvm not found; please install Node.js v${REQUIRED}" >&2
  fi
fi

# Backend dependencies
if [ -d backend ]; then
  (cd backend && pip install .)
fi

# Frontend dependencies
if [ -d frontend ]; then
  (cd frontend && pnpm install --frozen-lockfile)
fi

# Copy env file
if [ -f backend/.env.example ] && [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
fi
