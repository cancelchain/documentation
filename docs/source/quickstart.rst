Quick Start
===========

Requirements
------------

Python >= 3.9

Install
-------

Install CancelChain using pip:

.. code-block:: console

  $ pip install cancelchain

It is recommended that a `python virtual environment`_ is used for `all <https://realpython.com/python-virtual-environments-a-primer/#avoid-system-pollution>`__ `the <https://realpython.com/python-virtual-environments-a-primer/#sidestep-dependency-conflicts>`__ `usual <https://realpython.com/python-virtual-environments-a-primer/#minimize-reproducibility-issues>`__ `reasons <https://realpython.com/python-virtual-environments-a-primer/#dodge-installation-privilege-lockouts>`_.


Configure
---------

Create a `python-dotenv`_ ``.env`` file. The ``cancelchain`` command loads a ``.env`` file in the current working directory by default.  See :ref:`dotenv documentation <Dotenv>` to locate the file elsewhere. The following ``cancelchain`` command examples assume that the ``.env`` file is loaded by default.

A minimal ``.env`` configuration file:

.. code-block:: console

  # Flask Settings
  FLASK_APP=cancelchain
  FLASK_RUN_HOST=0.0.0.0
  FLASK_SECRET_KEY=0b6ceaa3b10d3e7a5dc53194

  # Flask-SQLAlchemy Settings
  FLASK_SQLALCHEMY_DATABASE_URI=sqlite:///cc.sqlite

The :py:data:`FLASK_SECRET_KEY <SECRET_KEY>` value should be a unique random string.

See the :ref:`Configuration Documentation <Configuration>` for more configuration settings.


Initialize
----------

Create a local database by running the :ref:`init command <Init>`:

.. code-block:: console

  $ cancelchain init

The :py:data:`FLASK_SQLALCHEMY_DATABASE_URI <SQLALCHEMY_DATABASE_URI>` value in the example configuration above specifies a `SQLite`_ database called ``cc.sqlite`` with a file path relative to the ``cancelchain`` `instance folder`_.


Import Data
-----------

Download the most recent export of `CancelChain data`_. This `JSON Lines`_ file is updated at every blockchain epoch (2016 blocks or approximately every two weeks).

Run the :ref:`import command <Import>`, passing it the location of the downloaded file:

.. code-block:: console

  $ cancelchain import path/to/cancelchain.jsonl

This command could take a while to run depending on your computer and the number of blocks imported. A progress bar will display with estimated time remaining. You can run the ``import`` command multiple times and it will only import new blocks that are not yet in the database.


Run
---

Run the ``cancelchain`` application by issuing the ``run`` command:

.. code-block:: console

  $ cancelchain run

Open `http://localhost:5000 <http://localhost:5000>`_ in a browser to explore the local copy of the blockchain.

Home Page (Current Chain)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://github.com/cancelchain/cancelchain/blob/7a4fab66dfe6026e56c79df3e147b1ecbdbb6158/readme-assets/browser-chain.png?raw=true
   :width: 500pt

Block Page
^^^^^^^^^^

.. image:: https://github.com/cancelchain/cancelchain/blob/7a4fab66dfe6026e56c79df3e147b1ecbdbb6158/readme-assets/browser-block.png?raw=true
   :width: 500pt

Transaction Page
^^^^^^^^^^^^^^^^

.. image:: https://github.com/cancelchain/cancelchain/blob/7a4fab66dfe6026e56c79df3e147b1ecbdbb6158/readme-assets/browser-txn.png?raw=true
   :width: 500pt

Running the ``cancelchain`` application also exposes a set of web service endpoints that comprise the communications layer of the blockchain. See the  :ref:`API Documentation <API>` for more information.

There are other ``cancelchain`` commands for interacting with the blockchain. See the :ref:`Command Line Interface Documentation <Command Line Interface>` for more information or run ``cancelchain --help``.


Joining The CancelChain Network
-------------------------------

The CancelChain is run by a permissioned network of nodes. A CancelChain instance requires :ref:`miller <Miller>` or :ref:`transactor <Transactor>` role :ref:`API access <API Roles>` to a node in the network in order to have locally milled blocks or submitted transactions propagate to the official CancelChain.

`The Cancel Button`_ allows :ref:`reader <Reader>` role :ref:`API access <API Roles>` to any account that completes at least one transaction on the blockchain:

1) `Register for an account`_.
2) Submit a successful transaction for any subject. Access won't be granted until the sentiment transaction successfully completes.
3) Click `Download Account Key`_ on the `account page`_ to download the account's key (`PEM`_) file.
4) Create a directory called ``wallets`` and copy the downloaded key file into it.
5) Add the following settings to the ``.env`` configuration file. Replace ``CCTheCancelButtonAddressCC`` with the address on the `account page`_ and ``/path/to/wallet`` with the path to the ``wallets`` directory created above:

  .. code-block:: console

    # CancelChain Settings
    CC_NODE_HOST=http://CCTheCancelButtonAddressCC@localhost:5000
    CC_PEERS=["https://CCTheCancelButtonAddressCC@thecancelbutton.com"]
    CC_DEFAULT_COMMAND_HOST=https://CCTheCancelButtonAddressCC@thecancelbutton.com
    CC_WALLET_DIR=/path/to/wallets

6) Restart to load the new configuration.

See :ref:`Configuration Documentation <Configuration>` for more detailed information about these settings.

The :ref:`reader <Reader>` role :ref:`API access <API Roles>` allows the :ref:`sync command <Sync>` to update to the most recent peer block data:

.. code-block:: console

  $ cancelchain sync

This command could take a while to run depending on your computer, internet access, and the number of blocks synchronized. A progress bar will display with estimated time remaining. You can run the :ref:`sync command <Sync>` multiple times and it will only synchronize new blocks that are not yet in the database.

Reader access also allows querying data (i.e. subject counts and balances) using the CLI. See :ref:`Command Line Interface Documentation <Command Line Interface>` for more information.

If you would like to be granted other :ref:`API access <API Roles>` to a node in the CancelChain network, send an email to contact@cancelchain.org including what kind of role you'd like (e.g. :ref:`reader <Reader>`, :ref:`transactor <Transactor>`, or :ref:`miller <Miller>`) and how you intend to use it (e.g. research, business, non-profit, hobby).

See the :ref:`documentation <The Ledger>` for some potential development ideas.


.. _account page: https://thecancelbutton.com/account
.. _CancelChain data: https://storage.googleapis.com/blocks.cancelchain.org/cancelchain.jsonl
.. _Download Account Key: https://thecancelbutton.com/pem
.. _instance folder: https://flask.palletsprojects.com/en/2.2.x/config/#instance-folders
.. _JSON Lines: https://jsonlines.org/
.. _PEM: https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail
.. _python virtual environment: https://docs.python.org/3/library/venv.html
.. _python-dotenv: https://pypi.org/project/python-dotenv/
.. _Register for an account: https://thecancelbutton.com/register
.. _SQLite: https://sqlite.org/index.html
.. _The Cancel Button: https://thecancelbutton.com
