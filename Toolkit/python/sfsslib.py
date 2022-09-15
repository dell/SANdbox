# Copyright (c) 2022, Dell Inc. or its subsidiaries.  All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See the LICENSE file for details.
#
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
        return f'{self._url}{"" if oid[0] == "/" else "/"}{oid}'

    def __hdrs__(self, headers: dict):
        if headers is not None:
            headers.update(self._headers)
        else:
            headers = self._headers
        return headers

    def _get(self, oid: str, headers=None):
        reply = requests.get(
            self.__uri__(oid),
            auth=self._creds,
            headers=self.__hdrs__(headers),
            verify=False,
        )
        return reply

    def _put(self, oid: str, json_data: dict, headers=None):
        reply = requests.put(
            self.__uri__(oid),
            auth=self._creds,
            headers=self.__hdrs__(headers),
            json=json.dumps(json_data),
            verify=False,
        )
        return reply

    def _post(self, oid: str, json_data: dict, headers=None):
        reply = requests.post(
            self.__uri__(oid),
            auth=self._creds,
            headers=self.__hdrs__(headers),
            json=json.dumps(json_data),
            verify=False,
        )
        return reply

    def _delete(self, oid: str, headers=None):
        reply = requests.delete(
            self.__uri__(oid),
            auth=self._creds,
            headers=self.__hdrs__(headers),
            verify=False,
        )
        return reply

    def get_ip_address_management(self):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = 'SFSSApp/IpAddressManagements?$expand=IpAddressManagements'
        return self._get(oid)

    def edit_ipv4_address_management(self, iface: str, addr: str, cfg: str, gw: str, plen: int, mtu: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        json_data = {
            'IPV4Address': addr,
            'IPV4Config': cfg,
            'IPV4Gateway': gw,
            'IPV4PrefixLength': plen,
            'MTU': mtu,
        }
        oid = f'SFSSApp/IpAddressManagements({iface})'
        return self._put(oid, json_data)

    def pull_register_ddc(self, instance: int, trtype: str, traddr: str, trsvcid: int, activate: bool):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        ip = ipaddress.ip_address(traddr)
        json_data = {
            'TransportType': trtype,
            'TransportAddress': traddr,
            'PortId': trsvcid,
            'TransportAddressFamily': f'IPV{ip.version}',
            'Activate': activate,
        }
        oid = f'SFSS/{instance}/DDCs'
        return self._post(oid, json_data, {'Accept': 'application/json'})

    def get_ddcs(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = f'SFSS/{instance}/DDCs'
        return self._get(oid)

    def delete_ddc(self, instance: int, ddc: str):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = f'SFSS/{instance}/DDCs({ddc})'
        return self._delete(oid, {'Accept': 'application/json'})

    def get_subsystems(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = f'SFSS/{instance}/Subsystems?$expand=Subsystems'
        return self._get(oid)

    def get_instance(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = f"SFSSApp/CDCInstanceManagers('{instance}')"
        return self._get(oid)

    def create_instance(self, instance: int, interfaces: str):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        json_data = {
            'InstanceIdentifier': instance,
            'Interfaces': interfaces,
            'CDCAdminState': 'Enable',
            'DiscoverySvcAdminState': 'Enable',
        }
        oid = f"SFSSApp/CDCInstanceManagers('{instance}')"
        return self._put(oid, json_data)

    def get_foundational_configs(self):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = 'SFSSApp/FoundationalConfigs?$expand=FoundationalConfigs'
        return self._get(oid)

    def get_hosts(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = f'SFSS/{instance}/Hosts?$expand=Hosts'
        return self._get(oid)

    def get_zonedb(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = f'SFSS/{instance}/ZoneDBs'
        return self._get(oid)

    def get_zonedb_configdb(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = f"SFSS/{instance}/ZoneDBs('config')?$source=config"
        return self._get(oid)

    def get_zonedb_activedb(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        # REVIEW: This is the same as get_zone_group
        oid = f"SFSS/{instance}/ZoneDBs('active')?"
        return self._get(oid)

    def activate_zonedb(self, instance: int, zone_group: str):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        json_data = {
            'ActivateStatus': 'Activate',
        }
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups('{zone_group}')"
        return self._put(oid, json_data)

    def deactivate_zonedb(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/) on success, None otherwise.'''
        zone_group = self.get_zone_group(instance)
        if zone_group is None:
            return None

        json_data = {
            'ActivateStatus': 'DeActivate',
        }
        oid = f"SFSS/{instance}/ZoneDBs('active')/ZoneGroups('{zone_group}')"
        return self._put(oid, json_data)

    def get_zone_group(self, instance: int):
        '''Get Zone Group.
        @return: Zone group on success, None otherwise.'''
        # REVIEW: This is the same as get_zonedb_configdb
        oid = f"SFSS/{instance}/ZoneDBs('config')?$source=config"
        reply = self._get(oid)
        if reply.status_code != requests.codes.ALL_GOOD:
            return None

        try:
            return reply.json()['ZoneGroups']
        except KeyError:
            return None

    def create_zone_group(self, instance: int, zone_group_name: str):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        # REVIEW: $Headers is undefined
        json_data = {
            'ZoneDBType': 'config',
            'ZoneGroupName': zone_group_name,
        }
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups"
        return self._post(oid, json_data, {'Accept': 'application/json'})

    def delete_zone_group(self, instance: int, zone_group_name: str):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        # REVIEW: zone_group_name should be in parenthesis
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group_name})"
        return self._delete(oid)

    def get_zones(self, instance: int):
        '''Get all the zones.
        @return: tuple(zone_group, list-of-zones) on success, tuple(None, []) otherwise.'''
        zone_group = self.get_zone_group(instance)
        if zone_group is None:
            return None, []

        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group})/Zones?$source=config&$expand=Zones"
        reply = self._get(oid)
        if reply.status_code != requests.codes.ALL_GOOD:
            return None, []

        return zone_group, reply.json()

    def get_zone(self, instance: int, zone_name: str):
        '''Get zone by name.
        @return: A tuple (zone_group, zone_id) on success, (None, None) otherwise'''
        zone_group, zones = self.get_zones(instance)
        if zone_group is None:
            return None, None

        for zone in zones:
            if zone.get('ZoneName') == zone_name:
                return zone_group, zone.get('ZoneId')

        return None, None

    def create_zone(self, instance: int, zone_name: str):
        '''@return: requests.Response object (see https://requests.readthedocs.io/) on success, None otherwise.'''
        # REVIEW: $Headers is undefined
        zone_group = self.get_zone_group(instance)
        if zone_group is None:
            return None
        json_data = {
            'ZoneName': zone_name,
        }
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group})/Zones"
        return self._post(oid, json_data, {'Accept': 'application/json'})

    def delete_zone(self, instance: int, zone_name: str):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        # REVIEW: $Headers is undefined
        zone_group, zone_id = self.get_zone(instance, zone_name)
        if None in (zone_group, zone_id):
            return None

        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group})/Zones({zone_id})"
        return self._delete(oid)

    def add_zone_member(self, instance: int, zone_name: str, member: str, role: str):
        '''@return: requests.Response object (see https://requests.readthedocs.io/) on success, None otherwise.'''
        # REVIEW: $Headers is undefined
        zone_group, zone_id = self.get_zone(instance, zone_name)
        if None in (zone_group, zone_id):
            return None

        json_data = {
            'ZoneMemberId': member,
            'ZoneMemberType': 'FullQualifiedName',
            'Role': role,
        }
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups({zone_group})/Zones({zone_id})/ZoneMembers"
        return self._post(oid, json_data, {'Accept': 'application/json'})

    def get_zonedb_configdb_zone_group(self, instance: int):
        '''@return: requests.Response object (see https://requests.readthedocs.io/)'''
        oid = f"SFSS/{instance}/ZoneDBs('config')/ZoneGroups?$source=config"
        return self._get(oid)


#    def get_zonedb_activedb(self, instance: int):
#        # REVIEW: function defined twice
#        # REVIEW: This is the same as get_zone_group
#        return self._get(f"SFSS/{instance}/ZoneDBs('active')")
