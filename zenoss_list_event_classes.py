#!/usr/bin/env python
# https://community.zenoss.com/forum/community-home/digestviewer/viewthread?GroupId=19&MessageKey=5a46e08b-1fc2-45eb-be5a-2a428f3ce2fc
import Globals
ZENPACK_NAME="ZenPacks.acme.EventClasses"

limit = 10000000
classFilter = None
count = 0
ec_count = 0
mappings_count = 0

ec_list = []

ec_properties = ['description',
                 'transform',
                ]

mapping_properties = [
                        'eventClassKey',
                        'example',
                        'explanation',
                        'regex',
                        'remove',
                        'resolution',
                        'rule',
                        'sequence',
                        'transform',
                        ]

zProperties = [
                'zEventAction',
                'zEventSeverity',
                'zFlappingIntervalSeconds',
                'zFlappingSeverity',
                'zFlappingThreshold',
                ]


def yaml_print(key='', value='', indent=0):

    head = indent*' '
    if key:
        key = '{}: '.format(key)
    value = str(value)

    multiline = len(str(value).splitlines()) > 1
    if multiline:
        print('{}{}|+'.format(head, key))
        for l in str(value).splitlines():
            print('  {}{}'.format(head, l))
    else:
        if ':' in value or '%' in value or '#' in value:
            print('{}{}{!r}'.format(head, key, value))
        elif value.startswith("'") or value.startswith("["):
            print('{}{}{!r}'.format(head, key, value))
        else:
            print('{}{}{}'.format(head, key, value))


yaml_print(key='name', value=ZENPACK_NAME, indent=0)
print('')
yaml_print(key='event_classes', value='', indent=0)

for ec in sorted([dmd.Events] + dmd.Events.getSubOrganizers(), key=lambda c: c.getOrganizerName().lower()):
    # ec isn't a dict, but a 'Acquisition.ImplicitAcquisitionWrapper'

    count += 1
    if count > limit:
        break

    '''
    {'zEventAction': 'status', 
    'description': '', 
    '_guid': 'f7df318c-8fbb-49c5-9259-c42c60542a27', 
    'transform': ''
    '__primary_parent__': <EventClass at Win>, 
    'instances': <ToManyContRelationship at instances>, 
    '_properties': ({'type': 'string', 'id': 'description', 'mode': 'w'}, 
                    {'type': 'text', 'id': 'transform', 'mode': 'w'}, 
                    {'visible': True, 'type': 'string', 'id': 'zEventAction'}), 
    'createdTime': DateTime('2014/03/11 17:39:45.367768 UTC'), 
    '_objects': ({'meta_type': 'ToOneRelationship', 'id': 'pack'}, 
                 {'meta_type': 'ToManyContRelationship', 'id': 'instances'}), 
     '__ac_local_roles__': {'admin': ['Owner']}, 
     'id': 'Userenv', 
     'pack': <ToOneRelationship at pack>}
    '''

    '''
    name
    subclasses
    description
    transform
    eventClassKey
    rule
    regex
    instances : mappings
    zEventAction, zEventClearClasses, zEventMaxTransformFails, zEventSeverity, zFlappingIntervalSeconds, zFlappingSeverity, zFlappingThreshold
    '''
    ec_dict = {}
    ec_name = ec.getOrganizerName()

    if classFilter and not ec_name == classFilter:
        # print(ec_name)
        continue

    # if not ec_name.startswith("/ATest"):
    # if not ec_name == "/HW":
    #    continue

    # print(ec.__dict__)
    ec_dict['name'] = ec_name
    ec_dict['id'] = ec.id

    for prop in ec._properties:
        prop_id = prop.get('id', None)
        prop_value = ec.getProperty(prop_id)
        # print('**Prop: {}={}'.format(prop_id, prop_value))
        if prop_value:
            ec_dict[prop_id] = ec.getProperty(prop_id)

    mapping_list = []
    for mapping in sorted(ec.instances(), key=lambda m: m.id.lower()):
        mapping_dict = {}
        for prop in mapping._properties:
            prop_id = prop.get('id', None)
            # print('prop: {}={}'.format(prop_id, mapping.getProperty(prop_id)))
            mapping_dict[prop_id] = mapping.getProperty(prop_id)
        mapping_dict['id'] = mapping.id
        mappings_count += 1
        mapping_list.append(mapping_dict)
    ec_dict['instances'] = mapping_list

    ec_count += 1

    ec_list.append(ec_dict)

    '''
    event_classes:
      /Status/Acme:
        remove: false
        description: Acme event class
        mappings:
          Widget:
            eventClassKey: WidgetEvent
            sequence:  10
            remove: true
            transform: | -
              if evt.message.find('Error reading value for') >= 0:
                  evt._action = 'drop'
    '''

    # print(ec_dict)

    # continue
    # YAML print ###################################################################

    yaml_print(key=ec_dict['name'], indent=2)
    yaml_print(key='remove', value='false', indent=4)
    # TODO: make a loop with variables
    # TODO: if multi-line, use |- and reformat on multiline

    # Event Class fields

    for field in ec_properties:
        if field in ec_dict:
            value = str(ec_dict[field])
            value = value.replace('\\\\', '\\')
            if value:
                yaml_print(key=field, value=value, indent=4)

    if any([z for z in zProperties if z in ec_dict]):
        yaml_print(key='zProperties', indent=4)
        for zprop in zProperties:
            if zprop in ec_dict:
                yaml_print(key=zprop, value=ec_dict[zprop], indent=6)

    # Mapping fields
    if ec_dict['instances']:
        yaml_print(key='mappings', indent=4)
        for mapping in ec_dict['instances']:
            # print('**{}**'.format(yaml.dump(mapping['rule'], default_flow_style=False)))
            # print(type(yaml.dump(mapping, default_flow_style=False)))
            yaml_print(key=mapping['id'], indent=6)
            yaml_print(key='remove', value='false', indent=8)
            if any([z for z in zProperties if z in mapping]):
                # print(mapping)
                # not sure whether it's working, zProperties aren't imported with Zenpack install ?
                yaml_print(key='zProperties', indent=8)
                for zprop in zProperties:
                    if zprop in mapping:
                        yaml_print(key=zprop, value=mapping[zprop], indent=10)
            for field in mapping_properties:
                if field in mapping:
                    value = str(mapping[field])
                    value = value.replace('\\\\', '\\')         # replace double-backslash with single
                    if value and value != 'None':
                        yaml_print(field, value, 8)

print('# Event Classes count: {}'.format(ec_count))
print('# Mappings  count: {}'.format(mappings_count))
