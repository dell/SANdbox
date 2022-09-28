## SANdbox

[![Linters](https://github.com/dell/SANdbox/actions/workflows/linters.yml/badge.svg)](https://github.com/dell/SANdbox/actions/workflows/linters.yml)
[![License](https://img.shields.io/github/license/dell/SANdbox?style=flat-square&color=blue&label=License)](https://github.com/dell/SANdbox/blob/master/LICENSE)
[![Last Release](https://img.shields.io/github/v/release/dell/SANdbox?label=Latest&style=flat-square&logo=go)](https://github.com/dell/SANdbox/releases)

SANdbox is a developer enablement portal that provides documentation and tools that will help automate the deployment and management of NVMe(TM) IP-Based SANs (Storage Area Networks). An NVMe IP-Based SAN typically consists of Hosts, NVM Subsystems and one or more network switches that provide IP connectivity.

![IP SAN Diagram](https://github.com/dell/SANdbox/blob/main/Documentation/Images/SimpleIPSAN.png)

As the number of endpoints used begin to scale up (e.g., more than 32 end devices), a traditional NVMe IP-Based SAN can become difficult to manage. More information about this scalability problem can be found here ![NVMe-oF: Discovery Automation for NVMe IP-Based SANs](https://www.youtube.com/watch?v=uzeK_g-1Pxw)  

To address this scalability challenge, several companies have collaborated on the concept of a Centralized Discovery Controller (CDC) to allow administrators to deploy NVMe/TCP at scale. This is accomplished by providing a Centralized Discovery Service for NVMe/TCP Endpoints that facilitates endpoint discovery, registration, soft zoning, and event notification.

![IP SAN Diagram](https://github.com/dell/SANdbox/blob/main/Documentation/Images/DetailedIPSAN.png)

SANdbox provides documentation, tools and helpful resources that will enable you to programatically interact with IP SANs.  Before you begin, please take a moment to review the following information.

Additional information about Centralized Discovery Controllers (for example Dell's SFSS) and the NVMe/TCP ecosystem can be found below:
- [The Future of Software-defined Networking for Storage Connectivity](https://www.delltechnologies.com/en-us/blog/the-future-of-software-defined-networking-for-storage-connectivity/)
- [NVMe-oF Looking beyond performance hero numbers](https://www.youtube.com/watch?v=F6nifK_Rkxw__;!!NEt6yMaO-gk!WdfAXaGVUFFHMzL4v-Pj2BdinQaPpTkm1l6GZTc15AdXNgIWDPyAsi6FVftH7iA$)
- [SNIA NSF – Discovery Automation for NVMe IP-Based SANs](https://www.youtube.com/watch?v=uzeK_g-1Pxw__;!!NEt6yMaO-gk!WdfAXaGVUFFHMzL4v-Pj2BdinQaPpTkm1l6GZTc15AdXNgIWDPyAsi6F4G96ptU$)
- [SNIA SDC – Discovery Protocol deep dive](https://www.youtube.com/watch?v=Oqb3s0llNxw__;!!NEt6yMaO-gk!WdfAXaGVUFFHMzL4v-Pj2BdinQaPpTkm1l6GZTc15AdXNgIWDPyAsi6FeqdFbxU$)
- [Nvme-stas (Dell maintained open source discovery client for Linux)](https://github.com/linux-nvme/nvme-stas) 
