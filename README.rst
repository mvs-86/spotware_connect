====================
spotware_connect
====================

.. image:: https://img.shields.io/pypi/v/spotware_connect.svg
        :target: https://pypi.python.org/pypi/spotware_connect

.. image:: https://img.shields.io/travis/marcus-santos/spotware_connect.svg
        :target: https://travis-ci.org/marcus-santos/spotware_connect

.. image:: https://coveralls.io/repos/github/marcus-santos/spotware_connect/badge.svg
        :target: https://coveralls.io/github/marcus-santos/spotware_connect

.. image:: https://readthedocs.org/projects/spotware_connect/badge/?version=latest
        :target: https://spotware_connect.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/github/license/marcus-santos/spotware_connect
        :alt: License




A python client wraper for Spotware Open API 2 https://connect.spotware.com/docs/open_api_2


* Free software: GNU General Public License v3
* Documentation: https://spotware_connect.readthedocs.io.

Quickstart
--------
Install with pip::
    
    $ pip install spotware-connect


A sample to request server version::

    import spotware_connect as sc

    c = sc.Client()

    @c.event
    def connect():
        c.emit("VersionReq")

    @c.message(msgtype="VersionRes")
    def version(msg, payload, version, **kargs):
        print("Server version: ", version)
        c.stop()
    
    c.start(timeout=5) # optional timeout in seconds

See the usage_ in docs_ for a complete example with App Authorization.

.. _usage: https://spotware-connect.readthedocs.io/en/latest/usage.html
.. _docs: https://spotware-connect.readthedocs.io/en/latest/

Features
--------

* Simple client for connecting, sending and receiving Protobuf Messages
* Use decorators to specify wich messages to process
* No need to worry about sockets, bytes and message structure
* Use abbreviated names for sending and receiving payloads: VersionReq translates to ProtoOAVersionReq
* Requests limit 5/second more information about limits here_

.. _here: https://connect.spotware.com/docs/frequently-asked-questions

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Using twisted_ for network layer

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _twisted: https://github.com/twisted/twisted
