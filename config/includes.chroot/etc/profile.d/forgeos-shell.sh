#!/bin/sh
if [ -n "${BASH_VERSION:-}" ] && [ -n "${PS1:-}" ]; then
  PS1='\[\033[1;36m\]\u@\h\[\033[0m\]:\[\033[1;35m\]\w\[\033[0m\]$ '
fi
