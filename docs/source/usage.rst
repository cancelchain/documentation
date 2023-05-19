Usage
=====

Running A Node
--------------

A node consists of `deploying`_ and/or `running`_ the :ref:`CancelChain` flask application. The node must also have access to a `database`_ indicated with the required configuration value, :py:data:`SQLALCHEMY_DATABASE_URI`. The only other required setting is :py:data:`SECRET_KEY`. However, to allow the node to do useful work, additional configuration values are usually needed.

Most nodes will want to configure a :py:data:`WALLET_DIR` to contain wallets used for :ref:`API Authorization` with other nodes and/or to sign transactions.

The remote nodes that a local node will communicate with are defined using the configuration list :py:data:`PEERS`. Most nodes will want to indicate at least one peer with which to share new blocks and transactions.

Incoming authorized remote nodes are configured using the :py:data:`MILLER_ADDRESSES`, :py:data:`TRANSACTOR_ADDRESSES`, and :py:data:`READER_ADDRESSES` lists. See :ref:`API roles` for more information.

If at least one :py:data:`PEERS` entry is defined, the :py:data:`NODE_HOST` should also be configured to indicate the hostname and default wallet address of the local node.

In addition to exposing the :ref:`api` used for node-to-node communication, a simple web-based ledger data browser is also provided.

Database
--------

:ref:`CancelChain` requires a relational database and uses `Flask SQLAlchemy`_ to interact with it. Any `supported database`_ should work.

New databases must be initialized before running a node or miller using the `init`_ command:

    .. code:: console

        $ cancelchain init

Configuration
-------------

:ref:`CancelChain` can be configured like any other Flask_ application including a few custom options:

1. The environment variable :code:`CANCELCHAIN_SETTINGS` can be set to the location of a `python config file`_.
2. Most Flask and CancelChain settings can be configured from environment variables. CancelChain-specific environment variables are prefixed with ``CC_`` and are documented below. All other Flask-specific environment variables are prefixed with ``FLASK_`` and loaded with the built-in flask method, |from_prefixed_env()|_.


Dotenv
^^^^^^

Environment variables can be set using a `python-dotenv`_ ``.env`` file. A ``.env`` file is loaded by default if it is located either in the current working directory or in the `instance folder`_. Use the ``--env-file`` parameter to specify an alternate file path when running commands.

You can find the location of the `instance folder`_ by running the `shell command`_:

.. code-block:: console

  $ cancelchain --env-file path/to/.env shell
  Python 3.10.11 (main, Apr  8 2023, 14:38:50) [GCC 11.3.0] on linux
  App: cancelchain
  Instance: /home/arlo/.pyenv/versions/3.10.11/envs/my-cancelchain/var/cancelchain-instance

By default, it is the directory ``$PREFIX/var/cancelchain-instance`` where ``$PREFIX`` is the prefix of the Python installation.


Flask
^^^^^

All built-in `Flask Configuration`_ values can be set.

The following setting is required:

.. py:data:: SECRET_KEY

    This value can also be set using the environment variable ``FLASK_SECRET_KEY``.


Flask SQLAlchemy
^^^^^^^^^^^^^^^^

All `Flask SQLAlchemy Configuration`_ values can be set.

The following setting is required:

.. py:data:: SQLALCHEMY_DATABASE_URI

    This value can also be set using the environment variable ``FLASK_SQLALCHEMY_DATABASE_URI``.


Celery
^^^^^^

`Celery Task Queue`_ is used to optionally enable asynchronous processing of new blocks and transactions (desireable for nodes with many :py:data:`PEERS`).

All `Celery Configuration`_ values can be set.

The following setting is required to enable asynchronous processing of new blocks and transactions:

.. py:data:: CELERY_BROKER_URL

    This value can also be set using the environment variable ``FLASK_CELERY_BROKER_URL``.

    Default: ``None``

.. note::

    If you configure a `Celery Broker`_, :py:data:`API_ASYNC_PROCESSING` must also be ``True`` to enable asynchronous processing.

When running the `Celery worker server`_, set the `application`_ to ``cancelchain.tasks``:

    .. code:: console

        $ celery -A cancelchain.tasks worker

Flask Caching
^^^^^^^^^^^^^

All `Flask Caching Configuration`_ values can be set.

No settings are required, but the following has a default and can be configured via an environment variable:

.. py:data:: CACHE_TYPE

    This value can also be set using the environment variable ``FLASK_CACHE_TYPE``.

    Default: ``NullCache`` (i.e. no caching).

CancelChain
^^^^^^^^^^^

.. py:data:: PEERS

    The list of peer nodes that this node will forward blocks and transactions to and synchronize its chain with. Each peer not only defines its host URL but also the wallet address that should be used for authentication and authorization.

    A peer node is represented as a URL with the following format:

        ``https://WALLET_ADDRESS@HOST[:PORT]``

    The ``WALLET_ADDRESS`` should be an address that matches a wallet file (i.e. a `.pem` file) in the :py:data:`WALLET_DIR`. For the nodes to successfully communicate, the ``WALLET_ADDRESS`` must also be in the peer node's :py:data:`MILLER_ADDRESSES`, :py:data:`TRANSACTOR_ADDRESSES`, or :py:data:`READER_ADDRESSES` config lists. In addition, the ``WALLET_ADDRESS`` must have initiated at least one successful transaction so the peer node can access the ``WALLET_ADDRESS``'s public key for use in authentication.

    This value can also be set using the environment variable ``CC_PEERS`` with a list of of peers in `JSON array`_ format.

    Default: ``list()``

.. py:data:: NODE_HOST

    This node's host URL including wallet address component (see :py:data:`PEERS`). This will be the host URL/wallet address used to perform background processing on the node. In addition, the host URL (sans wallet address) is used to identify the node on the network.

    This value can also be set using the environment variable ``CC_NODE_HOST``.

    Default: ``None``

.. py:data:: API_CLIENT_TIMEOUT

    The timeout in seconds for calls using the API client.

    This value can also be set using the environment variable ``CC_API_CLIENT_TIMEOUT``.

    Default: ``10``

.. py:data:: API_ASYNC_PROCESSING

    A boolean indicating whether processing of incoming blocks and transactions should be handled asynchronously.

    This value can also be set using the environment variable ``CC_API_ASYNC_PROCESSING`` with a `JSON boolean`_ string (``true`` or ``false``). 

    Default: ``False``

    .. warning::

        If ``True``, :py:data:`CELERY_BROKER_URL` must also be configured or incoming blocks and transactions will not be processed.

.. py:data:: DEFAULT_COMMAND_HOST

    The default host URL (with optional auth wallet address (see :py:data:`PEERS`)) for CLI commands to use for API calls.

    This value can also be set using the environment variable ``CC_DEFAULT_COMMAND_HOST``.

    Default: ``None``

.. py:data:: WALLET_DIR

    The directory path where wallet (i.e. `.pem`) files are stored.

    This value can also be set using the environment variable ``CC_WALLET_DIR``.

    Default: ``None``

.. py:data:: ADMIN_ADDRESSES

    The list of wallet addresses and/or `regular expressions`_ that when matched and authenticated are granted the role of ``ADMIN``.  See :ref:`API Roles` for more information.

    This value can also be set using the environment variable ``CC_ADMIN_ADDRESSES`` with a list of wallet addresses in `JSON array`_ format.

    Default: ``list()``

.. py:data:: MILLER_ADDRESSES

    The list of wallet addresses and/or `regular expressions`_ that when matched and authenticated are granted the role of ``MILLER``.  See :ref:`API Roles` for more information.

    This value can also be set using the environment variable ``CC_MILLER_ADDRESSES`` with a list of wallet addresses in `JSON array`_ format.

    Default: ``list()``

.. py:data:: TRANSACTOR_ADDRESSES

    The list of wallet addresses and/or `regular expressions`_ that when matched and authenticated are granted the role of ``TRANSACTOR``.  See :ref:`API Roles` for more information.

    This value can also be set using the environment variable ``CC_TRANSACTOR_ADDRESSES`` with a list of wallet addresses in `JSON array`_ format.

    Default: ``list()``

.. py:data:: READER_ADDRESSES

    The list of wallet addresses and/or `regular expressions`_ that when matched and authenticated are granted the role of ``READER``.  See :ref:`API Roles` for more information.

    This value can also be set using the environment variable ``CC_READER_ADDRESSES`` with a list of wallet addresses in `JSON array`_ format.

    Default: ``list()``

Command Line Interface
----------------------

Administrative interactions with the :ref:`CancelChain` application are conducted through its `Command Line Interface`_ (CLI).

Usage:
    .. code:: console

        $ cancelchain [OPTIONS] COMMAND [ARGS]...

Options:
    --version  Show the version and exit.
    --help     Show the help message and exit.

:ref:`CancelChain` registers its own ``cancelchain`` command that can be used as a drop-in replacement for the standard ``flask`` `CLI`_ and inherits all of the built-in `Flask Command Line Interface`_ commands (e.g. ``run`` and ``shell``).

CLI Commands
------------

export
^^^^^^

Export the block chain to file.

Usage:
    .. code:: console

        $ cancelchain export FILE

Args:
    :FILE: The file path to export the blocks to. If the file already exists, it will be appended to.

import
^^^^^^

Import the block chain from file.

Usage:
    .. code:: console

        $ cancelchain import FILE

Args:
    :FILE: The file path from which to import the blocks.

A recent `JSON Lines`_ export of the CancelChain block data can be downloaded `here`_.

init
^^^^

Initialize the database.

Usage:
    .. code:: console

        $ cancelchain init

mill
^^^^

Start a milling process.

Usage:
    .. code:: console

        $ cancelchain mill [OPTIONS] ADDRESS

Args:
    :ADDRESS: The wallet address to use for milling coinbase rewards.

Options:
    -m, --multi           Use python multiprocessing when calculating hashes.
    -r, --rounds INTEGER  Number of rounds of milling between new block checks.
                          (default 1)
    -s, --size INTEGER    Number of hashes to calculate per round (per CPU if
                          multiprocessing is enabled) (default 100000)
    -w, --wallet PATH     Wallet file to use for milling coinbase rewards.
    -p, --peer TEXT       Peer node to poll before checking for new blocks and
                          transactions.
    -b, --blocks INTEGER  Stop after this many blocks. (default 0 (run forever))

.. note::

    Many CLI commands will make API calls to a :ref:`CancelChain` node. If the command's specified API `host` (or the default specified by :py:data:`DEFAULT_COMMAND_HOST`) does not specify a wallet address, or the CLI does not have access to the address' wallet (i.e. it is not in :py:data:`WALLET_DIR`), a `wallet` file **must** be specified for API auth.

subject-balance
^^^^^^^^^^^^^^^

Get the balance (i.e. subject transactions minus forgiveness transactions) in CCG for a subject.

Usage:
    .. code:: console

        $ cancelchain subject balance [OPTIONS] SUBJECT

Args:
    :SUBJECT: The raw (unencoded) subject string.

Options:
    -h, --host TEXT     The API host to use (default: :py:data:`DEFAULT_COMMAND_HOST`).
    -w, --wallet PATH   Wallet file to use for API auth.

subject-support
^^^^^^^^^^^^^^^

Get the support total in CCG for a subject.

Usage:
    .. code:: console

        $ cancelchain subject support [OPTIONS] SUBJECT

Args:
    :SUBJECT: The raw (unencoded) subject string.

Options:
    -h, --host TEXT     The API host to use (default: :py:data:`DEFAULT_COMMAND_HOST`).
    -w, --wallet PATH   Wallet file to use for API auth.

sync
^^^^

Synchronize the node's block chain to that of its peers.

Usage:
    .. code:: console

        $ cancelchain sync

txn-transfer
^^^^^^^^^^^^

Create and post a transfer transaction.

Usage:
    .. code:: console

        $ cancelchain txn transfer [OPTIONS] FROM_ADDRESS AMOUNT TO_ADDRESS

Args:
    :FROM_ADDRESS: The transaction source address.
    :AMOUNT: The amount (as a float) of CCG to transfer.
    :TO_ADDRESS: The transaction destination address.

Options:
  -t, --txn-wallet PATH  Wallet file to use for transaction source.
  -h, --host TEXT        The API host to use (default: :py:data:`DEFAULT_COMMAND_HOST`).
  -w, --wallet PATH      Wallet file to use for API auth.
  -y, --yes              Assume "yes" as answer to all prompts and run non-interactively.

txn-subject
^^^^^^^^^^^

Create and post a subject (i.e. "cancel") transaction.

Usage:
    .. code:: console

        $ cancelchain txn subject [OPTIONS] ADDRESS AMOUNT SUBJECT

Args:
    :ADDRESS: The transaction source address.
    :AMOUNT: The amount (as a float) of CCG to apply.
    :SUBJECT: The raw (unencoded) subject string.

Options:
  -t, --txn-wallet PATH  Wallet file to use for transaction source.
  -h, --host TEXT        The API host to use (default: :py:data:`DEFAULT_COMMAND_HOST`).
  -w, --wallet PATH      Wallet file to use for API auth.
  -y, --yes              Assume "yes" as answer to all prompts and run non-interactively.

txn-forgive
^^^^^^^^^^^

Create and post a forgiveness transaction.

Usage:
    .. code:: console

        $ cancelchain txn forgive [OPTIONS] ADDRESS AMOUNT SUBJECT

Args:
    :ADDRESS: The transaction source address.
    :AMOUNT: The amount (as a float) of CCG to apply.
    :SUBJECT: The raw (unencoded) subject string.

Options:
  -t, --txn-wallet PATH  Wallet file to use for transaction source.
  -h, --host TEXT        The API host to use (default: :py:data:`DEFAULT_COMMAND_HOST`).
  -w, --wallet PATH      Wallet file to use for API auth.
  -y, --yes              Assume "yes" as answer to all prompts and run non-interactively.

txn-support
^^^^^^^^^^^

Create and post a support transaction.

Usage:
    .. code:: console

        $ cancelchain txn support [OPTIONS] ADDRESS AMOUNT SUBJECT

Args:
    :ADDRESS: The transaction source address.
    :AMOUNT: The amount (as a float) of CCG to apply.
    :SUBJECT: The raw (unencoded) subject string.

Options:
  -t, --txn-wallet PATH  Wallet file to use for transaction source.
  -h, --host TEXT        The API host to use (default: :py:data:`DEFAULT_COMMAND_HOST`).
  -w, --wallet PATH      Wallet file to use for API auth.
  -y, --yes              Assume "yes" as answer to all prompts and run non-interactively.

validate
^^^^^^^^

Validate the node's block chain.

Usage:
    .. code:: console

        $ cancelchain validate

wallet-balance
^^^^^^^^^^^^^^

Get the wallet balance in CCG for an address.

Usage:
    .. code:: console

        $ cancelchain wallet balance [OPTIONS] ADDRESS

Args:
    :ADDRESS: The wallet address.

Options:
  -h, --host TEXT    The API host to use (default: :py:data:`DEFAULT_COMMAND_HOST`).
  -w, --wallet PATH  Wallet file to use for API auth.

wallet-create
^^^^^^^^^^^^^

Create a new wallet file.

Usage:
    .. code:: console

        $ cancelchain wallet create [OPTIONS]

Options:
  -d, --walletdir PATH  Parent directory for the wallet file (default: :py:data:`WALLET_DIR`).

Running A Miller
----------------

The :ref:`CancelChain` block milling is performed by a permissioned (i.e. private) network. If you are interested in joining the network, `email us`_.

.. note::

    CCG is not a cryptocurrency. By design, it has an inflationary, never-decreasing coinbase reward. It also lacks rewards for address-to-address transfers compared to large rewards for other ledger transactions. It is intended to have no value other than being a ticket for creating subject, forgiveness, and support transactions on the blockchain ledger.


.. _application: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#application
.. _Celery Broker: https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html
.. _Celery Configuration: https://docs.celeryq.dev/en/stable/userguide/configuration.html
.. _Celery Task Queue: https://docs.celeryproject.org/en/stable/index.html
.. _Celery worker server: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#running-the-celery-worker-server
.. _CLI: https://flask.palletsprojects.com/en/2.1.x/cli/
.. _deploying: https://flask.palletsprojects.com/en/2.1.x/deploying/
.. _email us: contact@cancelchain.org
.. _Flask Caching Configuration: https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching
.. _Flask Command Line Interface: https://flask.palletsprojects.com/en/2.1.x/cli/
.. _Flask Configuration: https://flask.palletsprojects.com/en/2.1.x/config/
.. _Flask SQLAlchemy Configuration: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
.. _Flask SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
.. _Flask: https://flask.palletsprojects.com/
.. |from_prefixed_env()| replace:: ``from_prefixed_env()``
.. _from_prefixed_env(): https://flask.palletsprojects.com/en/2.3.x/api/#flask.Config.from_prefixed_env
.. _here: https://storage.googleapis.com/blocks.cancelchain.org/cancelchain.jsonl
.. _instance folder: https://flask.palletsprojects.com/en/2.2.x/config/#instance-folders
.. _JSON array: https://www.w3schools.com/js/js_json_arrays.asp
.. _JSON boolean: https://json-schema.org/understanding-json-schema/reference/boolean.html
.. _JSON Lines: https://jsonlines.org/
.. _python config file: https://flask.palletsprojects.com/en/2.1.x/config/#configuring-from-python-files
.. _python-dotenv: https://pypi.org/project/python-dotenv/
.. _regular expressions: https://docs.python.org/3/library/re.html
.. _running: https://flask.palletsprojects.com/en/2.1.x/cli/#run-the-development-server
.. _shell command: https://flask.palletsprojects.com/en/2.2.x/cli/#open-a-shell
.. _supported database: https://docs.sqlalchemy.org/en/14/dialects/
