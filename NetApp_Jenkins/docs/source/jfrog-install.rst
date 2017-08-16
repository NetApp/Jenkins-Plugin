.. NetApp Jenkins Plugin documentation master file, created by
   sphinx-quickstart on Fri Jul 21 10:21:20 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :titlesonly:
   :hidden:
   
.. _jfroginstall:


JFrog Artifactory
=================================================
   
   
.. _jfrogprerequisites:
   
Prerequisites
=================================================   
	* A host (VM/Physical-server/AWS) with any any flavour of linux.
	* `Docker Engine 1.12.5 <https://docs.docker.com/cs-engine/1.12/>`_
	* `NetAppDVP 1.13 <http://netappdvp.readthedocs.io/en/latest/install/index.html>`_.
	* `Docker Compose <https://docs.docker.com/compose/install/>`
 
.. _jfrogmain:
   
JFrog Artifactory on Docker
=================================================

	We recommend to install JFrog Artifactory via docker-compose from the following YAML file. :
	
	Use the following Compose file to install JFrog Artifactory:  
	
.. code-block:: yaml
   	
		# Version 2 without namespacing. Required env variables :
		# 
		# ART_LOGIN (optional, default=admin)
		# ART_PASSWORD (optional, default=password)
		#
		version: '2'
		services:
		  artifactory-node1:
		  image: jfrog-docker-reg2.bintray.io/jfrog/artifactory-ha-primary:5.1.4
		ports:
			- 8081:8081
			- 10017:10017
		volumes:
			- ~/data/artifactory/node1/etc:/var/opt/jfrog/artifactory/etc
			- artdata:/var/opt/jfrog/artifactory/data
			- ~/data/artifactory/node1/logs:/var/opt/jfrog/artifactory/logs
		environment:
			- DB_TYPE=mysql
			- DB_HOST=mysqldb
			- DB_PORT=3306
			- HA_IS_PRIMARY=true
			- HA_MEMBERSHIP_PORT=10017
			- DB_USER=artifactory
			- DB_PASSWORD=password
			- ART_LICENSES="<<YOUR_ARTIFACTORY_LICENSE>>"
		depends_on:
			- mysqldb
		restart: always
		artifactory-node2:
			image: jfrog-docker-reg2.bintray.io/jfrog/artifactory-ha-primary:5.1.4
		ports:
			- 8082:8081
			- 10018:10017
		volumes:
			- ~/data/artifactory/node2/etc:/var/opt/jfrog/artifactory/etc
			- artdata:/var/opt/jfrog/artifactory/data
			- ~/data/artifactory/node2/logs:/var/opt/jfrog/artifactory/logs
		environment:
			- DB_TYPE=mysql
			- ART_PRIMARY_BASE_URL=http://artifactory-node1:8081/artifactory
			- DB_HOST=mysqldb
			- DB_PORT=3306
			- HA_IS_PRIMARY=false
			- HA_MEMBERSHIP_PORT=10017
			- DB_USER=artifactory
			- DB_PASSWORD=password
			- ART_LICENSES="<<YOUR_ARTIFACTORY_LICENSE>>"
		depends_on:
			- artifactory-node1
			- mysqldb
		restart: always
		nginx:
			image: jfrog-docker-reg2.bintray.io/jfrog/nginx-art:5.1.4
		ports:
			- "80:80"
			- "443:443"
			- "5000-5010:5000-5010"
		environment:
			- ART_PRIMARY_BASE_URL=http://artifactory-node1:8081/artifactory
			#- ART_REVERSE_PROXY_METHOD=SUBDOMAIN
			#- ART_SERVER_NAME=mycluster.local
		mysqldb:
			image: registry.access.redhat.com/rhscl/mysql-57-rhel7:latest
		environment:
			- MYSQL_ROOT_PASSWORD=password
			- MYSQL_DATABASE=artdb
			- MYSQL_USER=artifactory
			- MYSQL_PASSWORD=password
		volumes:
			- mysqldata:/var/lib/mysql/data
		ports:
			#- "8145:8145"
			- "3306:3306"
		restart: always
    
		volumes:
			mysqldata:
				driver: netapp
				driver_opts:
				snapshotDir: "false"
			artdata:
				driver: netapp
				driver_opts:
			snapshotDir: "false"	


			
			
			
			
.. note:: 	1) Replace <<Artifactory License>>  with your actual Artifactory License.
			
			2) NetAppDVP should be running on your host before you execute the compose file.

			
	
	Save the above compose file on your linux host as docker-compose.yml and run it using following command ::
		
		>docker-compose up
		
	.. figure:: images/jfroghome.png
			:scale: 100 %
			:alt: Zip
		
	
	
Artifactory will be up and running at  ::

	http://<<HOST-IP:8081>>
	

.. note:: 	Artifactory starts with default username=admin and password=password	