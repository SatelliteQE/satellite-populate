.. highlight:: shell

============
Installation
============


Stable release
--------------

To install satellite-populate, run this command in your terminal:

.. code-block:: console

    $ pip install satellite-populate

This is the preferred method to install satellite-populate, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

To install from github master branch `tarball`_::

    pip install https://github.com/SatelliteQE/satellite-populate/tarball/master

For development from the `Github repo`_.::

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


Testing if installation is good::

     $ satellite-populate --test
     satellite_populate.base - INFO - ECHO: Hello, if you can see this it means that I am working!!!



.. _Github repo: https://github.com/SatelliteQE/satellite-populate
.. _tarball: https://github.com/SatelliteQE/satellite-populate/tarball/master
