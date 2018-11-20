====================================
Olist Technical Challenge - REST API
====================================

|Build Status| |Coverage Status|

This project is my solution to the `Olist's technical challenge`_.
It implements a REST API that receives call detail records
and calculates monthly bills for a given telephone number.

The project is deployed at https://olist-technical-challenge.herokuapp.com/.


API Documentation
=================

To see the API Documentation, access the URL of the project using the path :code:`/apidocs`,
for example :code:`http://localhost:5000/apidocs` or https://olist-technical-challenge.herokuapp.com/apidocs.


Usage Examples
==============

Receive Call Start Record
-------------------------

.. code:: bash

    curl -i -X POST https://olist-technical-challenge.herokuapp.com/api/v1/calls \
        -H 'Content-Type: application/json' \
        -d '{
            "call_id": 1,
            "destination": "10987654321",
            "id": 1,
            "source": "12345678901",
            "timestamp": "2018-11-20T15:20:12Z",
            "type": "start"
        }'

    HTTP/1.1 200 OK
    Connection: keep-alive
    Server: gunicorn/19.9.0
    Date: Tue, 20 Nov 2018 15:26:13 GMT
    Content-Type: application/json
    Content-Length: 27
    Via: 1.1 vegur

    {
      "message": "Success"
    }


Receive Call End Record
-------------------------

.. code:: bash

    curl -i -X POST https://olist-technical-challenge.herokuapp.com/api/v1/calls \
        -H 'Content-Type: application/json' \
        -d '{
            "call_id": 1,
            "id": 2,
            "timestamp": "2018-11-20T15:25:42Z",
            "type": "end"
        }'

    HTTP/1.1 200 OK
    Connection: keep-alive
    Server: gunicorn/19.9.0
    Date: Tue, 20 Nov 2018 15:26:43 GMT
    Content-Type: application/json
    Content-Length: 27
    Via: 1.1 vegur

    {
      "message": "Success"
    }


Get a Telephone Bill (without Period)
-------------------------------------

.. code:: bash

    curl -i -X GET https://olist-technical-challenge.herokuapp.com/api/v1/calls/12345678901

    HTTP/1.1 204 NO CONTENT
    Connection: keep-alive
    Server: gunicorn/19.9.0
    Date: Tue, 20 Nov 2018 15:30:32 GMT
    Content-Type: text/html; charset=utf-8
    Content-Length: 0
    Via: 1.1 vegur


Get a Telephone Bill (Specific Period)
--------------------------------------

.. code:: bash

    curl -i \
      -X GET https://olist-technical-challenge.herokuapp.com/api/v1/calls/99988526423/2018/3

    HTTP/1.1 200 OK
    Connection: keep-alive
    Server: gunicorn/19.9.0
    Date: Tue, 20 Nov 2018 15:38:01 GMT
    Content-Type: application/json
    Content-Length: 1159
    Via: 1.1 vegur

    {
        "calls": [
            {
                "call_start_date": "2017-12-11",
                "call_start_time": "15:07:13",
                "destination": "9933468278",
                "duration": "0h7min43s",
                "price": 0.99
            },
            {
                "call_start_date": "2017-12-12",
                "call_start_time": "04:57:13",
                "destination": "9933468278",
                "duration": "1h13min43s",
                "price": 1.26
            },
            {
                "call_start_date": "2017-12-12",
                "call_start_time": "15:07:58",
                "destination": "9933468278",
                "duration": "0h4min58s",
                "price": 0.72
            },
            {
                "call_start_date": "2017-12-12",
                "call_start_time": "21:57:13",
                "destination": "9933468278",
                "duration": "0h13min43s",
                "price": 0.54
            },
            {
                "call_start_date": "2017-12-12",
                "call_start_time": "22:47:56",
                "destination": "9933468278",
                "duration": "0h3min0s",
                "price": 0.36
            },
            {
                "call_start_date": "2017-12-13",
                "call_start_time": "21:57:13",
                "destination": "9933468278",
                "duration": "24h13min43s",
                "price": 86.94
            }
        ],
        "period": "2017-12",
        "subscriber": "99988526423"
    }


Development Instructions
========================

The instructions to install, run and test the project are already described in `Makefile <Makefile>`_.

.. include:: Makefile
    :code: make


Work Environment
================

.. csv-table::
    :stub-columns: 1
    :delim: |

    Operating system | Ubuntu Linux 18.04
    Text Editor/IDE | VS Code
    Language | Python (3.6.6)
    Web Framework | Flask (1.0.2)
    Libraries | apispec, flasgger, flask-marshmallow, flask-migrate, flask-sqlalchemy, marshmallow, marshmallow-sqlalchemy, python-dotenv, sqlalchemy-utils


Implementation Annotations
==========================

Database Model
--------------

Only one table is necessary for this application:

.. code:: sql

    CREATE TABLE call (
            id INTEGER NOT NULL,
            source VARCHAR(11),
            destination VARCHAR(11),
            start_timestamp TIMESTAMP,
            end_timestamp TIMESTAMP,
            price NUMERIC(10, 2),
            PRIMARY KEY (id)
    );
    CREATE INDEX call_idx1 ON call (source, end_timestamp);

This table holds information about complete calls,
that are filled by the application as it receives each call start/end record.
When both :code:`start_timestamp` and :code:`end_timestamp` are known,
the application automatically calculates the :code:`price` of the call.


Call Start/End Records API
--------------------------

Since the specification just says about receiving call records
but nothing about editing or deleting them,
there is only one endpoint and method for receiving (creating) call start and end records:
:code:`POST /api/v1/calls`.





.. |Build Status| image:: https://travis-ci.org/andredias/work-at-olist.svg?branch=master
    :target: https://travis-ci.org/andredias/work-at-olist
.. |Coverage Status| image:: https://coveralls.io/repos/github/andredias/work-at-olist/badge.svg?branch=master
    :target: https://coveralls.io/github/andredias/work-at-olist?branch=master

.. _Olist's technical challenge: work-at-olist-spec.md
