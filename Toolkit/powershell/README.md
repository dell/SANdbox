## PowerShell related examples and functions
This Directory contains PowerShell related information and provides example scripts that can be used to manage your NVMe IP-Based SAN infrastructure.

Before you begin, ensure you have the correct prerequisites installed and/or configured on your system, this inclucdes:
- Admin level privileges for the system where PowerShell and PowerCLI will be installed. 

     **NOTE:** While not strictly necessary, having Local Admin rights for your system will reduce your frustration and therefore make the world a nicer place. If getting access to admin rights is not possible, or you don't really care about making the world a nicer place, you can always use the `-Scope CurrentUser` parameter (don't worry, you'll be repeatedly prompted when and where this is necessary) Oh! And if you forgot to use the `-Scope CurrentUser` parameter when using the `Install-Module VMware.PowerCLI` command (Again, don't worry, you'll know when it happens), you'll probably need use the `AllowClobber` option when you run it AGAIN! Here's the command to save you a bit of work `Install-Module VMware.PowerCLI -Scope CurrentUser`

     **NOTE:** If you receive an error message containing the string "running scripts is disabled on this system"... CONGRATULATIONS! Me too... Try using the `Set-ExecutionPolicy Bypass` command. 
- PowerShell - Version 5.1 was used to validate the following functions APPEARED to be working correctly. You can check the version by using the `$PSVersionTable` 
command from within the PowerShell instance running on your system.
- PowerCLI - (Optional: Only Required if the PowerShell script will be interacting with vCenter) Version 12.5 was used to validate the functions that interact with vCenter and APPEARED to be working correctly. You can check the version by using the `Get-PowerCLIversion` command from within the PowerShell instance running on your system.
- vCenter - (Optional: Only Required when running scripts that interact with vCenter such as setupLocalLab.ps1) 
- One or more PowerShell or PowerCLI functions.  You are free to use the ones provided in this directory (no warranty expressed or implied, YMMV) or write your own...that's the beauty of a developer enablement portal!

### A REALLY simple way to verify that PowerShell is configured correctly:
1. From Powershell, cd to the directory that contains the `BasicSANdboxFunctions.ps1` PowerShell script:

    `PS > cd C:\work\scripts\`

2. Modify the parameters in the VARIABLES section of the `BasicSANdboxFunctions.ps1` PowerShell script to match the specifics of your environment:

    `$SFSSIP = "Your SFSS IP ADDRESS"`
    
    `$SFSSusername = "A valid username for your SFSS instance"`
    
    `$SFSSpassword = "The password associated with the username provided above"`
    
3. Source the `BasicSANdboxFunctions.ps1` PowerShell script to import the functions and variables defined within:

    `PS > . .\BasicSANdboxFunctions.ps1`

4. Establish a session with the SFSS instance by running `Get-SFSS-IPAddressManagement`

    `PS > Get-SFSS-IPAddressManagement`

Something like the following output will be shown:
    Getting SFSS Interfaces...


    IpAddressManagements             : {@{@odata.id=/redfish/v1/SFSSApp/IpAddressManagements('eth1')},
                                   @{@odata.id=/redfish/v1/SFSSApp/IpAddressManagements('eth0')}}
    IpAddressManagements@odata.count : 2
    @odata.id                        : /redfish/v1/SFSSApp/IpAddressManagements?=IpAddressManagements
    @odata.context                   : /redfish/v1/SFSSApp/$metadata#IpAddressManagements
    @odata.type                      : #IpAddressManagementsCollection.IpAddressManagementsCollection

### A REALLY simple way to verify if PowerShell AND PowerCLI are configured correctly:
1. Connect to your vCenter instance using the `Connect-VIServer <VIserver FQDN or IP Address>`, for example `Connect-VIServer 10.10.10.42`
     **NOTE:** If you get a error about unknown or invalid certificates you COULD use the 
`Set-PowerCLIConfiguration -Scope User -InvalidCertificateAction warn` command but please take note, `-Scope` is set to User not CurrentUser.
2. Proivde the vCenter credentials when prompted.
3. Get a list of VMs from vCenter using the `Get-VM | Select-Object Name,NumCPU,MemoryMB,PowerState,Host | Export-CSV VMs.csv -NoTypeInformation`
     **NOTE:** If you don't have local admin rights, this command will probably fail with `about attempting to access c:\WINDOWS\system32\vms.cs` as a result you'll need to use
something like `Get-VM | Select-Object Name,NumCPU,MemoryMB,PowerState,Host | Export-CSV C:\Users\iiiiitsJonny\PowerCLIOutput\VMs.csv -NoTypeInformation` 
4. If you get a list of VMs, congratulations! You are now ready to use the scripts in this directory.

# How to use the scripts in this directory?
The following examples should not be performed in a production environment. They are being provided for example purposes only.

### To create a zone that contains all Hosts and Subsystem interfaces in CDC instance 1
1. From Powershell, cd to the directory that contains the `BasicSANdboxFunctions.ps1` PowerShell script:

    `PS > cd C:\work\scripts\`

2. Modify the parameters in the VARIABLES section of the `BasicSANdboxFunctions.ps1` PowerShell script to match the specifics of your environment:

    `$SFSSIP = "Your SFSS IP ADDRESS"`
    
    `$SFSSusername = "A valid username for your SFSS instance"`
    
    `$SFSSpassword = "The password associated with the username provided above"`
    
3. Source the `BasicSANdboxFunctions.ps1` PowerShell script to import the functions and variables defined within:

    `PS > . .\BasicSANdboxFunctions.ps1`

4. Establish a session with the SFSS instance by running `Get-SFSS-IPAddressManagement`

    `PS > Get-SFSS-IPAddressManagement`

5. Create the zone, zonegroup and activate the zonegroup:

    `PS > ZoneA`
