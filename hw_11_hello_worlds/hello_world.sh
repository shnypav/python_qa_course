#!/usr/bin/env bash
printf '%s\n' '[INFO] Program started' >&2
printf 'What is your name? '
read -r name
printf 'Hello, %s!\n' "$name"
printf '%s\n' '[INFO] Greeting printed' >&2
