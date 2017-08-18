# coding: utf-8
"""Default base config values"""
from satellite_populate.utils import SmartDict

REQUIRED_MODULES = {
    'fauxfactory': 'fauxfactory',
    'env': 'os.environ'
}

RAW_SEARCH_RULES = {
    # force Organization to always perform raw_search
    'organization': {'_force_raw': True},
    'user': {
        '_force_raw': True,
        'organization': {
            # rename organization Entity to organization_id
            'rename': 'organization_id',
            # and get the attr 'id' from object
            'attr': 'id',
            # using object in index 0 (because it is a list)
            'index': 0,
            # if was dict key_name here
            # 'key': 'name_of_key'
        },
        # remove fields from search
        'password': {'remove': True},
        'default_organization': {'remove': True},
        'admin': {'remove': True},
    },
    'repository': {
        'url': {'remove': True},
    },
    'architecture': {'_force_raw': True},
    'bookmark': {
        '_force_raw': True,
        'query': {'remove': True},
        'public': {'remove': True}
    },
    'configtemplate': {
        '_force_raw': True,
        'template_combinations': {'remove': True},
        'audit_comment': {'remove': True},
        'locked': {'remove': True},
        'organization': {'remove': True},
        'template': {'remove': True},
        'template_kind': {'remove': True},
        'snippet': {'remove': True},
        'operatingsystem': {'remove': True},
    },
    'interface': {'_force_raw': True},
    'location': {'_force_raw': True},
    'media': {
        '_force_raw': True,
        'os_family': {'remove': True},
        'path': {'remove': True},
        'location': {'remove': True},
        'operatingsystem': {'remove': True},
        'organization': {'remove': True},
    },
    'operatingsystem': {
        '_force_raw': True,
        'release_name': {'remove': True},
        'description': {'remove': True},
        'architecture': {'remove': True},
        'family': {'remove': True},
        'major': {'remove': True},        
        'minor': {'remove': True},
        'medium': {'remove': True},
        'ptable': {'remove': True},
        'config_template': {'remove': True},
        'provisioning_template': {'remove': True},
        'password_hash': {'remove': True},
        'title': {'remove': True},        
    },
    'partitiontable': {
        '_force_raw': True,
        'layout': {'remove': True},
        'location': {'remove': True},
        'organization': {'remove': True},
        'os_family': {'remove': True},
    },
    'provisioningtemplate': {
        '_force_raw': True,
        'audit_comment': {'remove': True},
        'locked': {'remove': True},
        'organization': {'remove': True},
        'location': {'remove': True},
        'template': {'remove': True},
        'template_combinations': {'remove': True},
        'template_kind': {'remove': True},
        'snippet': {'remove': True},
        'operatingsystem': {'remove': True},
    },
    'role': {'_force_raw': True},
}

DEFAULT_CONFIG = SmartDict({
    'populator': 'api',
    'populators': {
        'api': {
            'module': 'satellite_populate.api.APIPopulator'
        }
    },
    'verbose': 0,
    'username': 'admin',
    'password': 'changeme',
    'hostname': None,
    'output': 'validate_data.yaml'
})

TEST_DATA = """
actions:
  - action: echo
    log: Hello, if you can see this it means that I am working!!!
  - action: register
    data:
      you: "{{ env.USER }}"
      path: "{{ env.PWD }}"
  - action: echo
    when: you is not None
    log: And your username is {{ you }}
  - action: echo
    when: path is not None
    log: And I am running from {{ path }}
  - action: create
    model: Organization
    data:
      name: testing
    silent_errors: true
  - action: echo
    level: DEBUG
    log: >
       And you should see above an error message saying that
       no host has been supplied, thats ok! this test should error
       if you can see error message and HTTP debug message it means
       that it is working well!!!
"""
