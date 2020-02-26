====================
spotware_connect
====================

.. image:: https://img.shields.io/pypi/v/spotware_connect.svg
        :target: https://pypi.python.org/pypi/spotware_connect

.. image:: https://img.shields.io/travis/marcus-santos/spotware_connect.svg
        :target: https://travis-ci.org/marcus-santos/spotware_connect

.. image:: https://readthedocs.org/projects/spotware_connect/badge/?version=latest
        :target: https://spotware_connect.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/github/license/marcus-santos/spotware_connect
        :alt: License




A python client wraper for Spotware Open API 2 https://connect.spotware.com/docs/open_api_2


* Free software: GNU General Public License v3
* Documentation: https://spotware_connect.readthedocs.io.


Features
--------

* Simple client for connecting, sending and receiving Protobuf Messages
* Use decorators to specify wich messages to process
* No need to worry about sockets, bytes and message structure
* Use abbreviated names for sending and receiving payloads: VersionReq translates to ProtoOAVersionReq
* Requests limit 5/second more information: https://connect.spotware.com/docs/frequently-asked-questions

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
