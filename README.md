## Django-tequilla

Simple django lib to use with tequilla.

Sciper is used for username.

EPFL also has a more complex version if needed: http://kis-doc.epfl.ch/django/django-tequila.html

## Install

1) Copy tequila.py in your django project's folder

2) Add in settings.py :

```AUTHENTICATION_BACKENDS = ( 'yourProject.tequila.Backend', )
LOGIN_URL = '/login'

TEQUILA_SERVER = 'https://tequila.epfl.ch' # Url of tequila server
TEQUILA_SERVICE = 'Name of your application' # Title used in tequila
TEQUILA_AUTOCREATE = True # Auto create users ?
TEQUILA_FAILURE = '/failure' # Where to redirect user if there is a problem
```

2b) If you still want to use normal django's authentification, add 'django.contrib.auth.backends.ModelBackend' in AUTHENTICATION_BACKENDS

3) Add in your urls.py

`(r'^login$', 'yourProject.tequila.login'),`

4) You can login using url /login.

4) (Optionnal)

If you want to use this to login in admin section, create in your templates' directory the file admin/login.html with the following content:

`<script type="text/javascript">window.location='/login?next=' + window.location</script>`

5) (Optionnal) 

Create a view with a template bound to url TEQUILA_FAILURE to inform user about problems.

6) If you want to be an admin with a tequila user, create an admin account with your sciper as username before using tequila's authentification or use
 shell to manipulate the database :

```python manage.py shell
from django.contrib.auth.models import User
user = User.objects.get(username=YOURSCIPER)
user.is_admin = True
user.is_staff = True
user.save()
```