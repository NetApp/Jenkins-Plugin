FROM openjdk:8-jdk

MAINTAINER Akshay.Patil@Netapp.com
#RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
RUN apt-get clean
RUN apt-get update && apt-get install -y git curl zip && rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install -y sudo python-pip xterm
RUN pip install requests
RUN pip install texttable

#Docker install
COPY docker.list /etc/apt/sources.list.d/docker.list
RUN apt-get install -y apt-transport-https ca-certificates apt-utils
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y nano
RUN apt-cache policy docker-engine
RUN apt-get install -y docker-engine=1.12.5*



# nDVP Installation
# download and unpack the application
RUN wget https://github.com/NetApp/netappdvp/releases/download/v1.3/netappdvp-1.3.tar.gz
RUN tar zxf netappdvp-1.3.tar.gz

# move to a location in the bin path
RUN mv netappdvp /usr/local/bin
RUN chown root:root /usr/local/bin/netappdvp
RUN chmod 755 /usr/local/bin/netappdvp

# create a location for the config files
RUN mkdir -p /etc/netappdvp


COPY ontap-nas.json /etc/netappdvp/ontap-nas.json
#CMD netappdvp --config=/etc/netappdvp/ontap-nas.json &


ENV JENKINS_HOME /var/jenkins_home
ENV JENKINS_SLAVE_AGENT_PORT 50000
ENV TERM xterm

ARG user=jenkins
ARG group=jenkins
ARG uid=1000
ARG gid=1000

# Jenkins is run with user `jenkins`, uid = 1000
# If you bind mount a volume from the host or a data container, 
# ensure you use the same uid
RUN groupadd -g ${gid} ${group} \
    && useradd -d "$JENKINS_HOME" -u ${uid} -g ${gid} -m -s /bin/bash ${user}

# Jenkins home directory is a volume, so configuration and build history 
# can be persisted and survive image upgrades
VOLUME /var/jenkins_home

# `/usr/share/jenkins/ref/` contains all reference configuration we want 
# to set on a fresh new installation. Use it to bundle additional plugins 
# or config file with your custom jenkins Docker image.
RUN mkdir -p /usr/share/jenkins/ref/init.groovy.d


RUN mkdir -p /tmp/ps
RUN mkdir -p /tmp/vol1
RUN mkdir -p /tmp/vol2




ENV TINI_VERSION 0.14.0
ENV TINI_SHA 6c41ec7d33e857d4779f14d9c74924cab0c7973485d2972419a3b7c7620ff5fd

# Use tini as subreaper in Docker container to adopt zombie processes 
RUN curl -fsSL https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini-static-amd64 -o /bin/tini && chmod +x /bin/tini \
  && echo "$TINI_SHA  /bin/tini" | sha256sum -c -

COPY init.groovy /usr/share/jenkins/ref/init.groovy.d/tcp-slave-agent-port.groovy

RUN mkdir -p /usr/share/jenkins/ref/jobs/Source_Code_Management\(SCM\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Build_Artifact_Management\(BAM\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Developer_Workspace\(DWS\)
RUN mkdir -p /usr/share/jenkins/ref/jobs/Continous_Integration\(CI\)



COPY Build_Artifact_Management\(BAM\) /usr/share/jenkins/ref/jobs/Build_Artifact_Management\(BAM\)
COPY Continous_Integration\(CI\) /usr/share/jenkins/ref/jobs/Continous_Integration\(CI\)
COPY Developer_Workspace\(DWS\) /usr/share/jenkins/ref/jobs/Developer_Workspace\(DWS\)
COPY Source_Code_Management\(SCM\) /usr/share/jenkins/ref/jobs/Source_Code_Management\(SCM\)
COPY Build_Artifacts_JFrog_2017 /usr/share/jenkins/ref/jobs/Build_Artifacts_JFrog_2017
COPY CreateDockerImage /usr/share/jenkins/ref/jobs/CreateDockerImage
COPY JFrog_2017_1 /usr/share/jenkins/ref/jobs/JFrog_2017_1
COPY JFrog_OSS_Repo /usr/share/jenkins/ref/jobs/JFrog_OSS_Repo
#COPY ListBuildCheckpoints /usr/share/jenkins/ref/jobs/ListBuildCheckpoints
COPY UserWorkspace /usr/share/jenkins/ref/jobs/UserWorkspace
COPY ZipAndCopy /usr/share/jenkins/ref/jobs/ZipAndCopy
COPY ListSCMCheckpoints /usr/share/jenkins/ref/jobs/List_SCM_Checkpoints
COPY ListBuildCheckPoints /usr/share/jenkins/ref/jobs/List_Build_CheckPoints
COPY SCMCheckpoints /usr/share/jenkins/ref/jobs/SCMCheckpoints
COPY CreateBuildCheckpoints /usr/share/jenkins/ref/jobs/CreateBuildCheckpoints
COPY Purge_Policy /usr/share/jenkins/ref/jobs/Purge_Policy
#COPY JFrog_CI_Build /usr/share/jenkins/ref/jobs/JFrog_CI_Build


COPY build_artifact_create.py /tmp/ps/build_artifact_create.py
COPY clone_list.py /tmp/ps/clone_list.py
COPY clone_purge.py /tmp/ps/clone_purge.py
COPY Volume_create.py /tmp/ps/Volume_create.py
COPY user_workspace_creation1.py /tmp/ps/user_workspace_creation1.py
COPY scmconfig2.py /tmp/ps/scmconfig2.py
COPY CI_dev_branch_create2.py /tmp/ps/CI_dev_branch_create2.py
COPY Jenkins_slave_create2.py /tmp/ps/Jenkins_slave_create2.py
COPY snapshot_delete.py /tmp/ps/snapshot_delete.py
COPY snap_show.py /tmp/ps/snap_show.py
COPY snapshot_create.py /tmp/ps/snapshot_create.py
COPY volume_list.py /tmp/ps/volume_list.py
COPY svm_aggr_list.py /tmp/ps/svm_aggr_list.py
COPY build_artifact_container_purge.py /tmp/ps/build_artifact_container_purge.py
#COPY dockerimagecreate.py /tmp/ps/dockerimagecreate.py
COPY create_snap_structure.py /tmp/ps/create_snap_structure.py
COPY scmcheckpoint_create.py /tmp/ps/scmcheckpoint_create.py
COPY snaps2.properties /usr/share/jenkins/ref/snaps2.properties
COPY snapshot_create_write.py /tmp/ps/snapshot_create_write.py
COPY purge.py /tmp/ps/purge.py
COPY config.xml /usr/share/jenkins/ref/config.xml


ARG JENKINS_VERSION
ENV JENKINS_VERSION ${JENKINS_VERSION:-2.71}

# jenkins.war checksum, download will be validated using it
ARG JENKINS_SHA=14727da24054e956dc8b8514998e19001c99efce637891f544d2a9b3d9ea752c

#Can be used to customize where jenkins.war get downloaded from
ARG JENKINS_URL=https://repo.jenkins-ci.org/public/org/jenkins-ci/main/jenkins-war/${JENKINS_VERSION}/jenkins-war-${JENKINS_VERSION}.war

# could use ADD but this one does not check Last-Modified header neither does it allow to control checksum 
# see https://github.com/docker/docker/issues/8331
RUN curl -fsSL ${JENKINS_URL} -o /usr/share/jenkins/jenkins.war \
  && echo "${JENKINS_SHA}  /usr/share/jenkins/jenkins.war" | sha256sum -c -


ENV JENKINS_UC https://updates.jenkins.io
RUN chown -R ${user} "$JENKINS_HOME" /usr/share/jenkins/ref

# for main web interface:
EXPOSE 8080

# will be used by attached slave agents:
EXPOSE 50000

ENV COPY_REFERENCE_FILE_LOG $JENKINS_HOME/copy_reference_file.log

USER root

COPY jenkins-support /usr/local/bin/jenkins-support
COPY jenkins.sh /usr/local/bin/jenkins.sh
RUN echo 2.0 > /usr/share/jenkins/ref/jenkins.install.UpgradeWizard.state
ENTRYPOINT ["/bin/tini", "--", "/usr/local/bin/jenkins.sh"]

# from a derived Dockerfile, can use `RUN plugins.sh active.txt` to setup /usr/share/jenkins/ref/plugins from a support bundle
COPY plugins.sh /usr/local/bin/plugins.sh
COPY install-plugins.sh /usr/local/bin/install-plugins.sh
RUN /usr/local/bin/install-plugins.sh workflow-aggregator:2.5 artifactory:2.12.1 swarm:2.1 parameterized-trigger:2.35.1 extended-choice-parameter:0.75 git:3.4.1 git-client:2.4.6 jenkins-multijob-plugin:1.24 nodelabelparameter:1.7.2

