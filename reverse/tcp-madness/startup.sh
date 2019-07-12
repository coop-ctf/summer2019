#!/bin/bash

sudo -u admin python3 /home/guest/server.py &
python3 /home/guest/client.py &
cd /home/guest
