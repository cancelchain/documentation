Quick Start
===========

Requirements
------------

Python >= 3.9

Installation
------------

Install CancelChain using pip:

.. code-block:: console

  $ pip install cancelchain

It is recommended that a `python virtual environment`_ is used for `all <https://realpython.com/python-virtual-environments-a-primer/#avoid-system-pollution>`__ `the <https://realpython.com/python-virtual-environments-a-primer/#sidestep-dependency-conflicts>`__ `usual <https://realpython.com/python-virtual-environments-a-primer/#minimize-reproducibility-issues>`__ `reasons <https://realpython.com/python-virtual-environments-a-primer/#dodge-installation-privilege-lockouts>`_.


Sample Configuration
--------------------

Create a `python-dotenv`_ ``.env`` file. Here is an example minimal configuration:

.. code-block:: console

  # Flask Settings
  FLASK_APP=cancelchain
  FLASK_RUN_HOST=0.0.0.0

  # CancelChain Settings
  CC_SECRET_KEY=0b6ceaa3b10d3e7a5dc53194
  CC_SQLALCHEMY_DATABASE_URI=sqlite:///cc.sqlite

The `CC_SECRET_KEY <https://docs.cancelchain.org/en/latest/usage.html#SECRET_KEY>`_ value should be a unique random string.

See the `Configuration Documentation`_ for more configuration settings.

The ``cancelchain`` command loads a ``.env`` file by default if it is located either in the current working directory or in the ``cancelchain`` `instance folder`_. Use the ``--env-file`` parameter to specify an alternate file path.

You can find the location of the `instance folder`_ by running the ``cancelchain`` `shell command`_:

.. code-block:: console

  $ cancelchain --env-file path/to/.env shell
  Python 3.10.11 (main, Apr  8 2023, 14:38:50) [GCC 11.3.0] on linux
  App: cancelchain
  Instance: /home/arlo/.pyenv/versions/3.10.11/envs/my-cancelchain/var/cancelchain-instance

By default, it is the directory ``$PREFIX/var/cancelchain-instance`` where ``$PREFIX`` is the prefix of the Python installation.

The following ``cancelchain`` command examples assume that the ``.env`` file is loaded by default.


Initialize
----------

Create a local database by running the `init command`_:

.. code-block:: console

  $ cancelchain init

The `CC_SQLALCHEMY_DATABASE_URI`_ value in the example configuration above specifies a `SQLite`_ database called ``cc.sqlite`` with a file path relative to the ``cancelchain`` `instance folder`_.


Import Data
-----------

Download the most recent export of `CancelChain data`_. This `JSON Lines`_ file is updated at every blockchain epoch (2016 blocks or approximately every two weeks).

Next, run the `import command`_, passing it the location of the downloaded file:

.. code-block:: console

  $ cancelchain import path/to/cancelchain.jsonl

This command could take a while to run depending on your computer and the number of blocks imported. A progress bar will display with estimated time remaining. You can run the ``import`` command multiple times and it will only import new blocks that are not yet in the database.


Run
---

You run the ``cancelchain`` application by issuing the ``cancelchain run`` command:

.. code-block:: console

  $ cancelchain run

Open `http://localhost:5000 <http://localhost:5000>`_ in a browser to explore the local copy of the blockchain.

Home (Current Chain) UI
^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://github.com/cancelchain/cancelchain/blob/7a4fab66dfe6026e56c79df3e147b1ecbdbb6158/readme-assets/browser-chain.png?raw=true
   :width: 500pt

Block UI
^^^^^^^^

.. image:: https://github.com/cancelchain/cancelchain/blob/7a4fab66dfe6026e56c79df3e147b1ecbdbb6158/readme-assets/browser-block.png?raw=true
   :width: 500pt

Transaction UI
^^^^^^^^^^^^^^

.. image:: https://github.com/cancelchain/cancelchain/blob/7a4fab66dfe6026e56c79df3e147b1ecbdbb6158/readme-assets/browser-txn.png?raw=true
   :width: 500pt

Running the ``cancelchain`` application also exposes a number of web service endpoints that comprise the communications layer of the blockchain. See the  `API Documentation`_ for much more information.

There are also many other ``cancelchain`` commands for interacting with the blockchain. See the `Command Line Interface Documentation`_ or run ``cancelchain --help``.


Joining The CancelChain Network
-------------------------------

The CancelChain is run by a permissioned network of nodes. A CancelChain instance requires `miller`_ or `transactor`_ role `API access`_ to a node in the network in order to have locally milled blocks or submitted transactions propagate to the official CancelChain.

`The Cancel Button`_ allows `reader`_ `API access`_ to any account that completes at least one transaction on the blockchain.

To enable this access:

  1) `Register for an account`_.
  2) Submit a successful transaction for any subject. Note that access won't be granted until the opposition or support transaction successfully completes.
  3) Note the address on the `Account`_ page (it's a string that starts and ends with ``CC``) and then click `Download Account Key`_ to download the account's key (`PEM`_) file.
  4) Create a directory called ``wallets`` (note the location) and copy the downloaded key file into it.
  5) Add the following settings to the ``.env`` configuration file (make sure to replace ``CCTheCancelButtonAddressCC`` with the address noted on the account page and ``/path/to/wallet`` with the path to the ``wallets`` directory created above):

.. code-block:: console

  CC_NODE_HOST=http://CCTheCancelButtonAddressCC@localhost:5000
  CC_PEERS=https://CCTheCancelButtonAddressCC@thecancelbutton.com
  CC_DEFAULT_COMMAND_HOST=https://CCTheCancelButtonAddressCC@thecancelbutton.com
  CC_WALLET_DIR=/path/to/wallets

See `Configuration Documentation`_ for more detailed information about these settings.

Restart the local instance to load the new configuration.

CancelChain `reader`_ access allows running the `sync command`_ to update the local instance chain data up to the most recent peer block data:

.. code-block:: console

  $ cancelchain sync

This command could take a while to run depending on your computer, internet access, and the number of blocks synchronized. A progress bar will display with estimated time remaining. You can run the ``sync`` command multiple times and it will only synchronize new blocks that are not yet in the database.

Reader access also allows querying data (e.g. subject counts and wallet balances) using the CLI. See `Command Line Interface Documentation`_ for more information.

If you would like to be granted other API access to a node in the CancelChain network, send an email to contact@cancelchain.org including what kind of access you'd like (e.g. `reader`_, `transactor`_, or `miller`_) and how you intend to use it (e.g. research, business, non-profit, hobby).

See the `documentation`_ for some potential development ideas.


.. _Account: https://thecancelbutton.com/account
.. _API Documentation: https://docs.cancelchain.org/en/latest/api.html
.. _API access: https://docs.cancelchain.org/en/latest/api.html#api-roles
.. _Blog: https://blog.cancelchain.org
.. _CancelChain data: https://storage.googleapis.com/blocks.cancelchain.org/cancelchain.jsonl
.. _CC_SECRET_KEY: https://docs.cancelchain.org/en/latest/usage.html#SECRET_KEY
.. _CC_SQLALCHEMY_DATABASE_URI: https://docs.cancelchain.org/en/latest/usage.html#SQLALCHEMY_DATABASE_URI
.. _Command Line Interface Documentation: https://docs.cancelchain.org/en/latest/usage.html#command-line-interface
.. _Configuration Documentation: https://docs.cancelchain.org/en/latest/usage.html#configuration
.. _documentation: https://docs.cancelchain.org
.. _Documentation: https://docs.cancelchain.org
.. _Download Account Key: https://thecancelbutton.com/pem
.. _import command: https://docs.cancelchain.org/en/latest/usage.html#import
.. _init command: https://docs.cancelchain.org/en/latest/usage.html#init
.. _instance folder: https://flask.palletsprojects.com/en/2.2.x/config/#instance-folders
.. _JSON Lines: https://jsonlines.org/
.. _miller: https://docs.cancelchain.org/en/latest/api.html#miller
.. _PEM: https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail
.. _Project Home Page: https://cancelchain.org
.. _python-dotenv: https://pypi.org/project/python-dotenv/
.. _python virtual environment: https://docs.python.org/3/library/venv.html
.. _reader: https://docs.cancelchain.org/en/latest/api.html#reader
.. _Register for an account: https://thecancelbutton.com/register
.. _running milling processes: https://docs.cancelchain.org/en/latest/usage.html#mill
.. _shell command: https://flask.palletsprojects.com/en/2.2.x/cli/#open-a-shell
.. _sock puppet accounts: https://en.wikipedia.org/wiki/Sock_puppet_account
.. _SQLite: https://sqlite.org/index.html
.. _sync command: https://docs.cancelchain.org/en/latest/usage.html#sync
.. _The Cancel Button: https://thecancelbutton.com
.. _transactor: https://docs.cancelchain.org/en/latest/api.html#transactor