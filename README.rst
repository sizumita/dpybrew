=======
dpybrew
=======


.. image:: https://img.shields.io/pypi/v/dpybrew.svg
        :target: https://pypi.python.org/pypi/dpybrew

.. image:: https://img.shields.io/travis/sizumita/dpybrew.svg
        :target: https://travis-ci.com/sizumita/dpybrew

.. image:: https://readthedocs.org/projects/dpybrew/badge/?version=latest
        :target: https://dpybrew.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A discord.py extension/service manager


* Free software: MIT license
* Documentation: https://dpybrew.readthedocs.io.

=============
Installation
=============

You can install dpybrew from Pypi.

.. code-block:: console

    $ pip install dpybrew


======
Useage
======

-------------------
Show extension list
-------------------

.. code-block:: console

    $ dpybrew list

or

.. code-block:: console

    $ dpybrew list your-extensions-path


------------------
Install extensions
------------------

.. code-block:: console

    $ dpybrew install [extension-name]

or

.. code-block:: console

    $ dpybrew install git+url -dir cogs/

All extensions -> https://gist.github.com/sizumita/19ec79e3ad0ecfae89cca665ddf717e1


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
