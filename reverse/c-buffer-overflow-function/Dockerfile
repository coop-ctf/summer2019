FROM 32bit/ubuntu:16.04

$SSH_STEPS

RUN useradd -m admin

COPY reverse/c-buffer-overflow-function/src/ .

RUN gcc -fno-stack-protector -o program program.c && \
    rm program.c && \
    objdump -d program > objdump.txt && \
    chown admin program && \
    chown admin objdump.txt && \
    chmod 111 program && \
    chmod 444 objdump.txt

