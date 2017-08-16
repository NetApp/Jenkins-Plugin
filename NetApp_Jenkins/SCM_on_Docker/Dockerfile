FROM gitlab/gitlab-ce:latest

COPY startcont.sh /usr/bin/startcont.sh


RUN cd /tmp && curl -O http://repo.jenkins-ci.org/releases/org/jenkins-ci/plugins/swarm-client/2.1/swarm-client-2.1-jar-with-dependencies.jar && \
    chmod +x swarm-client-2.1-jar-with-dependencies.jar
RUN apt-get update
RUN apt-get install -y default-jdk
RUN apt-get install -y python
RUN apt-get install -y python-pip nano xterm
RUN pip install requests

ENTRYPOINT ["/usr/bin/startcont.sh"] 

