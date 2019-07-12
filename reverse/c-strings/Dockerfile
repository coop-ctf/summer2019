FROM ubuntu:bionic

$SSH_STEPS

RUN useradd -m admin

COPY reverse/c-strings/src/ .

RUN gcc -o program program.c && \
    rm program.c && \
    chown admin program && \
    chmod 555 program

