API
===

The application exposes an API that can be used to:

* Read and write blocks and transactions.
* Create transactions.
* Submit transactions to the chain.
* Query balances.


API Authorization
-----------------

Authorization Token
^^^^^^^^^^^^^^^^^^^

`API Services`_ (with the exception of :http:get:`/api/token/(address)` and :http:post:`/api/token/(address)`) are authenticated by including an authorization `JSON Web Token`_ as a `Bearer Token`_ in the :http:header:`Authorization` header:

    **Example request**:

    .. code:: http

        GET /api/block HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

This short-lived authorization JWT is requested by calling the :http:get:`/api/token/(address)` endpoint.

.. http:get:: /api/token/(address)

    Returns a challenge cipher encrypted with `RSAES-OAEP`_ using the public key associated with `address` on the chain.

    **Example request**:

    .. code:: http

        GET /api/token/CC7AT7Fo7X5nbRnmGnUidBr2PhkyMP8fdS2Ety94SsKvWZCC HTTP/1.1

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {"cipher": "gNUID6pj2zNfr5vNWZbrv6oz6arsoHdvRWVu1dUbRQBj9p1+HvNuWMrYBJO8/s8PMgj4Dpm/hmWLbXVXIcMs76nhTlpev+JUzyIlhpwLqj5/9ReLeopiZL69mov7JH+vd0MN/lxtYEWRy2M52xb8QvPU/VbBgiXcG+pNgd9MkmkGqM6nr7EXAHhSN+N/zexEeZq8Aw2oG7tmhQgfVYx9pfLFCH++oxfG2xAyp5i2+oYUhfiBC9dVBRfKQmVZF1Ojgi6mh0H/eKf//oFS+PnFlDXqK05ePgs0FsIFRaHbakleFe4FfJhmR24owubyht2ZcTxTaAJO7AQJfkskLkhPgeA2zpkcdCFk/ZGFnQOkdY2j7Y0izSiVB3x+nlWY1+RSlXKskIrstZNjsu2YMH3ArGhjF7NWaBK4WV1odb+WbA+fWBA9"}

    :response: A challenge cipher.
    :>header Content-Type: ``application/json``
    :>json string cipher: The challenge cipher.
    :statuscode 200: Success.
    :statuscode 401: No public key for `address` found.
    :statuscode 404: Invalid `address`.

After the challenge cipher is decrypted using the private key associated with `address`, the :http:post:`/api/token/(address)` endpoint can be called with the result.

.. http:post:: /api/token/(address)

    Returns a short-lived authorization JWT if the request body JSON ``challenge`` element matches the unencrypted ``cipher`` provided by a recent call to :http:get:`/api/token/(address)`.

    **Example request**:

    .. code:: http

        POST /api/token/CC7AT7Fo7X5nbRnmGnUidBr2PhkyMP8fdS2Ety94SsKvWZCC HTTP/1.1
        Content-Type: application/json

        {"challenge": "df473df0-51a7-4865-a69d-ce62ea023d05"}

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU"}

    :<header Content-Type: ``application/json``
    :<json challenge: The decrypted ``cipher`` string.
    :>header Content-Type: ``application/json``
    :>json string token: The `Authorization Token`_.
    :statuscode 200: Success.
    :statuscode 400: Bad request.
    :statuscode 401: Expired or incorrect challenge.
    :statuscode 403: No `API Roles`_ for `address`.
    :statuscode 404: Invalid `address`.

API Roles
^^^^^^^^^

There are four different client API roles that control what API services/methods are authorized for a client of a node. If a client address is assigned to more than one role, the more expansive role will take precedence.

Reader
""""""

Client addresses that belong to the ``READER`` role can call most API services with the ``GET`` method. ``READER``-authorized clients can not call services with any other methods (e.g. ``POST``). The one exception to this rule is that they can call the :http:post:`/api/token/(address)` authentication function.

By disallowing the ``POST`` methods, clients with the ``READER`` role can not submit transactions or blocks. They can only query data.

Addresses can be assigned the ``READER`` role by adding them (or `regular expressions`_ that match the addresses) to the :py:data:`READER_ADDRESSES` configuration list.

Transactor
""""""""""

Client addresses that belong to the ``TRANSACTOR`` role can call most API services with the ``GET`` method. In addition, this role can ``POST`` new transactions. This is the role that transaction (but not block) generating peers should be assigned to.

Addresses can be assigned to the ``TRANSACTOR`` role by adding them (or `regular expressions`_ that match the addresses) to the :py:data:`TRANSACTOR_ADDRESSES` configuration list.

Miller
""""""

Client addresses that belong to the ``MILLER`` role can call most API services with either the ``GET`` or ``POST`` methods. This allows the API client to submit transactions and new blocks. This is the role that peer milling clients should be assigned to.

Addresses can be assigned to the ``MILLER`` role by adding them (or `regular expressions`_ that match the addresses) to the :py:data:`MILLER_ADDRESSES` configuration list.

Admin
"""""

Client addresses that belong to the ``ADMIN`` role can call all API services with either the ``GET`` or ``POST`` methods. This allows the API client to submit transactions and new blocks.

.. note::

    The ``ADMIN`` role is reserved for future use. The ``ADMIN`` role currently has the same permissions as the ``MILLER`` role which should be used instead.


API Services
------------

A node exposes several API services that provide the network layer of the blockchain. All services are authorized by including an `Authorization Token`_ as a `Bearer Token`_ in the :http:header:`Authorization` header.

Block Services
^^^^^^^^^^^^^^

.. http:get:: /api/block

    Returns the latest block of the longest chain.

    **Example request**:

    .. code:: http

        GET /api/block HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "idx": 6079,
            "timestamp": "2022-04-12T15:07:48Z",
            "block_hash": "000000039dce716d704f90d0264a3448786dd67d7586fb21d1643eee300a5d27",
            "prev_hash": "000000038d7e9c1881afe43c74765ad3501a6d83d4f3969c855c533d0d52a622",
            "target": "00000005bff4bb076c3280000000000000000000000000000000000000000000",
            "proof_of_work": 26749217,
            "merkle_root": "fce05f6c12e5f58de612e35cc2733af4b1e4f2fde90c92f3f634d9f0d9879913",
            "txns":
            [
                {
                    "timestamp": "2022-04-12T15:06:24Z",
                    "txid": "111e01606fe162cda80f2ff56dff97454246c8f75534574f2863782399bfeb7b",
                    "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC",
                    "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV/ZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a+1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn/bQq9K7de9Z8pifDQIDAQAB",
                    "signature": "Vl6N+AIdU8m7SFtisftM6WCgtZ6ZLc42PJxJwq7baW5Dsby2A4m1SsIHd4IHjh/YDGJp8LvjT14dJLH4yh0jOrvbpLxHad/nBtedeZF8fdwqvTBYozY/1Bqhze2uROAuqNjJBOIsT3xnWNonPlyaqVOjW0jRmA2HHWLeHsG6WXLsUrJk29BkmzXiqLEu6AxkSpcWtpDy/aWgLRE4DIVjGGcveT+g0h0aTFo+h8zVYXZVFEhiZkA5P+pkSCLAqvjT8TQpNV4xy/WNz1RugccNNPAnQJck5jd4jDpP/bq1AeheDV5dYzjdTjanlIee7iXJUALehDb1ZWkspeVEqq8/+w==",
                    "inflows":
                    [
                        {
                            "outflow_txid": "7cbc0b8aeee94dc7777af6e0a0f14a4b0617b6b25f9656cc7fbfafc7814e4934",
                            "outflow_idx": 1
                        }
                    ],
                    "outflows":
                    [
                        {
                            "amount": 200,
                            "subject": "Vm9nb24gUG9ldHJ5"
                        }
                    ],
                    "version": "1"
                },
                {
                    "timestamp": "2022-04-12T15:07:48Z",
                    "txid": "d0dc6c546227b1cd31bff4fdcc25ef003c6284d003021c297e4118775fdd2dac",
                    "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC",
                    "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmK5Qb4j6sKwcnCaVpS1JSMPX6IrNx4FkR8B3xh6ZmXFH5kGDGfRrSPwQdN18tAG9dv1AAr1uvLHc7pX3TucPppnm6JBaqzE6eaR3Y71kD+qrDdnOuGQhOmTpMg9zyC7Oo2QerHQfP67v14Jf6tnUORNivFGEbeuCCUHSvwJmP6ZrjXZiaRZEnQYgIio8537XqnkDj6jM4LKtqjz+tx8KOt24a71NaTeR/zjjD/sbKX5pw+dODP2ClsP+LEgY6gX4a6QYx8ANQlNCdu3nVtLyQX8OYjN4ROf3cWzBbpNmjIzyOr/yQUiCc1l+N1dMXkLud+AsiRV/7+LBQkQvCWCUxQIDAQAB",
                    "signature": "DYFvjj42MIcuNZWyqVl9ghkZ9xAi8U9ujGq50p4jnlYoY/MQXv4aDq0mTROv3nVnE5uGexQvicAbUlP3VBooQlskFxfMDaDw9X8EK2K6APZp6HzYA2xy0CaTiLshjWPFogcBTj3ZSAqQyyxqP52M7iuNbQCP4+hqvdn7tHOIp9ybLAVDNuyX5SpV+ZT3WayhlHnuC2BMTnbuEA3peugcuZQjv2H6O/xcoxA+MFYiitgWLZcZU3qECCwVtX7e0P1JmCp+UHEDTn8yZWqKOqUUyOTBXujzdEHl66Z2mVh/yqAZFe6l6aebuGoUb7Qq1afnBWTj4HRIM3HtBqzAqwzJSA==",
                    "inflows": [],
                    "outflows":
                    [
                        {
                            "amount": 10000,
                            "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC"
                        },
                        {
                            "amount": 100,
                            "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC"
                        }
                    ],
                    "version": "1"
                }
            ],
            "version": "1"
        }

    :Required Role: * `Reader`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :statuscode 200: Success.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 404: The block was not found.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :response: The `Block`_ JSON data.
    :>json error: Error messages.

.. http:get:: /api/block/(block_hash)

    Returns the block with the given `block_hash`.

    **Example request**:

    .. code:: http

        GET /api/block/000000039dce716d704f90d0264a3448786dd67d7586fb21d1643eee300a5d27 HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "idx": 6079,
            "timestamp": "2022-04-12T15:07:48Z",
            "block_hash": "000000039dce716d704f90d0264a3448786dd67d7586fb21d1643eee300a5d27",
            "prev_hash": "000000038d7e9c1881afe43c74765ad3501a6d83d4f3969c855c533d0d52a622",
            "target": "00000005bff4bb076c3280000000000000000000000000000000000000000000",
            "proof_of_work": 26749217,
            "merkle_root": "fce05f6c12e5f58de612e35cc2733af4b1e4f2fde90c92f3f634d9f0d9879913",
            "txns":
            [
                {
                    "timestamp": "2022-04-12T15:06:24Z",
                    "txid": "111e01606fe162cda80f2ff56dff97454246c8f75534574f2863782399bfeb7b",
                    "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC",
                    "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV/ZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a+1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn/bQq9K7de9Z8pifDQIDAQAB",
                    "signature": "Vl6N+AIdU8m7SFtisftM6WCgtZ6ZLc42PJxJwq7baW5Dsby2A4m1SsIHd4IHjh/YDGJp8LvjT14dJLH4yh0jOrvbpLxHad/nBtedeZF8fdwqvTBYozY/1Bqhze2uROAuqNjJBOIsT3xnWNonPlyaqVOjW0jRmA2HHWLeHsG6WXLsUrJk29BkmzXiqLEu6AxkSpcWtpDy/aWgLRE4DIVjGGcveT+g0h0aTFo+h8zVYXZVFEhiZkA5P+pkSCLAqvjT8TQpNV4xy/WNz1RugccNNPAnQJck5jd4jDpP/bq1AeheDV5dYzjdTjanlIee7iXJUALehDb1ZWkspeVEqq8/+w==",
                    "inflows":
                    [
                        {
                            "outflow_txid": "7cbc0b8aeee94dc7777af6e0a0f14a4b0617b6b25f9656cc7fbfafc7814e4934",
                            "outflow_idx": 1
                        }
                    ],
                    "outflows":
                    [
                        {
                            "amount": 200,
                            "subject": "Vm9nb24gUG9ldHJ5"
                        }
                    ],
                    "version": "1"
                },
                {
                    "timestamp": "2022-04-12T15:07:48Z",
                    "txid": "d0dc6c546227b1cd31bff4fdcc25ef003c6284d003021c297e4118775fdd2dac",
                    "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC",
                    "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmK5Qb4j6sKwcnCaVpS1JSMPX6IrNx4FkR8B3xh6ZmXFH5kGDGfRrSPwQdN18tAG9dv1AAr1uvLHc7pX3TucPppnm6JBaqzE6eaR3Y71kD+qrDdnOuGQhOmTpMg9zyC7Oo2QerHQfP67v14Jf6tnUORNivFGEbeuCCUHSvwJmP6ZrjXZiaRZEnQYgIio8537XqnkDj6jM4LKtqjz+tx8KOt24a71NaTeR/zjjD/sbKX5pw+dODP2ClsP+LEgY6gX4a6QYx8ANQlNCdu3nVtLyQX8OYjN4ROf3cWzBbpNmjIzyOr/yQUiCc1l+N1dMXkLud+AsiRV/7+LBQkQvCWCUxQIDAQAB",
                    "signature": "DYFvjj42MIcuNZWyqVl9ghkZ9xAi8U9ujGq50p4jnlYoY/MQXv4aDq0mTROv3nVnE5uGexQvicAbUlP3VBooQlskFxfMDaDw9X8EK2K6APZp6HzYA2xy0CaTiLshjWPFogcBTj3ZSAqQyyxqP52M7iuNbQCP4+hqvdn7tHOIp9ybLAVDNuyX5SpV+ZT3WayhlHnuC2BMTnbuEA3peugcuZQjv2H6O/xcoxA+MFYiitgWLZcZU3qECCwVtX7e0P1JmCp+UHEDTn8yZWqKOqUUyOTBXujzdEHl66Z2mVh/yqAZFe6l6aebuGoUb7Qq1afnBWTj4HRIM3HtBqzAqwzJSA==",
                    "inflows": [],
                    "outflows":
                    [
                        {
                            "amount": 10000,
                            "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC"
                        },
                        {
                            "amount": 100,
                            "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC"
                        }
                    ],
                    "version": "1"
                }
            ],
            "version": "1"
        }

    :Required Role: * `Reader`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :statuscode 200: Success.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 404: Invalid `block_hash` or the block was not found.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :response: The `Block`_ JSON data.
    :>json error: Error messages.

.. http:post:: /api/block/(block_hash)

    Submit a milled block.

    **Example request**:

    .. code:: http

        POST /api/block/000000039dce716d704f90d0264a3448786dd67d7586fb21d1643eee300a5d27 HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU
        Content-Type: application/json

        {
            "idx": 6079,
            "timestamp": "2022-04-12T15:07:48Z",
            "block_hash": "000000039dce716d704f90d0264a3448786dd67d7586fb21d1643eee300a5d27",
            "prev_hash": "000000038d7e9c1881afe43c74765ad3501a6d83d4f3969c855c533d0d52a622",
            "target": "00000005bff4bb076c3280000000000000000000000000000000000000000000",
            "proof_of_work": 26749217,
            "merkle_root": "fce05f6c12e5f58de612e35cc2733af4b1e4f2fde90c92f3f634d9f0d9879913",
            "txns":
            [
                {
                    "timestamp": "2022-04-12T15:06:24Z",
                    "txid": "111e01606fe162cda80f2ff56dff97454246c8f75534574f2863782399bfeb7b",
                    "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC",
                    "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV/ZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a+1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn/bQq9K7de9Z8pifDQIDAQAB",
                    "signature": "Vl6N+AIdU8m7SFtisftM6WCgtZ6ZLc42PJxJwq7baW5Dsby2A4m1SsIHd4IHjh/YDGJp8LvjT14dJLH4yh0jOrvbpLxHad/nBtedeZF8fdwqvTBYozY/1Bqhze2uROAuqNjJBOIsT3xnWNonPlyaqVOjW0jRmA2HHWLeHsG6WXLsUrJk29BkmzXiqLEu6AxkSpcWtpDy/aWgLRE4DIVjGGcveT+g0h0aTFo+h8zVYXZVFEhiZkA5P+pkSCLAqvjT8TQpNV4xy/WNz1RugccNNPAnQJck5jd4jDpP/bq1AeheDV5dYzjdTjanlIee7iXJUALehDb1ZWkspeVEqq8/+w==",
                    "inflows":
                    [
                        {
                            "outflow_txid": "7cbc0b8aeee94dc7777af6e0a0f14a4b0617b6b25f9656cc7fbfafc7814e4934",
                            "outflow_idx": 1
                        }
                    ],
                    "outflows":
                    [
                        {
                            "amount": 200,
                            "subject": "Vm9nb24gUG9ldHJ5"
                        }
                    ],
                    "version": "1"
                },
                {
                    "timestamp": "2022-04-12T15:07:48Z",
                    "txid": "d0dc6c546227b1cd31bff4fdcc25ef003c6284d003021c297e4118775fdd2dac",
                    "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC",
                    "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmK5Qb4j6sKwcnCaVpS1JSMPX6IrNx4FkR8B3xh6ZmXFH5kGDGfRrSPwQdN18tAG9dv1AAr1uvLHc7pX3TucPppnm6JBaqzE6eaR3Y71kD+qrDdnOuGQhOmTpMg9zyC7Oo2QerHQfP67v14Jf6tnUORNivFGEbeuCCUHSvwJmP6ZrjXZiaRZEnQYgIio8537XqnkDj6jM4LKtqjz+tx8KOt24a71NaTeR/zjjD/sbKX5pw+dODP2ClsP+LEgY6gX4a6QYx8ANQlNCdu3nVtLyQX8OYjN4ROf3cWzBbpNmjIzyOr/yQUiCc1l+N1dMXkLud+AsiRV/7+LBQkQvCWCUxQIDAQAB",
                    "signature": "DYFvjj42MIcuNZWyqVl9ghkZ9xAi8U9ujGq50p4jnlYoY/MQXv4aDq0mTROv3nVnE5uGexQvicAbUlP3VBooQlskFxfMDaDw9X8EK2K6APZp6HzYA2xy0CaTiLshjWPFogcBTj3ZSAqQyyxqP52M7iuNbQCP4+hqvdn7tHOIp9ybLAVDNuyX5SpV+ZT3WayhlHnuC2BMTnbuEA3peugcuZQjv2H6O/xcoxA+MFYiitgWLZcZU3qECCwVtX7e0P1JmCp+UHEDTn8yZWqKOqUUyOTBXujzdEHl66Z2mVh/yqAZFe6l6aebuGoUb7Qq1afnBWTj4HRIM3HtBqzAqwzJSA==",
                    "inflows": [],
                    "outflows":
                    [
                        {
                            "amount": 10000,
                            "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC"
                        },
                        {
                            "amount": 100,
                            "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC"
                        }
                    ],
                    "version": "1"
                }
            ],
            "version": "1"
        }

    **Example response**:

    .. code:: http

        HTTP/1.1 201 CREATED
        Content-Type: application/json

        {"received": "2022-04-12T15:13:56Z"}

    :Required Role: * `Miller`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :<header Content-Type: ``application/json``
    :Request Body: The `Block`_ JSON data.
    :statuscode 200: The block already exists.
    :statuscode 201: The block has been received and processed.
    :statuscode 202: The block has been received and will be processed.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 404: Invalid `block_hash` or the posted block's previous block was not found. The node can not add the block to any of its chains.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :>json received: The ISO8601 timestamp at which the block was received.
    :>json error: Error messages.

Transaction Services
^^^^^^^^^^^^^^^^^^^^

.. http:get:: /api/transaction/transfer

    Get an unsigned transfer transaction.

    **Example request**:

    .. code:: http

        GET /api/transaction/transfer?public_key=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV%2FZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a%2B1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn%2FbQq9K7de9Z8pifDQIDAQAB&amount=200&address=CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "timestamp": "2022-04-12T16:05:07Z",
            "txid": "9c40a8a46214d85abc883ccc6e89789be637353e047b363b234665916e2de116",
            "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV/ZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a+1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn/bQq9K7de9Z8pifDQIDAQAB",
            "inflows":
            [
                {
                    "outflow_txid": "649ec09329a21306b1c0509c0610274f395d72eb19c5f67a7add15d4beec264c",
                    "outflow_idx": 1
                }
            ],
            "outflows":
            [
                {
                    "amount": 200,
                    "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC"
                }
            ],
            "version": "1"
        }

    :Required Role: * `Transactor`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :query public_key: The public key of the source address.
    :query amount: The amount of CCC to transfer from the source address to the destination address.
    :query address: The destination address.
    :statuscode 200: The unsigned transaction was successfully created.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :response: The unsigned `Transaction`_ JSON data.
    :>json error: Error messages.

.. http:get:: /api/transaction/subject

    Get an unsigned subject ("cancel") transaction.

    **Example request**:

    .. code:: http

        GET /api/transaction/subject?public_key=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV%2FZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a%2B1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn%2FbQq9K7de9Z8pifDQIDAQAB&amount=100&subject=Vogon+Poetry HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "timestamp": "2022-04-12T16:33:03Z",
            "txid": "10518a73e85d0cba82496212fa85ee21729e2cb09d6db73f224f380e1113f4b5",
            "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV/ZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a+1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn/bQq9K7de9Z8pifDQIDAQAB",
            "inflows":
            [
                {
                    "outflow_txid": "649ec09329a21306b1c0509c0610274f395d72eb19c5f67a7add15d4beec264c",
                    "outflow_idx": 1
                }
            ],
            "outflows":
            [
                {
                    "amount": 100,
                    "subject": "Vm9nb24gUG9ldHJ5"
                },
                {
                    "amount": 100,
                    "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC"
                }
            ],
            "version": "1"
        }

    :Required Role: * `Transactor`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :query public_key: The public key of the source address.
    :query amount: The amount of CCC to apply to the subject.
    :query subject: The raw (unencoded) subject string.
    :statuscode 200: The unsigned transaction was successfully created.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :response: The unsigned `Transaction`_ JSON data.
    :>json error: Error messages.

.. http:get:: /api/transaction/forgive

    Get an unsigned forgive transaction.

    **Example request**:

    .. code:: http

        GET /api/transaction/forgive?public_key=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV%2FZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a%2B1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn%2FbQq9K7de9Z8pifDQIDAQAB&amount=100&subject=Vogon+Poetry HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "timestamp": "2022-04-12T17:04:26Z",
            "txid": "ee0d2dc269c1a33eb63f3c0d9fc7de5d1890aafa981cc83eb3d5aa3de8fc3a7e",
            "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV/ZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a+1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn/bQq9K7de9Z8pifDQIDAQAB",
            "inflows":
            [
                {
                    "outflow_txid": "6944c502a49db47918756ad9c3f1086c0c7ab17367ddf95cfae72f5fd4cc3c22",
                    "outflow_idx": 0
                }
            ],
            "outflows":
            [
                {
                    "amount": 100,
                    "forgive": "Vm9nb24gUG9ldHJ5"
                },
                {
                    "amount": 400,
                    "subject": "Vm9nb24gUG9ldHJ5"
                }
            ],
            "version": "1"
        }

    :Required Role: * `Transactor`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :query public_key: The public key of the source address.
    :query amount: The amount of CCC to forgive the subject.
    :query subject: The raw (unencoded) subject string.
    :statuscode 200: The unsigned transaction was successfully created.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :response: The unsigned `Transaction`_ JSON data.
    :>json error: Error messages.

.. http:get:: /api/transaction/support

    Get an unsigned support transaction.

    **Example request**:

    .. code:: http

        GET /api/transaction/support?public_key=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV%2FZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a%2B1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn%2FbQq9K7de9Z8pifDQIDAQAB&amount=100&subject=Towel HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "timestamp": "2022-04-12T17:15:04Z",
            "txid": "79b2bc3a23a8b9fe6bf7c36f21c60cf9b220429beed2f2be28792604ad3e2dd8",
            "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV/ZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a+1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn/bQq9K7de9Z8pifDQIDAQAB",
            "inflows":
            [
                {
                    "outflow_txid": "649ec09329a21306b1c0509c0610274f395d72eb19c5f67a7add15d4beec264c",
                    "outflow_idx": 1
                }
            ],
            "outflows":
            [
                {
                    "amount": 100,
                    "support": "VG93ZWw"
                },
                {
                    "amount": 100,
                    "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC"
                }
            ],
            "version": "1"
        }

    :Required Role: * `Transactor`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :query public_key: The public key of the source address.
    :query amount: The amount of CCC to support the subject.
    :query subject: The raw (unencoded) subject string.
    :statuscode 200: The unsigned transaction was successfully created.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :response: The unsigned `Transaction`_ JSON data.
    :>json error: Error messages.

.. http:post:: /api/transaction/(txid)

    Submit a complete (signed) transaction.

    **Example request**:

    .. code:: http

        POST /api/transaction/111e01606fe162cda80f2ff56dff97454246c8f75534574f2863782399bfeb7b HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU
        Content-Type: application/json

        {
            "timestamp": "2022-04-12T15:06:24Z",
            "txid": "111e01606fe162cda80f2ff56dff97454246c8f75534574f2863782399bfeb7b",
            "address": "CCDNF5ybECTLcTkaHAtxzTtgkyu4X6hBZETgez6xJygVZ4CC",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlB8JV/ZuTX9CTAw182QUzSfTYbJ9AzpFyFjqpxn3piniqYwA4wGbzSpVSt8GrZ0agwRFuF9OpnQXawn28i3n2bTlF1MB130v1C9AH3sHAaRfz6kdQP553e5jKkbLsK1pxgaEMAd5i9lkbXP3LV0QVdmDV6IGb6MGpxRENjyVXAZOxLfBht5ACboHnLpS6QYZTIfY5luqeeQsrqasxHA6mRMR1xo5a+1KJE0TZvfFyibqg3g4nUU3aC7n6jxcb9fDAXe5OixzfrKQt0lF1oDVzg9B3WnogvJI9uYttnn0zUPzGDR4XIqgFqAVtC4azKZnqWegn/bQq9K7de9Z8pifDQIDAQAB",
            "signature": "Vl6N+AIdU8m7SFtisftM6WCgtZ6ZLc42PJxJwq7baW5Dsby2A4m1SsIHd4IHjh/YDGJp8LvjT14dJLH4yh0jOrvbpLxHad/nBtedeZF8fdwqvTBYozY/1Bqhze2uROAuqNjJBOIsT3xnWNonPlyaqVOjW0jRmA2HHWLeHsG6WXLsUrJk29BkmzXiqLEu6AxkSpcWtpDy/aWgLRE4DIVjGGcveT+g0h0aTFo+h8zVYXZVFEhiZkA5P+pkSCLAqvjT8TQpNV4xy/WNz1RugccNNPAnQJck5jd4jDpP/bq1AeheDV5dYzjdTjanlIee7iXJUALehDb1ZWkspeVEqq8/+w==",
            "inflows":
            [
                {
                    "outflow_txid": "7cbc0b8aeee94dc7777af6e0a0f14a4b0617b6b25f9656cc7fbfafc7814e4934",
                    "outflow_idx": 1
                }
            ],
            "outflows":
            [
                {
                    "amount": 200,
                    "subject": "Vm9nb24gUG9ldHJ5"
                }
            ],
            "version": "1"
        }

    **Example response**:

    .. code:: http

        HTTP/1.1 201 CREATED
        Content-Type: application/json

        {"received": "2022-04-12T16:28:01Z"}

    :Required Role: * `Transactor`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :<header Content-Type: ``application/json``
    :Request Body: The `Transaction`_ JSON data.
    :statuscode 200: The transaction already exists.
    :statuscode 201: The transaction has been received and processed.
    :statuscode 202: The transaction has been received and will be processed.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :>json received: The ISO8601 timestamp at which the transaction was received.
    :>json error: Error messages.

.. http:get:: /api/transaction/pending

    Get pending transactions.

    **Example request**:

    .. code:: http

        GET /api/transaction/pending?earliest=20220415T041537Z HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "timestamp": "2022-04-15T04:20:32Z",
                "txid": "1c95010b33468d720d579ecee95f9830cd93b7fd2b08d71e91e5471e4655267d",
                "address": "CCFGYFvC9LmMH4bRqC2U5e9HTWbz4sAMKDcU3jX7XKLbHwCC",
                "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt3kxpLXrgJccMOAUqNyDAP2zxeAb5rSojkYRSgRUN1YTlbpItHMRclg961uRFNZM8fCghnux9zRjOGg8UxTlftGXq0B4y5Xja3M+uOSVHO5EuLHgxrMqRm8Hz+3WNSvOYoLInTKvgEAQPL45QjREsB+O3Db9mb2WnRbghbS0Fn1vhhwrd8MVaSMy+xVe9+u+cZYrGfE7SqHdgRczDEJIGi+unTfvGN8bFQHosuVSApX8KWn0juTxhsgmBlZ1u8XcfSVZk7/OtRQ+h29YAYm/K5za+MHJpqWEAddMZirBnvi81facsWAbAFtNLtuVVBluNxWGCs80t4Dw8VtpR7XN+wIDAQAB",
                "signature": "oK7uEW1EPus8ysdHZgUlExf7cxXifpQJ2vvCERgIMACwiL/ARwkBbfrYqoKzt1akxBHSt+8B3xaKEedcSKLbWCb0z0k/w99bJBr1AVAoHovjEMQq5DWoz/oPpMtkUevSIuCET47LJpGKm94j1R1CSVq+Xq/9WAeKK2J2fIN/62vrdNBKLWZTYdVZ5Ed22pLptSHe2t7xc1EBB8xCGMxOomGBk4iInM/hNydfh31KdeMtQzw/Jnimr4OAJu5YvBxh0sr3kFrFfLXje+akT4YYblPWadvyFhVOoDyY9vDmCPEzvJPpHtRb7GiNrkfDtbTL1LX+KOa6cfRNIyzrLWgpbQ==",
                "inflows": [
                    {
                        "outflow_txid": "908a8c102cb84a93242a71d904f3853a66e800c8c158db33c00b0d939feb68a8",
                        "outflow_idx": 0
                    }
                ],
                "outflows": [
                    {"amount": 100, "support": "VG93ZWw"},
                    {"amount": 400, "address": "CCFGYFvC9LmMH4bRqC2U5e9HTWbz4sAMKDcU3jX7XKLbHwCC"}
                ],
                "version": "1"
            },
            {
                "timestamp": "2022-04-15T04:24:13Z",
                "txid": "c51f33a0b6057750ec7fee3ad46a880f59032f9e8e0724c0456ccb020ed3b5da",
                "address": "CCFGYFvC9LmMH4bRqC2U5e9HTWbz4sAMKDcU3jX7XKLbHwCC",
                "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt3kxpLXrgJccMOAUqNyDAP2zxeAb5rSojkYRSgRUN1YTlbpItHMRclg961uRFNZM8fCghnux9zRjOGg8UxTlftGXq0B4y5Xja3M+uOSVHO5EuLHgxrMqRm8Hz+3WNSvOYoLInTKvgEAQPL45QjREsB+O3Db9mb2WnRbghbS0Fn1vhhwrd8MVaSMy+xVe9+u+cZYrGfE7SqHdgRczDEJIGi+unTfvGN8bFQHosuVSApX8KWn0juTxhsgmBlZ1u8XcfSVZk7/OtRQ+h29YAYm/K5za+MHJpqWEAddMZirBnvi81facsWAbAFtNLtuVVBluNxWGCs80t4Dw8VtpR7XN+wIDAQAB",
                "signature": "RCC0qYRqRapcSMLSzvQa7ihtqpQZkNZvEJerSAfkT6WKBdVIuQ6gr4xK9AcZ2CxRkuBZIc2Hcz2bCEWSnTT0MXOMZGe24NhLQQo+gK2KxWN+JMTDCu7lWx7GaBN2WwEGxMzSXCS1qU12y3Ji8ovX3YYRTgh1fD4E0sG9aaYp8N7/cIHgSJg4qWgxWBxcm+0nzzC3DhptdmxjtegMtCzcrb/0bZfFigvzLPZGVZcYi3Zy1t6t2jF1+qThaJte5NCwy2+Au/4LHpBopIOghFt4cgOJROQuHEsg/x+ahVhzbupQ504vfswpXQkBW9d5xbmRN/RhK5lgKUg91qQdC4Jh0g==",
                "inflows": [
                    {
                        "outflow_txid": "908a8c102cb84a93242a71d904f3853a66e800c8c158db33c00b0d939feb68a8",
                        "outflow_idx": 0
                    }
                ],
                "outflows": [
                    {"amount": 100, "subject": "Vm9nb24gUG9ldHJ5"},
                    {"amount": 400, "address": "CCFGYFvC9LmMH4bRqC2U5e9HTWbz4sAMKDcU3jX7XKLbHwCC"}
                ],
                "version": "1"
            },
            {
                "timestamp": "2022-04-15T04:26:19Z",
                "txid": "eae076dced7412a4f951d9dc0b1d2d5786407c38dcf039bedb809e071f1f3fcc",
                "address": "CCFGYFvC9LmMH4bRqC2U5e9HTWbz4sAMKDcU3jX7XKLbHwCC",
                "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt3kxpLXrgJccMOAUqNyDAP2zxeAb5rSojkYRSgRUN1YTlbpItHMRclg961uRFNZM8fCghnux9zRjOGg8UxTlftGXq0B4y5Xja3M+uOSVHO5EuLHgxrMqRm8Hz+3WNSvOYoLInTKvgEAQPL45QjREsB+O3Db9mb2WnRbghbS0Fn1vhhwrd8MVaSMy+xVe9+u+cZYrGfE7SqHdgRczDEJIGi+unTfvGN8bFQHosuVSApX8KWn0juTxhsgmBlZ1u8XcfSVZk7/OtRQ+h29YAYm/K5za+MHJpqWEAddMZirBnvi81facsWAbAFtNLtuVVBluNxWGCs80t4Dw8VtpR7XN+wIDAQAB",
                "signature": "WCHBQ/mM2apUCJ+ao7ZXOo3bt8z7GCwEZKgUIPqOn7j2pfKwg2mjgFjKX4pf2kgJ1ZAxVImaBJZSP4JoVWVSEmnrdE4pclg4IeYA9fDhWTJqoJ1YxqxIgrYBrq7Hqth6f1kdWEctZQrg7hdXRau5mT7l9PwKusUKlt+ktVzaaijD3Lnr6pTY1miEPFsPiYPG7kgvWzm1glrPmKU62E9LKqJl6Pca5vayn/1+3VgLGqA/evznLcr2MgJea442WDcva0L3GGE7Wo+LFeCreno819/sWI0jGK0z3zUK7gWU1FojB0v07FdUu6jFdTYSrBTLUR5zHVN7TMWYT4Nd+JtV3g==",
                "inflows": [
                    {
                        "outflow_txid": "908a8c102cb84a93242a71d904f3853a66e800c8c158db33c00b0d939feb68a8",
                        "outflow_idx": 0
                    }
                ],
                "outflows": [
                    {"amount": 100, "address": "CCCDwzcN5sNSyH5rTjj4mEPLSSDEb6Vz356e3YGMuWT4roCC"},
                    {"amount": 400, "address": "CCFGYFvC9LmMH4bRqC2U5e9HTWbz4sAMKDcU3jX7XKLbHwCC"}
                ],
                "version": "1"
            }
        ]

    :Required Role: * `Reader`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :query earliest: (Optional) Only return pending transactions received by the node since this timestamp (provided in compact ISO8601 format (``yyyymmddThhmmssZ``)). If not provided, all valid pending transactions will be returned.
    :statuscode 200: Success.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :response: A JSON list of pending `Transaction`_ data.
    :>json error: Error messages.

.. http:get:: /wallet/(address)/balance

    Get the balance in CCC for `address`.

    **Example request**:

    .. code:: http

        GET /api/wallet/CCFGYFvC9LmMH4bRqC2U5e9HTWbz4sAMKDcU3jX7XKLbHwCC/balance HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "balance": 100,
            "as_of_block": "000000039dce716d704f90d0264a3448786dd67d7586fb21d1643eee300a5d27"
        }

    :Required Role: * `Reader`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :statuscode 200: Success.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 404: Invalid `address`.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :>json balance: The wallet balance in CCC.
    :>json as_of_block: The latest block's hash used to calculate the balance.
    :>json error: Error messages.

.. http:get:: /subject/(subject)/balance

    Get the balance (i.e. subject transactions minus forgiveness transactions) in CCC for the (encoded) `subject`.

    **Example request**:

    .. code:: http

        GET /api/subject/Vm9nb24gUG9ldHJ5/balance HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "balance": 300,
            "as_of_block": "000000039dce716d704f90d0264a3448786dd67d7586fb21d1643eee300a5d27"
        }

    :Required Role: * `Reader`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :statuscode 200: Success.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 404: Invalid `subject` encoding.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :>json balance: The subject balance in CCC.
    :>json as_of_block: The latest block's hash used to calculate the balance.
    :>json error: Error messages.

.. http:get:: /subject/(subject)/support

    Get the support total in CCC for the (encoded) `subject`.

    **Example request**:

    .. code:: http

        GET /api/subject/Vm9nb24gUG9ldHJ5/balance HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmb28ifQ.PCYPJkVZfox0jxt9jWJ44DJaQZ4-d2lnAMzvfLx9mXU

    **Example response**:

    .. code:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "support": 1200,
            "as_of_block": "000000039dce716d704f90d0264a3448786dd67d7586fb21d1643eee300a5d27"
        }

    :Required Role: * `Reader`_
    :<header Authorization: An `Authorization Token`_ as a `Bearer Token`_.
    :statuscode 200: Success.
    :statuscode 400: Bad request. See the Response JSON Object `error` property for messages.
    :statuscode 401: Unauthorized.
    :statuscode 404: Invalid `subject` encoding.
    :statuscode 500: Server error.
    :>header Content-Type: ``application/json``
    :>json support: The support total in CCC.
    :>json as_of_block: The latest block's hash used to calculate the support total.
    :>json error: Error messages.


JSON Schemas
^^^^^^^^^^^^

Block
"""""

.. jsonschema::

    {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "idx": {
                "type": "integer",
                "minimum": 0
            },
            "timestamp": {
                "type": "date-time"
            },
            "block_hash": {
                "type": "string",
                "minLength": 64,
                "maxLength": 64
            },
            "prev_hash": {
                "type": "string",
                "minLength": 64,
                "maxLength": 64
            },
            "target": {
                "type": "string",
                "minLength": 64,
                "maxLength": 64
            },
            "proof_of_work": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "merkle_root": {
                "type": "string",
                "minLength": 64,
                "maxLength": 64
            },
            "txns": {
                "type": "array",
                "items": {
                    "title": "Transaction"
                }
            },
            "version": {
                "type": "string",
                "pattern": "^[1]$"
            }
        },
        "required": [
            "idx", "timestamp", "block_hash", "prev_hash", "target",
            "proof_of_work", "merkle_root", "txns", "version"
        ]
    }

Transaction
"""""""""""

.. jsonschema::

    {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "timestamp": {
                "type": "date-time"
            },
            "txid": {
                "type": "string",
                "minLength": 64,
                "maxLength": 64
            },
            "address": {
                "type": "string"
            },
            "public_key": {
                "type": "string"
            },
            "signature": {
                "type": "string"
            },
            "inflows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "title": "Inflow",
                    "properties": {
                        "outflow_txid": {
                            "type": "string",
                            "minLength": 64,
                            "maxLength": 64
                        },
                        "outflow_index": {
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": ["outflow_txid", "outflow_index"]
                }
            },
            "outflows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "title": "Outflow",
                    "properties": {
                        "amount": {
                            "type": "integer",
                            "minimum": 1
                        },
                        "address": {
                            "type": "string"
                        },
                        "subject": {
                            "type": "string",
                            "minLength": 1
                        },
                        "forgive": {
                            "type": "string",
                            "minLength": 1
                        },
                        "support": {
                            "type": "string",
                            "minLength": 1
                        }
                    },
                    "required": ["amount"]
                }
            },
            "version": {
                "type": "string",
                "pattern": "^[1]$"
            }
        },
        "required": [
            "timestamp", "txid", "address", "public_key", "signature",
            "outflows", "version"
        ]
    }

(Properties in **bold** are required.)


.. _JSON Web Token: https://datatracker.ietf.org/doc/html/rfc7519
.. _Bearer Token: https://datatracker.ietf.org/doc/html/rfc6750
.. _RSAES-OAEP: https://datatracker.ietf.org/doc/html/rfc8017#section-7.1
.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
.. _regular expressions: https://docs.python.org/3/library/re.html
