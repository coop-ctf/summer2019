FROM ubuntu:bionic

$SSH_STEPS

RUN useradd -m admin

COPY reverse/c-buffer-overflow-variable/src/ .

RUN gcc -fno-stack-protector -o program program.c && \
    sed -i 's/yGmOl7Yry9YyVTI8IPRz56Oe21GfSRHu/.../g' program.c && \
    chown admin program && \
    chown admin program.c && \
    chmod 111 program && \
    chmod 444 program.c

