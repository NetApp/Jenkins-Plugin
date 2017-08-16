FROM ubuntu
RUN apt-get update
COPY docker.list /etc/apt/sources.list.d/docker.list
RUN apt-get install -y apt-transport-https ca-certificates apt-utils
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
RUN apt-get update
RUN apt-get install -y vim nano xterm
RUN apt-cache policy docker-engine net-tools iputils-ping
RUN apt-get install -y docker-engine=1.12.5*


RUN mkdir /tmp/ps
COPY swarm-client-2.1-jar-with-dependencies.jar /tmp/swarm-client-2.1-jar-with-dependencies.jar
#COPY slave.jar /tmp/slave.jar
COPY build_artifact_exec.py /tmp/build_artifact_exec.py
COPY clone_purge.py /tmp/clone_purge.py
COPY zipForApprenda.py /tmp/zipForApprenda.py
COPY snapshot_create_write.py /tmp/ps/snapshot_create_write.py
COPY create_snap_structure.py /tmp/ps/create_snap_structure.py
COPY dockerimagecreate.py /tmp/ps/dockerimagecreate.py


RUN apt-get update
RUN apt-get install -y default-jdk
RUN apt-get install -y git
RUN apt-get install -y python
RUN apt-get install -y zip
RUN apt-get install -y maven
RUN apt-get install -y curl
RUN apt-get install -y nano
#RUN apt-get install -y vim
RUN apt-get install -y python-pip
RUN pip install requests
RUN mkdir /tmp/vol1
RUN mkdir /tmp/vol2

ENTRYPOINT exec java -jar /tmp/swarm-client-2.1-jar-with-dependencies.jar -name $slavename -master $masterip -labels $labelname -disableClientsUniqueId -mode exclusive -executors 3
