"""
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
"""
# Authors: Martin Belanger <Martin.Belanger@dell.com>

import json
import ipaddress
import requests


class RestApi:
    def __init__(self, ip_addr: str, username: str, password: str):
        self._url = f'https://{ip_addr}/redfish/v1'
        self._creds = (username, password)
        # self._creds = requests.auth.HTTPDigestAuth(username, password)
        # self._creds = requests.auth.HTTPBasicAuth(username, password)

        # Define minimum headers contents (headers parameter will contain this data as a minimum)
        self._headers = {
            'Content-Type': 'application/json',
        }

    def __uri__(self, oid: str):
        '''Combine the URL and OID to form the URI needed to access the SFSS REST API'''
        return f'{self._url}{"" if oid[0] == "/" else "/"}{oid}'

    def __hdrs__(self, headers: dict):
        '''Build the 'headers' parameter needed to make REST API requests'''
        if headers is not None:
            headers.update(self._headers)
        else:
            headers = self._headers
        return headers

    def _get(self, oid: str, headers=None):
        '''
        Issue a REST API GET requests
        @return: A requests.Response object'''
        reply = requests.get(
            self.__uri__(oid),
            auth=self._creds,
            headers=self.__hdrs__(headers),
            verify=False,
        )
        return reply

    def _put(self, oid: str, json_data: dict, headers=None):
        '''
        Issue a REST API PUT requests
        @return: A requests.Response object'''
        reply = requests.put(
            self.__uri__(oid),
            auth=self._creds,
            headers=self.__hdrs__(headers),
            data=json.dumps(json_data),
            verify=False,
        )
        return reply

    def _post(self, oid: str, json_data: dict, headers=None):
        '''
        Issue a REST API POST requests
        @return: A requests.Response object'''
        reply = requests.post(
            self.__uri__(oid),
            auth=self._creds,
            headers=self.__hdrs__(headers),
            data=json.dumps(json_data),
            verify=False,
        )
        return reply

    def _delete(self, oid: str, headers=None):
        '''
        Issue a REST API DELETE requests
        @return: A requests.Response object'''
        reply = requests.delete(
            self.__uri__(oid),
            auth=self._creds,
            headers=self.__hdrs__(headers),
            verify=False,
        )
        return reply

    def _get_list(self, oid: str, key: str):
        '''
        Issue a REST API GET requests expecting a list as the returned data.
        @return: Requested list on success, empty list otherwise.'''
        reply = self._get(oid)
        if not reply.ok:
            return []

        return reply.json().get(key, [])

    # **************************************************************************
    def get_ip_address_management(self):
        '''@return: IP Management list on success, empty list otherwise.'''
        oid = 'SFSSApp/IpAddressManagements?$expand=IpAddressManagements'
        return self._get_list(oid, 'IpAddressManagements')

    def edit_ipv4_address_management(self, iface: str, addr: str, cfg: str, gw: str, plen: int, mtu: int):
        '''@return:'''
        json_data = {
            'IPV4Address': addr,
            'IPV4Config': cfg,
            'IPV4Gateway': gw,
            'IPV4PrefixLength': plen,
            'MTU': mtu,
        }
        oid = f'SFSSApp/IpAddressManagements({iface})'
        reply = self._put(oid, json_data)
        return reply.json() if reply.ok else {}

    def get_foundational_configs(self):
        '''@return: List of Foundational Configs on success, empty list otherwise'''
        oid = 'SFSSApp/FoundationalConfigs?$expand=FoundationalConfigs'
        return self._get_list(oid, 'FoundationalConfigs')

    def get_cdc_instances(self):
        '''
        Get the list of CDC instances
        @return: List of instance dicts on success, Empty list otherwise
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_cdc_instances()
           print(f'>>> {r}')
           >>> [{'CDCAdminState': 'Enable',
                 'DiscoverySvcAdminState': 'Enable',
                 'InstanceIdentifier': '1',
                 'Interfaces': ['ens160'],
                 '@odata.id': "/redfish/v1/SFSSApp/CDCInstanceManagers('1')",
                 '@odata.type': '#CDCInstanceManagers.CDCInstanceManagers',
                 '@odata.context': '/redfish/v1/SFSSApp/$metadata#CDCInstanceManagers/CDCInstanceManagers/$entity'}]
        '''
        oid = f"SFSSApp/CDCInstanceManagers?$source=config&$expand=CDCInstanceManagers"
        return self._get_list(oid, 'CDCInstanceManagers')

    def get_cdc_instance(self, instance: int):
        '''
        Get a CDC instance
        @return: The CDC instance as a dict on success, Empty dict otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_cdc_instance(1)
           print(f'>>> {r}')
           >>> {'CDCAdminState': 'Enable',
                'DiscoverySvcAdminState': 'Enable',
                'InstanceIdentifier': '1',
                'Interfaces': ['ens160'],
                '@odata.id': "/redfish/v1/SFSSApp/CDCInstanceManagers('1')",
                '@odata.type': '#CDCInstanceManagers.CDCInstanceManagers',
                '@odata.context': '/redfish/v1/SFSSApp/$metadata#CDCInstanceManagers/CDCInstanceManagers/$entity'}
        '''
        oid = f"SFSSApp/CDCInstanceManagers('{instance}')"
        reply = self._get(oid)
        return reply.json() if reply.ok else {}

    def create_cdc_instance(self, instance: int, interfaces: str):
        '''@return:'''
        json_data = {
            'InstanceIdentifier': instance,
            'Interfaces': interfaces,
            'CDCAdminState': 'Enable',
            'DiscoverySvcAdminState': 'Enable',
        }
        oid = f"SFSSApp/CDCInstanceManagers('{instance}')"
        reply = self._put(oid, json_data)
        return reply.json() if reply.ok else {}

    def pull_register_ddc(self, instance: int, trtype: str, traddr: str, trsvcid: int, activate: bool):
        '''@return:'''
        ip = ipaddress.ip_address(traddr)
        json_data = {
            'TransportType': trtype,
            'TransportAddress': traddr,
            'PortId': trsvcid,
            'TransportAddressFamily': f'IPV{ip.version}',
            'Activate': activate,
        }
        oid = f'SFSS/{instance}/DDCs'
        reply = self._post(oid, json_data, {'Accept': 'application/json'})
        return reply.json() if reply.ok else {}

    def get_hosts(self, instance: int):
        '''
        Get the list of hosts
        @return: List of hosts dicts on success, Empty list otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_hosts(1)
           print(f'>>> {r}')
           >>> [{'TransportType': 'TCP',
                 'HostInterface': 'nqn.2014-08.org.nvmexpress:uuid:83294d56-1ebf-a154-d613-a7cb28c6ef39@100.94.69.50:V4::0:39770:TCP',
                 'NQN': 'nqn.2014-08.org.nvmexpress:uuid:83294d56-1ebf-a154-d613-a7cb28c6ef39',
                 'TransportAddress': '100.94.69.50',
                 'TREQ': 'Secure channel Not specified',
                 'EKType': 'TRADDR',
                 'ConnectionStatus': 'Online',
                 'NodeName': 'stfs-cdcproxy-deployment-1-0',
                 'RegistrationType': 'Explicit',
                 'EVersion': 'Linux 5.17.0-rc2-stas-150400.1-default+ SLES 15.4',
                 'TSAS': 'No Security',
                 'HostIdentifier': '83294d561ebfa154d613a7cb28c6ef39',
                 'TransportAddressFamily': 'IPV4',
                 'Id': 'nqn.2014-08.org.nvmexpress:uuid:83294d56-1ebf-a154-d613-a7cb28c6ef39@100.94.69.50:V4::0:0:TCP',
                 'EName': 'sles15sp4',
                 '@odata.id': "/redfish/v1/SFSS/1/Hosts('nqn.2014-08.org.nvmexpress:uuid:83294d56-1ebf-a154-d613-a7cb28c6ef39@100.94.69.50:V4::0:0:TCP')",
                 '@odata.type': '#Hosts.Hosts',
                 '@odata.context': '/redfish/v1/SFSS/1/$metadata#Hosts/Hosts/$entity'},
           ]
        '''
        oid = f'SFSS/{instance}/Hosts?$expand=Hosts'
        return self._get_list(oid, 'Hosts')

    def get_ddcs(self, instance: int):
        '''@return: List of DDCs on success, empty list otherwise.'''
        oid = f'SFSS/{instance}/DDCs'
        return self._get_list(oid, 'DDCs')

    def delete_ddc(self, instance: int, ddc_id: str):
        '''@return:'''
        oid = f'SFSS/{instance}/DDCs({ddc_id})'
        reply = self._delete(oid, {'Accept': 'application/json'})
        return reply.ok

    def get_subsystems(self, instance: int):
        '''@return: List of subsystems on success, empty list otherwise.'''
        oid = f'SFSS/{instance}/Subsystems?$expand=Subsystems'
        return self._get_list(oid, 'Subsystems')

    # **************************************************************************
    def get_zonedbs(self, instance: int):
        '''
        Get the list of zone DBs.
        @return: List of zone DBs on success, empty list otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_zonedbs(1)
           print(f'>>> {r}')
           >>> ["/redfish/v1/SFSS/1/ZoneDBs('pending')",
                "/redfish/v1/SFSS/1/ZoneDBs('active')"]
        '''
        oid = f'SFSS/{instance}/ZoneDBs'
        items = self._get_list(oid, 'ZoneDBs')
        return [item['@odata.id'] for item in items]

    def get_config_zonedbs(self, instance: int):
        '''
        Get the 'config' DB.
        @return: The config DB as a dict.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_config_zonedbs(1)
           print(f'>>> {r}')
           >>> {'NumberZoneGroups': 2,
                'ZoneGroups': ['config:Klingons:nqn.1988-11.com.dell:SFSS:1:20220523215843e8',
                'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8'],
                '@odata.id': "/redfish/v1/SFSS/1/ZoneDBs('config')",
                '@odata.type': '#ZoneDBs.ZoneDBs',
                '@odata.context': '/redfish/v1/SFSS/1/$metadata#ZoneDBs/ZoneDBs/$entity'}
        '''
        oid = f"SFSS/{instance}/ZoneDBs('config')?$source=config"
        reply = self._get(oid)
        return reply.json() if reply.ok else {}

    def get_active_zonedbs(self, instance: int):
        '''
        Get the 'active' DB.
        @return: The active DB as a dict.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_active_zonedbs(1)
           print(f'>>> {r}')
           >>> {'NumberZoneGroups': 1,
                'ZoneGroups': ['active:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8'],
                '@odata.id': "/redfish/v1/SFSS/1/ZoneDBs('active')",
                '@odata.type': '#ZoneDBs.ZoneDBs',
                '@odata.context': '/redfish/v1/SFSS/1/$metadata#ZoneDBs/ZoneDBs/$entity'}
        '''
        oid = f"SFSS/{instance}/ZoneDBs('active')?"
        reply = self._get(oid)
        return reply.json() if reply.ok else {}

    # **************************************************************************
    def get_zone_group_ids(self, instance: int):
        '''
        Get the list of Zone Groups.
        @return: List of zone group IDs on success, Empty list otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_active_zonedbs(1)
           print(f'>>> {r}')
           >>> ['config:Klingons:nqn.1988-11.com.dell:SFSS:1:20220523215843e8',
                'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8']
        '''
        oid = f"SFSS/{instance}/ZoneDBs('config')?$source=config"
        return self._get_list(oid, 'ZoneGroups')

    def get_zone_group_id(self, instance: int, zone_group_name: str):
        '''
        Get Zone Group by name.
        @return: Zone group ID as a str on success, None otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_zone_group_id(1, 'Starfleet')
           print(f'>>> {r}')
           >>> config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8
        '''
        for zone_group_id in self.get_zone_group_ids(instance):
            if zone_group_name == zone_group_id.split(':')[1]:
                return zone_group_id
        return None

    def create_zone_group(self, instance: int, zone_group_name: str):
        '''
        Create a zone group
        @return: The zone group ID as a str on success, None otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.create_zone_group(1, 'Romulans')
           print(f'>>> {r}')
           >>> config:Romulans:nqn.1988-11.com.dell:SFSS:1:20220523215843e8
        '''
        json_data = {
            'ZoneDBType': 'config',
            'ZoneGroupName': zone_group_name,
        }
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups"
        reply = self._post(oid, json_data, {'Accept': 'application/json'})
        return reply.json().get('EId') if reply.ok else None

    def delete_zone_group(self, instance: int, zone_group_id: str):
        '''
        Create a zone group
        @return: True on success, False otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.delete_zone_group(1, 'config:Romulans:nqn.1988-11.com.dell:SFSS:1:20220523215843e8')
           print(f'>>> {r}')
           >>> True
        '''
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group_id})?$source=config&$expand=ZoneGroups"
        reply = self._delete(oid)
        return reply.ok

    def activate_zone_group(self, instance: int, zone_group_id: str):
        '''
        Activate a zone group
        @return: True on success, False otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.activate_zone_group(1, 'config:Romulans:nqn.1988-11.com.dell:SFSS:1:20220523215843e8')
           print(f'>>> {r}')
           >>> True
        '''
        json_data = {
            'ActivateStatus': 'Activate',
        }
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups('{zone_group_id}')"
        reply = self._put(oid, json_data)
        return reply.ok

    def deactivate_zone_group(self, instance: int, zone_group_id: str):
        '''
        Deactivate a zone group
        @return: True on success, False otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.deactivate_zone_group(1, 'config:Romulans:nqn.1988-11.com.dell:SFSS:1:20220523215843e8')
           print(f'>>> {r}')
           >>> True
        '''
        json_data = {
            'ActivateStatus': 'DeActivate',
        }
        oid = f"SFSS/{instance}/ZoneDBs('active')/ZoneGroups('{zone_group_id}')"
        reply = self._put(oid, json_data)
        return reply.ok

    # **************************************************************************
    def get_zones(self, instance: int, zone_group_id: str):
        '''
        Get all the zones in specified zone group.

        @return: List of zone dicts on success, Empty list otherwise.

        Example of a zone dict:
        {
            'ZoneName': str,
            'ZoneId': str,
            'numberZoneMembers': str,  # string representatin of an int
            '@odata.id': str,
            '@odata.type': str,
            '@odata.context': str
        }
        '''
        if zone_group_id is None:
            return []
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group_id})/Zones?$source=config&$expand=Zones"
        return self._get_list(oid, 'Zones')

    def get_zone(self, instance: int, zone_group_id: str, zone_name: str):
        '''
        Get zone by name.
        @return: The zone dict on success, None otherwise
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_zone_id(1, 'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8', 'enterprise')
           print(f'>>> {r}')
           >>> {'ZoneName': 'enterprise',
                'ZoneId': 'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise',
                'numberZoneMembers': '0',
                '@odata.id': "/redfish/v1/SFSS/1/ZoneDBs('config')/ZoneGroups(config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8)/Zones('config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise')",
                '@odata.type': '#Zones.Zones',
                '@odata.context': "/redfish/v1/SFSS/1/ZoneDBs('config')/ZoneGroups(config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8)/$metadata#Zones/Zones/$entity"}
        '''
        for zone in self.get_zones(instance, zone_group_id):
            if zone.get('ZoneName') == zone_name:
                return zone

        return None

    def get_zone_id(self, instance: int, zone_group_id: str, zone_name: str):
        '''
        Get zone ID by name.
        @return: The zone ID on success, None otherwise
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_zone_id(1, 'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8', 'enterprise')
           print(f'>>> {r}')
           >>> config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise
        '''
        zone = self.get_zone(instance, zone_group_id, zone_name)
        if zone is None:
            return None

        return zone.get('ZoneId')

    def create_zone(self, instance: int, zone_group_id: str, zone_name: str):
        '''
        Create a zone.
        @return: The zone ID on success, None otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.create_zone(1, 'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8', 'Voyager')
           print(f'>>> {r}')
           >>> config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:Voyager
        '''
        json_data = {
            'ZoneName': zone_name,
        }
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group_id})/Zones"
        reply = self._post(oid, json_data, {'Accept': 'application/json'})
        return reply.json().get('EId') if reply.ok else None

    def delete_zone(self, instance: int, zone_group_id: str, zone_id: str):
        '''
        Delete a zone.
        @return: True on success, False otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.delete_zone(
                   1, 'config:Klingons:nqn.1988-11.com.dell:SFSS:1:20220523215843e8',
                   config:Klingons:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:Bird-of-prey')
           print(f'>>> {r}')
           >>> True
        '''
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group_id})/Zones({zone_id})"
        reply = self._delete(oid)
        return reply.ok

    def add_zone_member(self, instance: int, zone_group_id: str, zone_id: str, member: str, role: str):
        '''
        Add a member to a zone.
        @return: The member ID on success, None otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.add_zone_member(
                   1,
                   'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8',
                   'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise',
                   'nqn.2014-08.org.nvmexpress:uuid:83294d56-1ebf-a154-d613-a7cb28c6ef39', 'Host')
           print(f'>>> {r}')
           >>> config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise:nqn.2014-08.org.nvmexpress:uuid:83294d56-1ebf-a154-d613-a7cb28c6ef39
        '''
        json_data = {
            'ZoneMemberId': member,
            'ZoneMemberType': 'FullQualifiedName',
            'Role': role,
        }
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group_id})/Zones({zone_id})/ZoneMembers"
        reply = self._post(oid, json_data, {'Accept': 'application/json'})
        return reply.json().get('EId') if reply.ok else None

    def get_zone_members(self, instance: int, zone_group_id: str, zone_id: str):
        '''
        Get the list of members in a zone.
        @return: The list of member dicts on success, None otherwise.
        @example:
           sfss = sfsslib.RestApi('1.2.3.4', 'admin', 'adminpass')
           r = sfss.get_zone_members(
                   1,
                   'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8',
                   'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise'))
           print(f'>>> {r}')
           >>> [{'ZoneMemberType': 'FullQualifiedName',
                 'ZoneMemberId': 'config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise:nqn.2014-08.org.nvmexpress:uuid:83294d56-1ebf-a154-d613-a7cb28c6ef39',
                 'Role': 'Host',
                 '@odata.id': "/redfish/v1/SFSS/1/ZoneDBs('config')/ZoneGroups(config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8)/Zones(config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise)/ZoneMembers('config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise:nqn.2014-08.org.nvmexpress:uuid:83294d56-1ebf-a154-d613-a7cb28c6ef39')",
                 '@odata.type': '#ZoneMembers.ZoneMembers',
                 '@odata.context': "/redfish/v1/SFSS/1/ZoneDBs('config')/ZoneGroups(config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8)/Zones(config:Starfleet:nqn.1988-11.com.dell:SFSS:1:20220523215843e8:enterprise)/$metadata#ZoneMembers/ZoneMembers/$entity"}]
        '''
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group_id})/Zones({zone_id})/ZoneMembers?$source=config&$expand=ZoneMembers"
        return self._get_list(oid, 'ZoneMembers')
