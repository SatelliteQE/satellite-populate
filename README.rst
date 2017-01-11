==================
Satellite-Populate
==================


.. image:: https://img.shields.io/pypi/v/satellite-populate.svg
        :target: https://pypi.python.org/pypi/satellite-populate

.. image:: https://img.shields.io/travis/SatelliteQE/satellite-populate.svg
        :target: https://travis-ci.org/SatelliteQE/satellite-populate

.. image:: https://readthedocs.org/projects/satellite-populate/badge/?version=latest
        :target: https://satellite-populate.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/SatelliteQE/satellite-populate/shield.svg
     :target: https://pyup.io/repos/github/SatelliteQE/satellite-populate/
     :alt: Updates


Populate and Validate the System using YAML


* Free software: GNU General Public License v3
* Documentation: https://satellite-populate.readthedocs.io.


Installation
------------

To install latest released version::

    pip install satellite-populate

To install from github master branch::

    pip install https://github.com/SatelliteQE/satellite-populate/tarball/master

For development::

    # fork https://github.com/SatelliteQE/satellite-populate/ to YOUR_GITHUB
    # clone your repo locally
    git clone git@github.com:YOUR_GITHUB/satellite-populate.git

    # add upstream remote
    git remote add upstream git@github.com:SatelliteQE/satellite-populate.git

    # create a virtualenv
    mkvirtualenv satellite-populate
    workon satellite-populate

    # install for development (editable)
    python setup.py develop

Features
--------

YAML based actions
++++++++++++++++++

Data population definition goes to YAML file e.g ``office.yaml`` in the following
example we are going to create 2 organizations and 2 admin users::

    vars:
      org_names:
        - Dunder Mifflin
        - Wernham Hogg

    actions:

      - model: Organization
        register: default_orgs
        data:
          name: "{{ item }}"
          label: org{{ item|replace(' ', '') }}
          description: This is a satellite organization named {{ item }}
        with_items: org_names

      - model: User
        data:
          admin: true
          firstname: Michael
          lastname: Scott
          login: mscott
          password:
            from_factory: alpha
          organization:
            from_registry: default_orgs
          default_organization:
            from_registry: default_orgs[0]

      - model: User
        data:
          admin: true
          firstname: David
          lastname: Brent
          login: dbrent
          password:
            from_factory: alpha
          organization:
            from_registry: default_orgs
          default_organization:
            from_registry: default_orgs[1]


On the populate file you can define CRUD actions such as **create**, **delete**, **update**
if ``action:`` is not defined, the default will be ``create``.

And also there is **special actions** and **custom actions** explained later.

Populate Satellite With Entities
++++++++++++++++++++++++++++++++

Considering ``office.yaml`` file above you can populate satellite system with the
command line::

    $ satellite-populate office.yaml -h yourserver.com --output=office.yaml -v

In the above command line ``-h`` stands for ``--hostname``, ``--output`` is the
output file which will be written to be used to validate the system, and ``-v`` is
the verbose level.

To see the list of available arguments please run::

    # satellite-populate --help

Validate if system have entities
++++++++++++++++++++++++++++++++

Once you run ``satellite-populate`` you can use the outputted file to validate the system.
as all the output files are named as ``validation_<name>.yaml`` in office example you can run::

   $ satellite-populate validation_office.yaml -v

Using that validation file the system will be checked for entities existence, read-only.
The Validation file exists because during the population dynamic data is generated such as
passwords and strings ``from_factory`` and also some entities can be deleted or updated
so validation file takes care of it.

Special actions
+++++++++++++++

Some builtin special actions are:

- assertion
- echo
- register
- unregister


In the following example we are going to run a complete test case using
actions defined in YAML file, if validation fails system returns status 0
which can be used to automate tests::

      # A TEST CASE USING SPECIAL ACTIONS
      # Create a plain vanilla activation key
      # Check that activation key is created and its "unlimited_hosts"
      # attribute defaults to true

      - action: create
        log: Create a plain vanilla activation key
        model: ActivationKey
        register: vanilla_key
        data:
           name: vanilla
           organization:
             from_registry: default_orgs[0]

      - action: assertion
        log: >
          Check that activation key is created and its "unlimited_hosts"
          attribute defaults to true
        operation: eq
        register: vanilla_key_unlimited_hosts
        data:
          - from_registry: vanilla_key.unlimited_hosts
          - true

      - action: echo
        log: Vanilla Key Unlimited Host is False!!!!
        level: error
        print: true
        when: vanilla_key_unlimited_hosts == False

      - action: echo
        log: Vanilla Key Unlimited Host is True!!!!
        level: info
        print: true
        when: vanilla_key_unlimited_hosts

      - action: register
        data:
          you_must_update_vanilla_key: true
        when: vanilla_key_unlimited_hosts == False

Custom actions
++++++++++++++

And you can also have special actions defined in a custom populator.

Lets say you have this python module in your project, properly available on
PYTHONPATH::

    from satellite_populate.api import APIPopulator

    class MyPopulator(APIPopulator):
        def action_writeinfile(self, rendered_data, action_data):
            with open(rendered_data['path'], 'w') as output:
                output.write(rendered_data['content'])

Now go to your ``test.yaml`` and write::

    config:
      populator: mine
      populators:
        mine:
          module: mypath.mymodule.MyPopulator

    actions:

      - action: writeinfile
        path: /tmp/test.txt
        text: Hello World!!!

and run:

  $ satellite-populate test.yaml -v

Decorator for test cases
++++++++++++++++++++++++

Having a data_file like::

    actions:
      - model: Organization
        register: organization_1
        data:
          name: My Org

Then you can use in decorators::

    @populate_with('file.yaml')
    def test_case_(self):
        'My Org exists in system test anything here'

And getting the populated entities inside the test_case::

    @populate_with('file.yaml', context=True)
    def test_case_(self, context=None):
        assert context.entities.organization_1.name == 'My Org'

You can also set a name to the context argument::

    @populate_with('file.yaml', context='my_context')
    def test_case_(self, my_context=None):
        assert my_context.organization_1.name == 'My Org'

NOTE::

    That is important that ``context`` argument always be declared using
    either a default value ``my_context=None`` or handle in ``**kwargs``
    Otherwise ``py.test`` may try to use this as a fixture placeholder.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

