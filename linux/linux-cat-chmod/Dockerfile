FROM ubuntu:18.04

$SSH_STEPS

COPY linux/linux-cat-chmod/flag.txt flag.txt
RUN chown -R guest /home/guest && chmod 000 /home/guest/flag.txt
