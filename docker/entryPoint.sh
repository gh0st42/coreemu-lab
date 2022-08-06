#!/bin/bash

systemctl enable ssh
service ssh start
#service core-daemon start
/update-custom-services.sh

core-daemon > /var/log/core-daemon.log 2>&1 &

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

if [ ! -z "$SSHKEY" ]; then
	echo "Adding ssh key: $SSHKEY"
	mkdir /root/.ssh
	chmod 755 ~/.ssh
	echo $SSHKEY > /root/.ssh/authorized_keys
    chmod 644 /root/.ssh/authorized_keys	
fi

FILE=/shared/experiment.conf
if [ -f "$FILE" ]; then
    echo "$FILE exists."
	sleep 1
	time core-experiment $FILE 2>&1 | tee /shared/experiment.log
else 
	core-gui
fi
