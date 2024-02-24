# Ubuntu OS and packages

Have Ubuntu 16.04

Install the following packages:
```
apt-get install python3-dev
apt-get install build-essential
apt-get install libssl-dev
apt-get install libmysqlclient-dev
apt-get install libssl-dev libffi-dev     # (otherwise, the Python package cryptography fails)
apt-get install libxml2-dev libxslt1-dev  # (otherwise, the Python package lxml fails)
```


# Virtualenv

Create a virtual environment for this project. 

- Install `apt-get install python3-venv`, this is necessary in Ubuntu 16.04.

- Create a virtual environment.
```python
python3 -m venv /path/to/new/virtual/environment
```

And then to use the virtual environment:
- To activate the virtual environment:
```Shell
source </path/to/new/virtual/environment>/bin/activate
```

- To deactivate the virtual environment:
```Shell
deactivate 
```



# Get the code
```Shell
git clone git@bitbucket.org:dlete/torque.git    # if hosted in bitbucket
git clone git@git.heanet.ie:heanet/torque.git   # if hosted in heanet
```


# Install Database

## if you are to use MySQL

Do install MySQL in your OS.
You will also neeed:

```Shell
sudo apt-get install mysql-server libmysqlclient-dev 
```

It also seems to need:
```Shell
sudo apt-get install python-dev
```

Unless `libmysqlclient-dev` is installed in the OS, the Python package `mysqlclient` fill fail. The Python package `mysqlclient` will be defined in the `requirements.txt` file. Do not worry about that Python package now.


## if you are to use MariaDB
Check instructions in: [How To Use MySQL or MariaDB with your Django Application on Ubuntu 14.04] (https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04)
Not sure if `libmysqlclient-dev` is required by MariaDB, I have it installed and does the trick.
Cannot install `libmariadbclient-dev`, does not exist, in Ubuntu 16.04

### if you are to have a cluster
Follow instructions in: [How To Configure a Galera Cluster with MariaDB 10.1 on Ubuntu 16.04 Servers] (https://www.digitalocean.com/community/tutorials/how-to-configure-a-galera-cluster-with-mariadb-10-1-on-ubuntu-16-04-servers)



## Common

Create database, user and grant permissions:

```SQL
CREATE DATABASE torque CHARACTER SET UTF8;
CREATE USER 'torque'@'localhost' IDENTIFIED BY 'Friday13';
GRANT ALL PRIVILEGES ON torque.* TO 'torque'@'localhost';
FLUSH PRIVILEGES;
```

and then, for the Django tests:
```SQL
GRANT ALL PRIVILEGES ON test_torque.* to 'torque'@'localhost';
```


Check the grants for a given user with:
```SQL
show grants for 'torque'@'localhost';
```



# Install required Python packages

Within the virtuallenv.

Do this first.
```Shell
pip install wheel
```

And this next.
```Shell
pip install -r requirements.txt
```

Note that `pip install criptography` will fail unless the OS has compilers, that is the package `build-essential` is installed.



# Initialize the Django project

Again, within the virtualenv. From now now, always operate within the 
virtualenv.
```Shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```


# References
- http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django
- https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04
- https://stackoverflow.com/questions/27274987/how-to-configure-and-use-mysql-with-django
- https://stackoverflow.com/questions/14186055/django-test-app-error-got-an-error-creating-the-test-database-permission-deni



# Install Apache2
You will need these packages:
```Shell
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
```

- copy the apache config file for the vhost to `sites-available`
- review apache config file for the vhost and ensure these parameters are correctly set for your environment:
```
WSGIDaemonProcess torque python-home=/home/dlete/.virtualenvs/torque python-path=/workspace/pjt_torque/torque
WSGIProcessGroup torque
WSGIScriptAlias / /workspace/pjt_torque/torque/torque/wsgi.py
```

- soft link (`ln -s`) apache config file from `sites-available` to `sites-enabled`
- copy `.htpasswd` to `/etc/apache2`



# References
- [How To Serve Django Applications with Apache and mod_wsgi on Ubuntu 16.04](
  https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04)

- [How To Set Up Password Authentication with Apache on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-password-authentication-with-apache-on-ubuntu-16-04)



# Django REST Framework (DRF)

To customize navigation bar: edit `rest_framework/base.html`
To customize login page: edit `rest_framework/login_base.html`



# Graphviz
Does require graphviz in the OS.
```
apt-get install graphviz
```


# How to add an audit

- Create .py script. Put script in `core/libs/jnpr/`
- Add call to function in `audits/libs/audits_ne.py`
- Add view to `audits/views.py`
- Add url entry in `audits/urls.py`
- Add entry in `inventories/templates/inventories/ne_detail.html`
- Add entry to `core/templates/core/features.html`
- Add new audit to view `ne_audit_all in audits/views.py`


# API
- Add view to `apiv1/views.py`
- Add entry to `apiv1/urls.py`


# How to upgrade to Django 2
```Shell
pip install -U django
pip install -U django-rest-swagger
pip install -U djangorestframework
pip install --upgrade -r ../requirements.txt
```

See question in stack overflow [Upgrading all packages with pip](https://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip)
```Shell
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
```

Or this blog: [A `pip` hack to upgrade all your Python packages](https://hackernoon.com/a-pip-hack-to-upgrade-all-your-python-packages-492658c49681)

## Fix namespaces to work in Django 2
- Remove any `namespace` mention from `torque/urls.py` (that is the project `urls.py` file).
- Add 
```Phython
app_name = '<app_name>' 
```
to each 
```Python
<app_name>/urls.py
```
