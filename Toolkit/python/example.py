#!/usr/bin/env python3
import sys
import requests
import sfsslib

sfss = sfsslib.RestApi('w.x.y.z', 'admin', 'adminpass')


def zone(instance: int, zone_group_name: str):
    reply = sfss.create_zone_group(instance, zone_group_name)
    if not reply.ok:
        sys.exit('Failed to create zone group')

    # Create Zones foreach Host
    hosts = sfss.get_hosts(instance)
    for host in hosts:
        zone_name = host['TransportAddress']
        reply = sfss.create_zone(instance, zone_name)
        if not reply.ok:
            sys.exit('Failed to create zone')

        nqn = host['NQN']  # REVIEW: Unused
        id = host['Id']
        reply = sfss.add_zone_member(instance, zone_name, id, 'Host')
        if not reply.ok:
            sys.exit('Failed to add zone member (Host)')

        # For each subsystem, add subsystem NQN to the Host Zone
        subsystems = sfss.get_subsystems(instance)
        for subsystem in subsystems:
            nqn = subsystem['NQN']  # REVIEW: Unused
            id = subsystem['Id']
            reply = sfss.add_zone_member(instance, zone_name, id, 'Subsystem')
            if not reply.ok:
                sys.exit('Failed to add zone member (Subsystem)')

    # Activate the Zone group
    zone_group = sfss.get_zone_group(instance)
    reply = sfss.activate_zonedb(instance, zone_group)
    if not reply.ok:
        sys.exit('Failed to activate zone group')


zone(1, 'ZG-VLAN100')  # Zone A
zone(2, 'ZG-VLAN200')  # Zone B
