These are my bits and pieces.

Investigate
===========

Choices in a Model 
------------------
Ref: https://docs.djangoproject.com/en/1.11/ref/models/fields/#choices
Could this be used as a way to have "settings" page? e.g. choices for 
IS-IS level, IS-IS authentication, etc.?

Logic in Models yes/no
----------------------
Fat Models, Model Behaviors a.k.a Mixins and Stateless Helper Functions

Timestamp create/update and Model inheritance
---------------------------------------------
django-model-utils to handle common patterns like TimeStampedModel



Style
=====

PEP 8 -- Style Guide for Python Code
------------------------------------
https://www.python.org/dev/peps/pep-0008/

Python Naming Conventions
-------------------------
http://visualgit.readthedocs.io/en/latest/pages/naming_convention.html

Django coding style
-------------------
https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#


Reference
=========
Model Meta options
https://docs.djangoproject.com/en/1.11/ref/models/options/

YAML extension: .yaml
http://www.yaml.org/faq.html


Las Pictures!
=============
Pantone 1235C

Royal Airforce Roundels
https://www.google.ie/search?q=Royal+Air+Force+                                                                                   roundels&source=lnms&tbm=isch&sa=X&ved=0ahUKEwirt9HdmrvUAhWFC8AKHdRBDzsQ_AUICigB&biw=1062&bih=628


How to
======

How to pull a remote branc in git 
---------------------------------
- Create a local branch
`git checkout -b <my_local_branch>`
- Pull the remote branch
`git pull origin {remotebranchname}:{localbranchname}`

From [stack overflow] (https://stackoverflow.com/questions/1709177/git-pull-a-certain-branch-from-github)
- You could pull a branch to a branch with the following commands.
```
git pull {repo} {remotebranchname}:{localbranchname}
git pull origin xyz:xyz
```

- When you are on the master branch you also could first checkout a branch like:
```
git checkout -b xyz
```

- This creates a new branch, "xyz", from the master and directly checks it out. Then you do:
```
git pull origin xyz
```

This pulls the new branch to your local xyz branch.




How to patch with mock
----------------------
This is the one that did it for me in the end!!!!!!
http://neverfriday.com/2015/05/26/django-unit-testing-with-mocks/

::

    from unittest.mock import patch

    class MyTestCase(TestCase):
        @patch('socket.gethostbyname', return_value='1.1.1.1')
        def test_ne_attributes2(self, mock_socket_gethostbyname):
            ne_attribs = audits_ne.get_me_ne_attributes(ne1.id)
            self.assertEqual(mock_socket_gethostbyname.call_count, 1)
            self.assertEqual(ne_attribs['address_ipv4'], mock_socket_gethostbyname())
            #self.assertEqual(ne_attribs['address_ipv4'], '1.1.1.1')

I try to summarize as:
 - we can't really use the function 'socket.gethostbyname'
 - we patch the actual function we can't use -> @patch('socket.gethostbyname', return_value='1.1.1.1')
 - we put a fake value as return for 'socket.gethostbyname', that is the '1.1.1.1'.
 - we put ANY, ANY name as argument to the def test_xxx(self, ANY-NAME):
 - we can see how many times/how the real 'socket.gethostbyname' has been called/substituted, replaced
   by interrogating the ANY-NAME. For example: ANY-NAME.call_count, see above the mock_socket_gethostbyname.call_count


Have these as reference, may be useful
https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


How to see a json file
----------------------

::

    python -m json.tool test.json


How to home/front/landing page
------------------------------
https://tutorial.djangogirls.org/en/django_urls/
url(r'', include('inventories.urls')),

How to Google Analytics
-----------------------
https://moz.com/blog/absolute-beginners-guide-to-google-analytics

How to center with CSS
----------------------
good
https://www.w3.org/Style/Examples/007/center.en.html
less good
https://css-tricks.com/quick-css-trick-how-to-center-an-object-exactly-in-the-center/

How to display an image while page loads
----------------------------------------
http://www.netavatar.co.in/2011/05/31/how-to-show-a-loading-gif-image-while-a-page-loads-using-javascript-and-css/
http://bradsknutson.com/blog/display-loading-image-while-page-loads/
https://stackoverflow.com/questions/27026323/show-loading-gif-after-clicking-form-submit-using-jquery
https://stackoverflow.com/questions/14525029/display-a-loading-message-while-a-time-consuming-function-is-executed-in-flask

How to Javascript Display
-------------------------
https://www.w3schools.com/jsref/prop_style_display.asp
https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_style_display


How to make a copy of the database (complete?)
----------------------------------------------
https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-dumpdata

::

    python manage.py dumpdata apiv1                    > core/fixtures/dump_apiv1_2017-11-29.json
    python manage.py dumpdata audits                   > core/fixtures/dump_audits_2017-11-29.json
    python manage.py dumpdata catalogues               > core/fixtures/dump_catalogues_2017-11
    python manage.py dumpdata inventories.oscredential > core/fixtures/dump_inventories.oscredential_2017-11-29.json
    python manage.py dumpdata inventories.circuit      > core/fixtures/dump_inventories.circuit_2017-11-29.json
    python manage.py dumpdata inventories.ne           > core/fixtures/dump_inventories.ne_2017-11-29.json


How to load data from fixtures
------------------------------
NOTE: the format MUST be JSON or XML. It will not take YAML. You will get this error:

::

    CommandError: Problem installing fixture '<file>': yml is not a known serialization format.


::

    python manage.py loaddata --ignorenonexistent core/fixtures/dump_inventory_2017-06-15.json



How to log
----------
https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info('adjacency: %s', adjacency)



How to run tests
----------------
python manage.py test inventory


How to coverage
---------------
# to run through all the tests and collect the coverage data for the <inventory> application
coverage run --source='.' manage.py test <inventory>
# to see the coverage report
coverage report -m
# to get in html
coverage html   # and find in htmlcov/index.htm?


How to reset the database
-------------------------

::

    python manage.py flush
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py loaddata core/fixtures/dump_inventory_2017-06-15.json
    python manage.py loaddata --ignorenonexistent core/fixtures/dump_inventory_2017-06-15.yaml


How to work with ManyToManyField
--------------------------------

::

    python manage.py shell
    from inventory.models import Ne
    ne1 = Ne.objects.get(fqdn='edge1-dcu-glasnevin.nn.hea.net')
    ne2 = Ne.objects.get(fqdn='edge1-dcu-spd.nn.hea.net')
    nni1 = Ne.objects.get(fqdn='edge1-dcu.nn.hea.net')
    nni2 = Ne.objects.get(fqdn='edge2-dcu.nn.hea.net')
    ne1.nni_neighbors.add(nni1)
    ne1.nni_neighbors.add(nni2)


How to connect to database with Python
--------------------------------------
https://www.tutorialspoint.com/python/python_database_access.htm


How to create a virtual environment in Python3
----------------------------------------------

In Python3, the ability to create virtual evnrionments is part of the core distribution. 
* install apt-get install python3-venv
* python3 -m venv /path/to/new/virtual/environment
* $ source <venv>/bin/activate
* deactivate


Howt to Puppet
--------------
Overall, it is a hierarchy
* modules are the most abstract. For a given environment (e.g. Django or ROR app).
* profiles. Variables/packages for a given app (eg. torque, assetdb, clientdb, etc.)
* hieradata file. Contains the variables for a given host. 




References
==========

DRF Testing
-----------
http://www.django-rest-framework.org/api-guide/testing/
https://www.vinta.com.br/blog/2017/how-i-test-my-drf-serializers/
https://realpython.com/blog/python/test-driven-development-of-a-django-restful-api/



Tricks
======
Convert outcome of Django QuerySet (xxx.all(), or xxx.filter()) to a Python list (['a', 'b'])
https://docs.djangoproject.com/en/dev/ref/models/querysets/#values-list
https://stackoverflow.com/questions/4424435/how-to-convert-a-django-queryset-to-a-list
self.assertEqual(ne_attribs['nni_neighbors'], list(ne1.nni_neighbors.values_list('fqdn', flat=True)))


Migrations
----------
If the number of migrations becomes unwieldy, use squashmigrations to bring them to heel.

Many to Many
------------
Shell

::

    python manage.py shell
    from inventory.models import Ne
    n = Ne.objects.get(pk=1)
    n.nni_neighbors.all()

Template

::

  {% for nni_neighbor in nni_neighbors %}
    {{ nni_neighbor.fqdn }}
  {% endfor %}


OneToOne
--------
Careful with the id field or not (primary_key True/False).
https://github.com/encode/django-rest-framework/issues/720
https://github.com/encode/django-rest-framework/issues/5135



Append same text to every cell in a column in Excel
https://stackoverflow.com/questions/3179513/append-same-text-to-every-cell-in-a-column-in-excel

FIXTURES
https://docs.djangoproject.com/en/1.11/howto/initial-data/
https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-FIXTURE_DIRS
https://code.djangoproject.com/wiki/Fixtures

django.core.exceptions.ImproperlyConfigured: '/workspace/pjt_torque/torque/core/fixtures' is a default fixture directory for the 'core' app and cannot be listed in settings.FIXTURE_DIRS.



Testing
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
https://realpython.com/blog/python/testing-in-django-part-1-best-practices-and-examples/
http://www.tangowithdjango.com/book17/chapters/test.html
https://docs.python.org/3/library/unittest.html#assert-methods


When DEBUG = False, you can use python manage.py runserver --insecure to serve the static files during local development.
python manage.py runserver --insecure 0:3000


You can use WhiteNoise to serve static files in production.
https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail/7639983#7639983

DRF
HyperlinkedModelSerializer vs. ModelSerializer
- primary and foreign keys are represented by URLs that point to those resources, instead of just actual key values
- you will not have to construct resource URLs in your frontend when you want to retrieve related objects
- nested representations which allows you to inline related objects in your serializer output
-  it is more convenient for the API consumer to have related items right away instead of making additional requests to retrieve them
- using URLs as keys makes it easier for other developers to understand your API


API CLI
httpie
http -a <username>:<password> <url> 
http -a joan:baez http://192.168.56.102:3000/api/v1/catalogues/manufacturer/

curl
curl -H 'Accept: application/json; indent=4' -u <username>:<password> <url>
curl -H 'Accept: application/json; indent=4' -u admin:Friday1 http://192.168.56.102:3000/api/v1/catalogues/manufacturer/

Name: Daniel Lete
    Department: NetDev
    Institute: HEANET
    List Type: Private
    List Name: HEANET-RMAN-AUDIT
    Description:  To receive results of RMAN network audits
    List Owner 1: Daniel Lete
    List Owner 2: Garwin Liu
    List Owner 3:
    List Owner 4:
    Subscription: Private
    Review: Owners
    Send: Private
    Confidential: Yes
    Archives: Private


To establish fixtures for each individual test case.
The setUp() and tearDown() methods allow define instructions that will
be executed before and after each test method.

To create and save an object in a single step, use the create() method.
https://docs.djangoproject.com/en/dev/topics/db/queries/#creating-objects

What to test in Models unittest: Creating/updating/deleting of models,
model methods, model manager methods.

