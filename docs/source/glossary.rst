Glossary
========

.. glossary::
    :sorted:

    CCC
        **Cancel Chain Curmudgeon**: The smallest ledger token.

    CCG
        **CancelChain Grumble**: The user-facing ledger token. A CancelChain Grumble is equal to 100 :term:`CancelChain Curmudgeons<CCC>`. This is the token that users purchase and assign to subjects via :term:`Sentiment Transactions`.

    Subject
        A UTF-8 string of less than 80 characters.

    Miller
        An entity that adds transactions to the blockchain. Also known as a "miner" in traditional proof-of-work blockchains.

    Sentiment Transactions
        The primary type of blockchain transaction. There are three types of sentiment transactions: :term:`subject<Subject Transaction>` (a.k.a. "opposition"), :term:`support<Support Transaction>`, and :term:`forgiveness<Forgiveness Transaction>`. All three types require a :term:`subject` and an integer amount of :term:`CCG` to assign.

    Subject Transaction
        A :term:`sentiment transaction<Sentiment Transactions>` type that adds the requested amount of :term:`CCG` to the :term:`subject's<Subject>` :term:`Subject Balance`.

    Support Transaction
        A :term:`sentiment transaction<Sentiment Transactions>` that adds the requested amount of :term:`CCG` to the :term:`subject's<Subject>` :term:`Support Balance`.

    Forgiveness Transaction
        A :term:`sentiment transaction<Sentiment Transactions>` type that subtracts the requested amount of :term:`CCG` from the :term:`subject's<Subject>` :term:`Subject Balance`. A forgiveness transaction can only be created by a user that has already successfully submitted :term:`Subject Transactions<Subject Transaction>` for the given :term:`subject<Subject>`. The amount forgiven cannot be more than the total unforgiven :term:`CCG` assigned to the :term:`subject<Subject>` by the user.

    Transfer Transaction
        A blockchain transaction that transfers ledger tokens from one :term:`address<Address>` to another. Although necessary for the proper function of the blockchain, they are discouraged by providing no reward for the :term:`miller <Miller>`.

    Subject Balance
        The total amount of unforgiven :term:`CCG` that has been assigned to a :term:`subject<Subject>` via :term:`Subject Transactions<Subject Transaction>`.

    Support Balance
        The total amount of :term:`CCG` that has been assigned to a :term:`subject<Subject>` via :term:`Support Transactions<Support Transaction>`.

    Permissioned Network
        A private network maintained through mutual, exclusive permissions.

    Address
        An identity on the ledger. Starts and ends with ``CC``.

    Transaction Flow
        The :term:`UTXO` inputs and outputs of a transaction, referred to as "inflows" and "outflows." See `Bitcoin transactions`_ for more information.

    UTXO
        **Unspent Transaction Output**: The ledger model. See `Unspent transaction output`_ for a more formal definition.


.. _Bitcoin transactions: https://en.wikipedia.org/wiki/Bitcoin_network#Transactions
.. _Unspent transaction output: https://en.wikipedia.org/wiki/Unspent_transaction_output
