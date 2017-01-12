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

.. image:: https://pyup.io/repos/github/satelliteqe/satellite-populate/shield.svg
     :target: https://pyup.io/repos/github/satelliteqe/satellite-populate/
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
    cd satellite-populate

    # add upstream remote
    git remote add upstream git@github.com:SatelliteQE/satellite-populate.git

    # create a virtualenv
    mkvirtualenv satellite-populate
    workon satellite-populate

    # install for development (editable)
    pip install -r requirements.txt

Features
--------

YAML based actions
++++++++++++++++++

Data population definition goes to YAML file e.g ``office.yaml`` in the following
example we are going to create 2 organizations and 2 admin users using lists::


    vars:

      org_names:
        - Dunder Mifflin
        - Wernham Hogg

      user_list:
        - firstname: Michael
          lastname: Scott

        - firstname: David
          lastname: Brent

    actions:

      - model: Organization
        with_items: org_names
        register: default_orgs
        data:
          name: "{{ item }}"
          label: org{{ item.replace(' ', '') }}
          description: This is a satellite organization named {{ item }}

      - model: User
        with_items: user_list
        data:
          admin: true
          firstname: "{{ item.firstname }}"
          lastname: "{{ item.lastname }}"
          login: "{{ '{0}{1}'.format(item.firstname[0], item.lastname) | lower }}"
          password:
            from_factory: alpha
          organization:
            from_registry: default_orgs
          default_organization:
            from_registry: default_orgs[loop_index]


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

        @populate_with('file.yaml', context_name='my_context')
        def test_case_(self, my_context=None):
            assert my_context.organization_1.name == 'My Org'

        You can also set a customized context wrapper to the
        context_wrapper argument::

            def my_custom_context_wrapper(result):
                # create an object using result
                my_context = MyResultContext(result)
                return my_context

            @populate_with('file.yaml', context_name='my_context',
                           content_wrapper=my_custom_context_wrapper)
            def test_case_(self, my_context=None):
                # assert with some expression using my_context object returned
                # my_custom_context_wrapper
                assert some_expression

NOTE::

    That is important that ``context`` argument always be declared using
    either a default value ``my_context=None`` or handle in ``**kwargs``
    Otherwise ``py.test`` may try to use this as a fixture placeholder.

    if context_wrapper is set to None, my_context will be the pure unmodified
    result of populate function.


Satellite versions
------------------

This code is by default prepared to run against Satellite **latest** version
which means the use of the **latest** master from **nailgun** repository.

If you need to run this tool in older versions e.g: to tun upgrade tests, you
have to setup **nailgun** version.

You have 2 options:

Manually
++++++++

before installing satellite-populate install specific nailgun version as
the following list.

- Satellite 6.1.x::

    pip install -e git+https://github.com/SatelliteQE/nailgun.git@0.28.0#egg=nailgun
    pip install satellite-populate

- Satellite 6.2.x::

    pip install -e git+https://github.com/SatelliteQE/nailgun.git@6.2.z#egg=nailgun
    pip install satellite-populate

- Satellite 6.3.x (latest)::

    pip install -e git+https://github.com/SatelliteQE/nailgun.git#egg=nailgun
    pip install satellite-populate



Docker
++++++


If you need to run ``satellite-populate`` in older Satellite versions you can
use the ``docker images`` so it will manage the correct nailgun version to
be used with that specific system version.

First pull image from Docker Hub::

    docker pull SatelliteQE/satellite-populate:latest

Change ``:latest`` to specific tag. e.g:  ``:6.1`` or ``:6.2``


Test it::

    docker run SatelliteQE/satellite-populate --test

Then run::

    docker run -v $PWD:/datafiles SatelliteQE/satellite-populate /datafiles/theoffice.yaml -v -h server.com

You must map your local folder containing datafiles

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

