#!/bin/sh
trap 'printf "%s\n" "cleanup complete"; exit 0' EXIT
false
exit "$?"
