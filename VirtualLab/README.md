# Virtual Lab Overview and configuration files

This directory contains files and configuraion examples that will enable you to create an AWS based NVMe/TCP IP-Based SAN lab configuration similar to the following.

![AWSConfig](https://github.com/dell/SANdbox/blob/main/Documentation/Images/AWSConfig.png)

All EC2 instances (Host 1, SFSS and Storage) are running a standard AWS Ubuntu 20.04 image and are accessible from my Desktop at home via the "LAN" network.  You can control who can access your instance via the Security Group (SG) configuration.  In this case, I am using a custom SG "Public" that I created to allow everyone in my extended team to access the instance. 

In addition:

- The Host 1 EC2 instance has been configured to use - [nvme-stas](https://github.com/linux-nvme/nvme-stas) for NVMe/TCP discovery automation.
- The SFSS EC2 instance has had SFSS loaded onto it and can be discovered via mDNS from Host 1.
- The Storage EC2 instance has nvmet loaded onto it as well as the "Dell Endpoint Simulator".
