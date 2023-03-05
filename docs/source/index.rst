Welcome To CancelChain
======================

CancelChain is an open-source python project that implements a custom blockchain ledger. The ledger protocol allows for the assigning of tokens to :term:`subjects<Subject>` as indications of either opposition or support. Opposition entries are allowed to be rescinded later. Support is forever.


Motivations
-----------

Social media is not tailored to capture emergent sentiments. Although it enables individuals to participate directly, free-form human language is a poor tool for capturing quantifiable sentiment. Human language requires inherently biased and expensive machine learning algorithms to extract quantifiable data. Because of this, the sentiment data that does exist is "fuzzy" and owned exclusively by large tech companies.

Social media users often lack any meaningful stake in their posts because they are free. This increases noise in the data and encourages "pile-on" behavior that isn't necessarily an indicator of true sentiment.

Social media provides no formal and easily quantifiable way to indicate forgiveness.

This project aims to address this impedance mismatch between real, quantifiable sentiment and social media by providing a secure, publicly verifiable blockchain ledger of sentiments on a virtually infinite number of subjects (*approximately* 1,112,064\ :sup:`79`).


The Ledger
----------

The official CancelChain ledger is maintained by a :term:`permissioned network <Permissioned Network>` of block :term:`millers <Miller>` that also act as gatekeeper merchants for :term:`sentiment transactions<Sentiment Transactions>`. This private network of miller-merchants help to keep the cost of sentiment transactions consistent across the network. This consistency facilitates trust among decision-makers in trying to understand the intensity of group sentiment for a particular subject.

The use of a permissioned network of :term:`millers <Miller>` that agree to strict hashrate limits keep the environmental impacts negligible.

All millers agree to only use milled or rewarded :term:`CCG <CCG>` for the sole purpose of facilitating end-user sentiment transaction purchases in their own application or website.

The first user-facing portal to the official CancelChain ledger is `The Cancel Button`_.

If you are interested in joining the network as a miller-merchant, `email us`_. We are particularly interested in non-profits that would like to leverage user sentiment for fundraising (e.g. a "Cancel Cancer" campaign).

If you have an idea that has nothing to do with being a miller or merchant and would like to join the network, `email us`_.

Some potential ideas:

    * Advanced Statistics
        * Further tease out sentiment and detect `sock puppet accounts`_ or "pile on" effects.

    * Aggregation
        * CancelChain does not aggregate similar subjects (e.g. “cancer” and “Cancer” and “CANCER” are all different subjects while obviously referring to the same underlying subject).

    * Search
        * Neither the built-in CancelChain browser nor `The Cancel Button`_ allow for browsing subjects or fuzzy searches (i.e. exact subject string searches only).

    * Leaderboards
        * The CancelChain browser has no concept of a leaderboard and `The Cancel Button`_ has limited top-ten leaderboards for :term:`subject balances <Subject Balance>`, :term:`support balances <Support Balance>`, and :term:`forgiveness <Forgiveness Transaction>` totals.


Contact
-------

If you hate this project and think it will be the end of civilization, `email us`_.

If you are a fan of this project and have some ideas, `report an issue`_ or `submit a pull request`_. Yes, you can also `email us`_.

If all else fails, `email us`_.


.. toctree::
    :maxdepth: 4
    :caption: Documentation
    :hidden:

    install
    usage
    api
    specs
    glossary


.. _The Cancel Button: https://thecancelbutton.com
.. _email us: contact@cancelchain.org
.. _submit a pull request: https://github.com/cancelchain/cancelchain/pulls
.. _report an issue: https://github.com/cancelchain/cancelchain/issues
.. _sock puppet accounts: https://en.wikipedia.org/wiki/Sock_puppet_account
