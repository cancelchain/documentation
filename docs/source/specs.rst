Specifications
==============

The CancelChain blockchain technical specification follows the `original bitcoin paper`_ at a high level with some significant modifications aimed at reducing its "electronic cash system" origins and instead focusing on its distributed ledger capabilities.

CancelChain uses proof-of-work to add blocks to the chain. Coinbase rewards are always 100 :term:`CCG <CCG>` and never halve.  This is to reduce token scarcity and make sure that there is always CCG available to purchase for :term:`sentiment transactions <Sentiment Transactions>`.

In addition to the coinbase reward, :term:`millers <Miller>` receive additional CCG compensation for adding :term:`sentiment transactions <Sentiment Transactions>` to a successfully milled block. Both :term:`subject transactions <Subject Transaction>` and :term:`forgiveness transactions <Forgiveness Transaction>` reward half of the transaction's assigned CCG to the miller. :term:`Support transactions <Support Transaction>` reward the full amount of the transaction's assigned CCG. :term:`Transfer transactions <Transfer Transaction>` reward no additional CCG to the miller in order to de-incentivize transfers. Millers are implicitly motivated to process transfer transactions by the fact that they should lead to the other types of transactions that do offer rewards.

Unlike the bitcoin protocol which specifies a binary representation of blocks and transactions for performance, CancelChain relies on :ref:`JSON and schemas <JSON Schemas>` for transmitting block and transaction data while utilizing an internal relational database representation for processing speed.

The ledger uses the :term:`Unspent Transaction Output (UTXO) <UTXO>` model to represent tokens in the blockchain.

The target block rate is one every 600 seconds (ten minutes) and the block hash target is recalculated every 2016 blocks.

A block can contain a maximum of 100 transactions and each transaction can contain a maximum of 50 :term:`transaction flows <Transaction Flow>`.

Users and their transactions are secured by 2048-bit RSA keys and identified by an address derived by hashing the public key, encoding into `Base58Check`_, and appending ``CC`` to the beginning and end.

Hashing is accomplished using `sha512`_ followed by `sha256`_.


.. _Base58Check: https://en.bitcoin.it/wiki/Base58Check_encoding
.. _original bitcoin paper: https://bitcoin.org/bitcoin.pdf
.. _sha256: https://en.wikipedia.org/wiki/SHA-2
.. _sha512: https://en.wikipedia.org/wiki/SHA-2
