from django.http import HttpResponseRedirect
from singly import SinglyHelper
from django.contrib.auth import authenticate, login as auth_login
from models import UserProfile
import logging

logger = logging.getLogger(__name__)

def authenticate_redirect(request, service):
    url = SinglyHelper.get_authorize_url(service)
    return HttpResponseRedirect(url)

def authorize_callback(request):

    error = request.GET.get('error', "")
    if error:
        #TODO : Do something graceful
        logger.error("%s from Singly", error)
        return HttpResponseRedirect("/error.html")

    mode = request.GET.get('mode', '_cand')
    code = request.GET.get('code')
    content = SinglyHelper.get_access_token(code)
    user_profile = UserProfile.objects.get_or_create_user(
            content['account'], content['access_token'])
    if not request.user.is_authenticated():
        user = authenticate(username=user_profile.user.username, password='fakepassword')
        auth_login(request, user)
    return HttpResponseRedirect('/?mode='+mode)
