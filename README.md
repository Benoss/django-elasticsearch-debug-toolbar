Django Elasticsearch Toolbar
======================

A Django Debug Toolbar panel for Elasticsearch

About
------------

This is a panel for `Django Debug Toolbar` 1.2+ that displays query results from
ElasticSearch using elasticsearch pyhon official client. [https://github.com/elasticsearch/elasticsearch-py](https://github.com/elasticsearch/elasticsearch-py)



Installation
------------

Install using ``pip``::

    pip install elasticsearch-django-debug-toolbar

or install the development version from source::

    pip install git+git@github.com:Benoss/elasticsearch-django-debug-toolbar.git

* Then add ``elastic_panel`` to your ``INSTALLED_APPS`` so that we can find the
templates in the panel. 
* Also, add ``'elastic_panel.panel.ElasticDebugPanel'`` to your ``DEBUG_TOOLBAR_PANELS``.

Usage
------------


License
------------

Uses the `MIT`_ license.


.. _Django Debug Toolbar: https://github.com/django-debug-toolbar/django-debug-toolbar
.. _MIT: http://opensource.org/licenses/MIT