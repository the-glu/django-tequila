# Tequila auth for django

# Version 2.0, 06.11.2015
# (C) Maximilien Cuony 2015
# BSD License


from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, authenticate, get_user_model, REDIRECT_FIELD_NAME
from django.conf import settings
from django.utils.http import is_safe_url


import requests
import re


def do_query(call, data=None):
    """Do a call on tequila'server"""

    if data:

        # Tequila's encoding
        data = '\n'.join(['{}={}'.format(k, v) for k, v in data.items()])

        print(data)

        r = requests.post('{}/cgi-bin/tequila/{}'.format(settings.TEQUILA_SERVER, call), data=data)
    else:
        r = requests.get('{}/cgi-bin/tequila/{}'.format(settings.TEQUILA_SERVER, call))

    if not r or not r.text:
        raise Exception("No response from tequila server when calling {}".format(call))

    return r


def get_request_key(request):
    """Ask tequila server for the key"""

    data = {
        'urlaccess': request.build_absolute_uri(),
        'service': settings.TEQUILA_SERVICE,
        'request': 'name,firstname,email,uniqueid'
    }

    response = do_query('createrequest', data)

    try:
        key = re.search('key=(.*)', response.text).group(1)
    except:
        key = None

    if key:
        return key
    else:
        raise Exception("Unable to find a key for tequila request")


def build_faillure(request, string):
    """ Build an HttpResponseRedirect for a faillure"""
    return HttpResponseRedirect("{}?why={}".format(settings.TEQUILA_FAILURE, string))


class Backend:
    """Backend to authenticate users"""

    def get_user(self, user_id):

        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

    def authenticate(self, token=None):

        # Check if token is valid
        data = {
            'key': token,
        }

        response = do_query('fetchattributes', data)

        if response.text.find('status=ok') == -1:
            return None

        # Get informations about user
        first_name = re.search('\nfirstname=(.*)', response.text).group(1).split(',')[0]
        last_name = re.search('\nname=(.*)', response.text).group(1).split(',')[0]
        email = re.search('\nemail=(.*)', response.text).group(1)
        sciper = re.search('\nuniqueid=(.*)', response.text).group(1)

        # Find user in database
        try:
            user = get_user_model().objects.get(username=sciper)

        except get_user_model().DoesNotExist:

            # Should we create it ?
            if settings.TEQUILA_AUTOCREATE:
                user = get_user_model()()
                user.username = sciper
            else:
                user = None

        # Update user info
        if user and (settings.TEQUILA_UPDATE or not user.pk):  # No pk = new user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

        return user

def login(request):
    """Login view"""

    key = request.GET.get('key', '')

    if key:  # If there is a key, try to login

        user = authenticate(token=key)

        if not user:  # Try to auth
            return build_faillure(request, 'genericerror')

        if not user.is_active:
            return build_faillure(request, 'disabled')

        auth_login(request, user)  # Login user

        redirect_to = request.COOKIES.get('tequila_login_redirect')

        if not redirect_to or not is_safe_url(url=redirect_to, host=request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return HttpResponseRedirect(redirect_to)

    else:  # Create a new tequila request

        response = HttpResponseRedirect('{}/cgi-bin/tequila/requestauth?requestkey={}'.format(settings.TEQUILA_SERVER, get_request_key(request)))

        # Set the cookie to be redirected when auth is done
        next = request.GET.get(REDIRECT_FIELD_NAME, settings.LOGIN_REDIRECT_URL)
        response.set_cookie('tequila_login_redirect', next)

        return response
