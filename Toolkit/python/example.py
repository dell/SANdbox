#!/usr/bin/env python3
import requests
import sfsslib

sfss = sfsslib.RestApi('w.x.y.z', 'admin', 'adminpass')


def zone(instance: int, zone_group_name: str):
    sfss.create_zone_group(instance, zone_group_name)

    try:
        hosts = sfss.get_hosts(instance).json()['Hosts']
    except KeyError:
        raise 'Failed to retrieve Hosts'

    # Create Zones foreach Host
    for host in hosts:
        zone_name = host['TransportAddress']
        reply = sfss.create_zone(instance, zone_name)
        if reply.status_code != requests.codes.ALL_GOOD:
            raise 'Failed to create zone'

        nqn = host['NQN']  # REVIEW: Unused
        id = host['Id']
        reply = sfss.add_zone_member(instance, zone_name, id, 'Host')
        if reply.status_code != requests.codes.ALL_GOOD:
            raise 'Failed to add zone member (Host)'

        # For each subsystem, add subsystem NQN to the Host Zone
        subsystems = sfss.get_subsystems(instance).json()  # REVIEW: This returns a dict and not a list
        for subsystem in subsystems:
            nqn = subsystem['NQN']  # REVIEW: Unused
            id = subsystem['Id']
            reply = sfss.add_zone_member(instance, zone_name, id, 'Subsystem')
            if reply.status_code != requests.codes.ALL_GOOD:
                raise 'Failed to add zone member (Subsystem)'

    # Activate the Zone group
    zone_group = sfss.get_zonedb_configdb(instance).json()['ZoneGroups']
    reply = sfss.activate_zonedb(instance, zone_group)
    if reply.status_code != requests.codes.ALL_GOOD:
        raise 'Failed to activate zone group'


zone(1, 'ZG-VLAN100')  # Zone A
zone(2, 'ZG-VLAN200')  # Zone B
