FROM ubuntu:18.04

$SSH_STEPS

COPY linux/linux-cat-gunzip/flag.txt flag.txt
RUN gzip flag.txt && chown -R guest /home/guest
