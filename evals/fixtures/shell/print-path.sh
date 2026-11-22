#!/bin/sh
set -eu
case "$1" in
    unsafe) shift; printf '<%s>\n' $1 ;;
    safe) shift; printf '<%s>\n' "$1" ;;
esac
