FROM ubuntu:18.04

$SSH_STEPS

RUN printf "A web server is running on a port in the range 41000 to 46000\nnmap & nc are installed\n" > info.txt
CMD ncat -lk -p 41054 --sh-exec "echo FLAG{Ey5tkCz7q5560YXsOktcmluHS169L7pqX3wHscoa}" & /usr/sbin/sshd -D
