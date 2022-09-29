<#
Copyright 2022 Dell Inc. or its subsidiaries. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
#>
#Special thanks to JT at Dell.

Write-Output "Loading functions..."

function Get-SFSS-IPAddressManagement{
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSSApp/IpAddressManagements?$expand=IpAddressManagements"
    Write-Output "Getting SFSS Interfaces..."
    $response = Invoke-RestMethod -uri $uri -method Get -credential $cred -ContentType "application/json"
    return $response
}

function Edit-SFSS-IPAddressManagement{
    param(
        [string]$Interface,
        [string]$IPV4Address,
        [string]$IPV4Config,
        [int]$IPV4PrefixLength,
        #[string]$IPV4Gateway,
        [int]$MTU
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSSApp/IpAddressManagements("+$Interface+")"
    $IPV4Addresses = @($IPV4Address)
    $json = @{
        "IPV4Address" = $IPV4Addresses
        "IPV4Config" = $IPV4Config
        "IPV4PrefixLength" = $IPV4PrefixLength
        "IPV6Config" = "AUTOMATIC"
        "MTU" = $MTU
    }
    $json = $json | ConvertTo-Json
    $response = Invoke-RestMethod -uri $uri -method PUT -credential $cred -ContentType "application/json" -body $json
    return $response
}

function Add-SFSS-DDC {
    Param(
        [Parameter(Mandatory=$true)][int]$Instance,
		$TransportAddress
        #$PortId = 8009
        #$TransportAddressFamily,
        #[boolean]$Activate,
        )


    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/"+ $Instance + "/DDCs"
    $json = @{
        "TransportAddress" = $TransportAddress
        "TransportAddressFamily" = "IPV4"
        "PortId" = 8009
        "TransportType" = "TCP"
        "Activate" = $true
    }

    Write-Output "Running pull registration of a SFSS Subsystem..."
    $json = $json | ConvertTo-Json
    $Headers = @{'Accept'='application/json'}
    $response = Invoke-RestMethod -uri $uri -method Post -credential $cred -ContentType "application/json" -Headers $Headers -body $json

    return $response
}

function Get-SFSS-DDC {
    param(
    [Parameter(Mandatory=$true)][int]$Instance
    )

    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance +"/DDCs"
    Write-Output "Getting SFSS DDCs now..."
    $response = Invoke-RestMethod -uri $uri -method Get -credential $cred -ContentType "application/json"

    return $response
}

function Remove-SFSS-DDC {
	[CmdletBinding(SupportsShouldProcess)]
    param (
        [Parameter(Mandatory=$true)][int]$Instance,
        $DDC
    )

    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/DDCs(""" + $DDC + """)"
    $response = Invoke-RestMethod -uri $uri -method Delete -credential $cred -ContentType "application/json"
    if ($PSCmdlet.ShouldProcess('$DDC')){
        Write-Output "Removing DDC $($DDC) from Instance $($Instance)"
    }
    return $response
}

function Get-SFSS-SubSystem {
    param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/"+ $Instance + "/Subsystems?" + '$expand=Subsystems'
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Get-SFSS-Instances {
    param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSSApp/CDCInstanceManagers('$Instance')"
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Add-SFSS-Instances {
    param(
        $InstanceIdentifier,
        $Interfaces
    )
    $Interfaces = @($Interfaces)
    $json = @{
        "InstanceIdentifier" = $InstanceIdentifier
        "Interfaces" = $Interfaces
        "CDCAdminState" = "Enable"
        "DiscoverySvcAdminState" = "Enable"
    }
    $json = $json | ConvertTo-Json
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSSApp/CDCInstanceManagers('$InstanceIdentifier')"
    $response = Invoke-RestMethod -Uri $uri -Method PUT -Credential $cred -ContentType "application/json" -Body $json
    
	return $response
}

function Get-SFSS-FoundationalConfigs{
    param(
    #[Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSSApp/FoundationalConfigs?" + '$expand=FoundationalConfigs'

    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Get-SFSS-Hosts {
     param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/Hosts?" + '$expand=Hosts'
    #Write-Output $uri
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Get-SFSS-ZoneDB {
    param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/ZoneDBs"
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Get-SFSS-ZoneDB-ConfigDB {
    param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/ZoneDBs('config')?" + '$source=config'
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Get-SFSS-ZoneDB-ActiveDB {
    param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/"+ $Instance + "/ZoneDBs('active')?"
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Request-ZoneDB-Activate{
    param (
        $ZoneGroup,
        [Parameter(Mandatory=$true)][int]$Instance
    )
    Write-Output "Activating ZoneDB" $ZoneGroup -ForegroundColor Yellow
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/ZoneDBs('config')/ZoneGroups('" + $ZoneGroup + "')"

    $json = @{
        "ActivateStatus" = "Activate"
    }
    $json = $json | ConvertTo-Json
    $response = Invoke-RestMethod -Uri $uri -Method PUT -Credential $cred -ContentType "application/json" -body $json

    return $response
}

function Request-ZoneDB-Deactivate{
    param (
        [Parameter(Mandatory=$true)][int]$Instance
    )
    $ZoneGroup = Get-SFSS-ZoneDB-ActiveDB
    $ZoneGroup = $ZoneGroup.ZoneGroups
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/"+ $Instance + "/ZoneDBs('active')/ZoneGroups('" + $ZoneGroup + "')"

    $json = @{
        "ActivateStatus" = "DeActivate"
    }
    $json = $json | ConvertTo-Json
    $response = Invoke-RestMethod -Uri $uri -Method PUT -Credential $cred -ContentType "application/json" -body $json

    return $response
}

function Get-SFSS-ZoneGroup {
    param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/ZoneDBs('config')?" + '$source' + "=config"
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Add-SFSS-ZoneGroup {
 Param(
        $ZoneGroupName,
        [Parameter(Mandatory=$true)][int]$Instance
    )
    Write-Output "Creating ZoneGroup named" $ZoneGroupName -ForegroundColor Yellow
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/"+ $Instance + "/ZoneDBs('config')/ZoneGroups"

    $json = @{
        "ZoneDBType" = "config"
        "ZoneGroupName" = $ZoneGroupName
    }

    $json = $json | ConvertTo-Json
    $response = Invoke-RestMethod -uri $uri -method Post -credential $cred -ContentType "application/json" -Headers $Headers -body $json

    return $response
}

function Remove-SFSS-ZoneGroup {
	[CmdletBinding(SupportsShouldProcess)]
    param(
        $ZoneGroupName,
        [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/ZoneDBs('config')/ZoneGroups" + $ZoneGroupName
    $response = Invoke-RestMethod -Uri $uri -Method Delete -Credential $cred -ContentType "application/json"
    if ($PSCmdlet.ShouldProcess('$ZoneGroupName')){
        Write-Output "Removing ZoneGroup $($ZoneGroupName) from Instance $($Instance)"
    }
	return $response
}

function Get-SFSS-Zones {
    param (
        #$zonename,
        [Parameter(Mandatory=$true)][int]$Instance
    )

    $ZoneGroup = (Get-SFSS-ZoneGroup -Instance $Instance).ZoneGroups
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" +$Instance+ "/ZoneDBs('config')/ZoneGroups(" + $ZoneGroup + ")/Zones?" + '$source' + "=config" + '&$expand=Zones'
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Add-SFSS-Zone {
    param(
        $ZoneName,
        [Parameter(Mandatory=$true)][int]$Instance
    )
    Write-Output "Creating Zone named" $ZoneName -ForegroundColor Yellow

    $ZoneGroup = (Get-SFSS-ZoneGroup -Instance $Instance).ZoneGroups
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/"+ $Instance+ "/ZoneDBs('config')/ZoneGroups(" + $ZoneGroup + ")/Zones"

    $json = @{
        "ZoneName" = $ZoneName
    }
    $json = $json | ConvertTo-Json
    $response = Invoke-RestMethod -uri $uri -method Post -credential $cred -ContentType "application/json" -Headers $Headers -body $json

    return $response
}

function Remove-SFSS-Zone {
    [CmdletBinding(SupportsShouldProcess)]
	param (
        $zonename,
        [Parameter(Mandatory=$true)][int]$Instance
        )
    $ZoneGroup = (Get-SFSS-ZoneGroup).ZoneGroups
    $Zones = Get-SFSS-Zones
    $ZoneToDelete = $Zones.Zones | Where-Object {$_.ZoneName -eq $zonename}
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/ZoneDBs('config')/ZoneGroups(" + $ZoneGroup + ")/Zones('" + $ZoneToDelete.ZoneId + "')"
    $response = Invoke-RestMethod -uri $uri -method DELETE -credential $cred -ContentType "application/json" -Headers $Headers
    if ($PSCmdlet.ShouldProcess('$zonename')){
        Write-Output "Removing Zonename $($zonename) from ZoneGroup $($ZoneGroup) on Instance $($Instance)"
    }
    return $response
}

function Add-SFSS-ZoneMember{
    param (
        $zonename,
        $member,
        $role,
        [Parameter(Mandatory=$true)][int]$Instance
        )
    Write-Output "Adding member" $member "To Zone: " $zonename -ForegroundColor Yellow
    $ZoneGroup = (Get-SFSS-ZoneGroup -Instance $Instance).ZoneGroups

    $Zones = Get-SFSS-Zones -Instance $Instance
    $Zone = ($Zones.Zones | Where-Object {$_.ZoneName -eq $zonename}) | Select-Object ZoneId

    $json = @{
        "ZoneMemberId" = $member
        "ZoneMemberType" = "FullQualifiedName"
        "Role" = "$role"
    }

    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/ZoneDBs('config')/ZoneGroups('" + $ZoneGroup + "')/Zones" + "('" + $Zone.ZoneId + "')/ZoneMembers"
    $json = $json | ConvertTo-Json
    $response = Invoke-RestMethod -uri $uri -method Post -credential $cred -ContentType "application/json" -Headers $Headers -body $json

    return $response
}

function Get-SFSS-ZoneDB-ConfigDB-ZoneGroup {
    param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/"+ $Instance +"/ZoneDBs('config')/ZoneGroups?$source=config"
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function Get-SFSS-ZoneDB-ActiveDB {
     param(
    [Parameter(Mandatory=$true)][int]$Instance
    )
    $uri = "https://" + $SFSSIP + "/redfish/v1/SFSS/" + $Instance + "/ZoneDBs('active')"
    $response = Invoke-RestMethod -Uri $uri -Method Get -Credential $cred -ContentType "application/json"
    
	return $response
}

function ZoneA
{
#Create ZoneGroup NetworkA
Add-SFSS-ZoneGroup -ZoneGroupName ZG-VLAN100 -Instance 1


 #Get Hosts
 $InitiatorHosts = Get-SFSS-Hosts -Instance 1

 #Create Zones foreach Host
 $InitiatorHosts = $InitiatorHosts.Hosts
 foreach ($InitiatorHost in $InitiatorHosts)
 {
    $Zonename = $InitiatorHost.TransportAddress
    #$zone = Add-SFSS-Zone -ZoneName $Zonename -Instance 1
	Add-SFSS-Zone -ZoneName $Zonename -Instance 1

    #$NQN = $InitiatorHost.NQN
    $Id = $InitiatorHost.Id
    #$addmember = Add-SFSS-ZoneMember -zonename $Zonename -member $Id -role Host -Instance 1
	Add-SFSS-ZoneMember -zonename $Zonename -member $Id -role Host -Instance 1


     #Get Subsystems
     $Subsystems = Get-SFSS-SubSystem -Instance 1

     #Foreach Subsystem, Add subsystem NQN to the Host Zone
     $Subsystems = $Subsystems.Subsystems
     foreach ($Subsystem in $Subsystems)
     {

        #$NQN = $Subsystem.NQN
        $Id = $Subsystem.Id
        #$addmember = Add-SFSS-ZoneMember -zonename $Zonename -member $Id -role Subsystem -Instance 1
		Add-SFSS-ZoneMember -zonename $Zonename -member $Id -role Subsystem -Instance 1

     }
 }




#Activate the Zoneset
$ZoneGroup = Get-SFSS-ZoneDB-ConfigDB -Instance 1
$ZoneGroup = $ZoneGroup.ZoneGroups

#$activatezoneset = Request-ZoneDB-Activate -ZoneGroup $ZoneGroup -Instance 1
Request-ZoneDB-Activate -ZoneGroup $ZoneGroup -Instance 1
}

function ZoneB
{
#Create ZoneGroup NetworkA
Add-SFSS-ZoneGroup -ZoneGroupName ZG-VLAN200 -Instance 2


 #Get Hosts
 $InitiatorHosts = Get-SFSS-Hosts -Instance 2

 #Create Zones foreach Host
 $InitiatorHosts = $InitiatorHosts.Hosts
 foreach ($InitiatorHost in $InitiatorHosts)
 {
    $Zonename = $InitiatorHost.TransportAddress
    #$zone = Add-SFSS-Zone -ZoneName $Zonename -Instance 2
	Add-SFSS-Zone -ZoneName $Zonename -Instance 2

    #$NQN = $InitiatorHost.NQN
    $Id = $InitiatorHost.Id
    #$addmember = Add-SFSS-ZoneMember -zonename $Zonename -member $Id -role Host -Instance 2
	Add-SFSS-ZoneMember -zonename $Zonename -member $Id -role Host -Instance 2


     #Get Subsystems
     $Subsystems = Get-SFSS-SubSystem -Instance 2

     #Foreach Subsystem, Add subsystem NQN to the Host Zone
     $Subsystems = $Subsystems.Subsystems
     foreach ($Subsystem in $Subsystems)
     {

        #$NQN = $Subsystem.NQN
        $Id = $Subsystem.Id
        #$addmember = Add-SFSS-ZoneMember -zonename $Zonename -member $Id -role Subsystem -Instance 2
		Add-SFSS-ZoneMember -zonename $Zonename -member $Id -role Subsystem -Instance 2

     }
 }




#Activate the Zoneset
$ZoneGroup = Get-SFSS-ZoneDB-ConfigDB -Instance 2
$ZoneGroup = $ZoneGroup.ZoneGroups

#$activatezoneset = Request-ZoneDB-Activate -ZoneGroup $ZoneGroup -Instance 2
Request-ZoneDB-Activate -ZoneGroup $ZoneGroup -Instance 2
}

#######VARIABLES############

#SFSS MgmtIP
#$SFSSIP = "w.x.y.z"

#SFSS User/Pass
#$SFSSusername = "admin"
#$SFSSpassword = "adminpass"

#$secpasswd = ConvertTo-SecureString $SFSSpassword -AsPlainText -Force
#$cred = New-Object System.Management.Automation.PSCredential ($SFSSusername, $secpasswd)

add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy

#######MAIN FUNCTION############

#Run Zoning Functions
#ZoneA
#ZoneB
