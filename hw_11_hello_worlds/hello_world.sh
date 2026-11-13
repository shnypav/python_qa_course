#!/usr/bin/env bash

printf "What is your name? "
IFS= read -r name || true
printf "Hello, %s!\n" "$name"
