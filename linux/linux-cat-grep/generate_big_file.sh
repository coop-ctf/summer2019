#!/bin/bash

LINE_COUNT=100000
LINE_BREAK=54245

function generate_fake_flag {
  CURRENT_LINE="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)"
}

for (( i=0; i<$LINE_COUNT; ++i)); do
    if [ $i = $LINE_BREAK ]; then
      echo -e "$(cat actual_flag.txt)" >> flag.txt
    else
      generate_fake_flag
      echo -e "GLAF{$CURRENT_LINE}" >> flag.txt
    fi
done
