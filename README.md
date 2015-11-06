## Simple-django-tequila
[![PyPI version](https://badge.fury.io/py/simple-django-tequila.svg)](https://badge.fury.io/py/simple-django-tequila)
[![PyPI](https://img.shields.io/pypi/l/Django.svg)]()
[![PyPI](https://img.shields.io/badge/PY2-Compatible-green.svg)]()
[![PyPI](https://img.shields.io/badge/PY3-Compatible-green.svg)]()


A very simple django login backend to login users with tequila.

Sciper is used as username.

EPFL also has a more complex version if needed: http://kis-doc.epfl.ch/django/django-tequila.html

## Install

1) `pip install simple-django-tequila`

2) Add to your settings.py :

```
AUTHENTICATION_BACKENDS = ('simple_django_tequila.Backend',)
LOGIN_URL = '/login'

TEQUILA_SERVER = 'https://tequila.epfl.ch'  # Url of tequila server
TEQUILA_SERVICE = 'Name of your application'  # Title used in tequila
TEQUILA_AUTOCREATE = True  # Auto create users ?
TEQUILA_UPDATE = True  # Update users ?
TEQUILA_FAILURE = '/failure'  # Where to redirect user if there is a problem
```

2b) If you still want to use normal django's authentification, add `'django.contrib.auth.backends.ModelBackend'` in `AUTHENTICATION_BACKENDS`

3) Add to your urls.py

`url(r'^login$', 'simple_django_tequila.login'),`

4) You can login using url /login. Notice: You don't have to do this, you can use the view `simple_django_tequila.login` as one of your login's methods.

5) (Optionnal)

If you want to use this to login in admin section, create in your templates' directory the file admin/login.html with the following content:

`<script type="text/javascript">window.location='/login?next=' + window.location</script>`

6) (Optionnal)

Create a view with a template bound to url TEQUILA_FAILURE to inform user about problems.

7) If you want to be an admin with a tequila user, create an admin account with your sciper as username before using tequila's authentification or use
 shell to manipulate the database :

```
python manage.py shell

from django.contrib.auth import get_user_model

user = get_user_model().objects.get(username=YOURSCIPER)

user.is_admin = True
user.is_staff = True

user.save()
```
