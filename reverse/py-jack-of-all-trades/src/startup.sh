#!/bin/bash

python3 /home/guest/script.pyc &
cd /home/guest/server/
{ python3 -m server & } > /dev/null
cd /home/guest