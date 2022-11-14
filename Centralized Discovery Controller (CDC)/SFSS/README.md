# SFSS - SmartFabric Storage Software

SFSS enables the automated discovery of NVMe controllers that are available to each host within an NVMe IP-Based Storage Area Network (SAN).

SFSS provides:

1. A Centralized Discovery Controller (CDC) as defined in the NVM Express(TM) Technical Propoposal TP8010.
2. An mDNS responder as defined in NVM Express Technical Propoposal TP8009.
3. A GUI that supports the configuration of zoning and discovery parameters.

## Try it before you load it

If you're just looking for an overview of SFSS and see what it can do, Dell has provided
an [SFSS simulator](https://www.delltechnologies.com/en-us/product-demos/smartfabric-storage-software/index.htm?ref=DemoCenter__;!!NEt6yMaO-gk!WdfAXaGVUFFHMzL4v-Pj2BdinQaPpTkm1l6GZTc15AdXNgIWDPyAsi6FYuZEtJU$) that is available for you to experiment with.

## Docker

```bash
docker-compose up
```

## KVM

This is just a short version of the [Official documentation](https://www.dell.com/support/manuals/en-us/dell-emc-smartfabric-storage-software/sfss-120-user-guide/)

### Virtualization support

Make sure that VT-x/AMD-v support is enabled in BIOS

```bash
$ lscpu | grep -i virtualization
Virtualization:                  VT-x
```

and that kvm modules are loaded

```bash
$ lsmod | grep -i kvm
kvm_intel             217088  0
kvm                   614400  1 kvm_intel
irqbypass              16384  1 kvm
```

### Qemu installation

From <https://www.qemu.org/download/>

Installation on Fedora

```bash
sudo dnf install qemu-kvm wget
```

or on Ubuntu

```bash
sudo apt install qemu-system wget
```

or on SUSE

```bash
sudo zypper install qemu-kvm wget
```

### Download guest image

```bash
wget https://linux.dell.com/files/SANdbox/1.2.0/CDC-1.2.0.0028_2022_0719_0410.qcow2.zip
unzip CDC-1.2.0.0028_2022_0719_0410.qcow2.zip
```

### Run KVM with above image

```bash
qemu-kvm -cpu host -smp 2 -m 1G \
-drive file=CDC-1.2.0.0028_2022_0719_0410.qcow2,if=none,id=disk \
-device ide-hd,drive=disk,bootindex=0 \
--nographic
```

Login using admin/admin and change your defualt password
