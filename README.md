Django Elasticsearch Toolbar
============================

A Django Debug Toolbar panel for Elasticsearch

About
------------

This is a panel for `Django Debug Toolbar` 1.2+ that displays query results from
ElasticSearch queries using [elasticsearch python](https://github.com/elasticsearch/elasticsearch-py) official client.

You are more than welcome to participate
* Any idea and no time to code send your idea here: https://github.com/Benoss/django-elasticsearch-debug-toolbar/issues
* An idea and the code just send a pull request here: https://github.com/Benoss/django-elasticsearch-debug-toolbar/pulls



Installation
------------

Install using ``pip``::

    pip install django-elasticsearch-debug-toolbar

or install the development version from source::

    pip install git+git@github.com:Benoss/django-elasticsearch-debug-toolbar.git

* Then add ``elastic_panel`` to your ``INSTALLED_APPS`` so that we can find the templates in the panel. 
* Also, add ``'elastic_panel.panel.ElasticDebugPanel'`` to your ``DEBUG_TOOLBAR_PANELS``.

Usage
------------

Just click the link in the Django Debug toolbar:

![elastic queries image](https://raw.github.com/Benoss/django-elasticsearch-debug-toolbar/master/doc/elastic_queries.png)

License
------------

Uses the `MIT` license.

* Django Debug Toolbar: https://github.com/django-debug-toolbar/django-debug-toolbar
* MIT: http://opensource.org/licenses/MIT

