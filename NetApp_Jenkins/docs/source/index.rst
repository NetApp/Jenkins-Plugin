.. NetApp Jenkins Plugin documentation master file, created by
   sphinx-quickstart on Fri Jul 21 10:21:20 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   


   
  
    

Welcome to NetApp-Jenkins-Plugin 2.0 documentation!
=======================================================

The NetApp-Jenkins integration is an end-to-end framework from creating code repository until zipping the successful builds in the artifactory location. All these processes run as Docker-containers and use persistent NetApp storage with NetApp Docker volume plugin (nDVP).

The advantage of running CI process on NetApp for Business or Asset owner are –
	1.	Improve Developer productivity
	
		 a.	NetApp FlexClones allows to cut down the user workspace provisioning from hours and days to few seconds.
		
		 b.	Each user workspace is pre-packaged with the source code and the dependencies like libraries, tools, compilers and config files for developers start working quickly. There are no long wait times for developers to prepare their workspaces.
		
	2.	Reduce build time
	
		 a.	NetApp Snapshots for the CI data volumes allows developers to run incremental builds over full builds. Full builds are time consuming.
		
		 b.	Incremental builds allow developers to test the changes quickly in their workspaces and provides consistency to the builds with reduced build times. 

	3.	Reduce infrastructure costs
	
		 a.	NetApp data volumes also known as FlexVols, Snapshots and FlexClones are thin provisioned. This allows to provision more build workloads with less storage footprint and optimize compute and network resources for parallel builds. Thus providing an improved Return of Investment (ROI) by doing “more with less” in the entire build farm.
		
		 b.	Data Compaction and De-duplication for the source code repositories and the software builds during the CI process on NetApp provides a high degree of storage space efficiency. Data compression of build artifacts in the binary repository lso provides space savings.

		 
Contents
=======================================================		 
.. toctree::
   :maxdepth: 2

   prerequisites
   support
	
   

	


   




