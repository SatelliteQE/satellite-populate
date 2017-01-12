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
    }
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
