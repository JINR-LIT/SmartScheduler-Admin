# SmartScheduler admin

This project implements the web-interface for the SmartScheduler project and is based on Django administrative interface. Django >1.10 is supported.

## Prerequisites

CentOS/SL 6 and the Apache web-server must be installed first, which is not covered in this document.

## Installing on a CentOS/SL 6

## mod_wsgi

We need to install python34 first which is located in epel repo (make sure it is installed and activated):

```bash
$ yum install python34 gcc python34-devel mysql-devel
```

And pip34:
```bash
$ curl -O https://bootstrap.pypa.io/get-pip.py
$ /usr/bin/python3.4 get-pip.py
```

We'll also need httpd-devel to install mod_wsgi:

```bash
yum install httpd-devel
```

Now we can install mod_wsgi:

```bash
$ pip3.4 install mod_wsgi
```

Run `$ mod_wsgi-express module-config` and you’ll get the output like this:
```bash
LoadModule wsgi_module "/usr/lib64/python3.4/site-packages/mod_wsgi/server/mod_wsgi-py34.cpython-34m.so"
WSGIPythonHome "/usr"
```
Place it into the `/etc/httpd/conf.d/wsgi.conf`.

Edit `/etc/httpd/conf/httpd.conf`:
```bash
Listen 8000
<VirtualHost *:8000>
     DocumentRoot /var/www/scheduler
     WSGIScriptAlias / /var/www/scheduler/sched_django/sched_django/wsgi.py
     Alias "/static/" /var/www/scheduler/sched_django/static/
     <Directory /var/www/scheduler/sched_django/static>
         Order deny,allow
         Allow from all
     </Directory>
</VirtualHost>
```

You can change the port number to whatever you want, but don't forget to allow it in your firewall.


### Database
```bash
$ yum install mysql-server
$ service mysqld start
```

Run `mysql_secure_installation` command and follow the guides.

Now we need to create the user and the database:
```bash
$ mysql -u root -p

> create database smartsched;
> create user 'smartsched'@'localhost' IDENTIFIED by 'smartsched';
> grant all privileges on smartsched.* to smartsched@localhost;
> flush privileges;
```

### Django

Install required dependences first:
```bash
$ pip3.4 install django==version django_admin_bootstrapped django.js xmltodict django-bootstrap3 django-fontawesome mysqlclient
```

Where substitute the `version` with the current django version you want to use (e.g. 1.11.2).

Follow the repo guides to install the [SmartScheduler-lib](https://git.jinr.ru/cloud-team/SmartScheduler-lib).

Place `sched_django` folder (the one **from the root!**) from this repo under `/var/www/scheduler`.

Populate `/var/www/scheduler/sched_django/sched_django/settings.py` with proper database name and credentials and also check the `ALLOWED_HOSTS` - it should be an IP or a hostname of your server.

>>
### django-debug-toolbar
By default [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/stable/) is enabled, so make sure to install it if you wish to use it for development:  
```bash
pip3.4 install django-debug-toolbar
```
Edit the [configuration](https://django-debug-toolbar.readthedocs.io/en/stable/) if needed or just change the `INTERNAL_IPS` to match the IP-address of the host that will be used to access the site.  
If you don't want to use it then remove `debug_toolbar` and `debug_toolbar.middleware.DebugToolbarMiddleware` from the INSTALLED_APPS and MIDDLEWARE sections correspondingly and also remove the `INTERNAL_IPS` and `DEBUG_TOOLBAR_CONFIG` parameters from your settings.py.
>>

Prepare the database:
```bash
python3.4 manage.py migrate
```

And finally create the `root` user:
```bash
$ python3.4 manage.py createsuperuser
```

Restart apache: `service httpd restart`

Now your site should be avalable by http://your_address:8000/admin