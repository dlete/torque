
# OS
- Ubuntu 16.04


# Base
- Python 3
- Django 2
- MySQL or MariaDB (with or without Galera cluster)
- Apache2 + mod_wsgi


# Python packages
- junos-eznc 


# Django templates
Django Template Language (DTL) throught. Does not use Jinja2.


# API
- [Django REST Framework (DRF)](http://www.django-rest-framework.org/)
- [Django REST Swagger](https://github.com/marcgibbons/django-rest-swagger)

## API custom endpoints
Based on this article: [Django REST Framework - Create Endopoints for Custom Actions](https://eureka.ykyuen.info/2014/08/28/django-rest-framework-create-endpoints-for-custom-actions/)


# Project documentation
Markdown files in the `docs/` directory.


## Packages needed
See the installation instructions in `docs/installation.md`

- libmysqlclient-dev
- build-essential libssl-dev libffi-dev (otherwise, the Python package cryptography fails)
- libxml2-dev libxslt1-dev (otherwise, the Python package lxml fails)

# Optional packages
- graphviz
- git

# Decissions
The functionality of auditing resides in a collection of independent pure python scripts. A different approach could have been to make each of the auditing scripts a Ne method; e.g. Ne.audit_lldp(). The former was preferred over the later so that those scripts could be used by other means, people, uses, etc. For example, through CLI.
