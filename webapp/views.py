from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from upload_form import UploadFileForm
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import os
import settings
from webapp.models import UserResume, CandidateRating

import urllib
import braintree
import urlparse

def index(request, template='index.html'):
    services = [
        'LinkedIn'
    ]

    if request.user.is_authenticated():
        user_profile = request.user.get_profile()
        # We replace single quotes with double quotes b/c of python's strict json requirements
        profiles = simplejson.loads(user_profile.profiles.replace("'", '"'))


    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    return response


@login_required
@csrf_protect
def upload_view(request):
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            print request.FILES

            # save the file, add an entry in database, generate bar-code
            handle_uploaded_file(request.FILES['file'])
            user_resume = UserResume.objects.create(user=request.user.get_profile(),
                                      file_name="fdsafas",
                                      file_location=os.path.join(
                                                             request.FILES['file'].name))

            print request.FILES['file'].name

            userid = request.user.get_profile().id
            user_resume_id = user_resume.id
            return save_qr_code(request, userid, user_resume_id )
    else:
        form = UploadFileForm()

    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('upload.html', c)


def save_qr_code(request, userid, user_resume_id):

    import socket
    ipaddr = socket.gethostbyname(socket.gethostname())

    data = "%s/webapp/employee/%s/resume/%s" % (_get_domain_addr(), userid, user_resume_id)

    url = \
          "http://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=%s&chld=H|0" \
          % (data)

    qrobj = urllib.urlopen(url)
    return HttpResponse(qrobj.read(), content_type='image/png')


def handle_uploaded_file(file):
    path = os.path.join(settings.FILE_UPLOAD_PATH, file.name)
    print path
    x = default_storage.save(os.path.join(settings.FILE_UPLOAD_PATH, file.name), file)

    print x, file
   #return render_to_response(request, {'t':'t'} )

def get_resume(request, user_resume_id):

    userresume = UserResume.objects.get(id=user_resume_id)
    path = os.path.join(settings.FILE_UPLOAD_PATH, userresume.file_location )
    print path
    f = open(path)
    return HttpResponse(f.read(), content_type='application/pdf')


@csrf_exempt
def get_candidate_info(request, userid, user_resume_id):
    try:
        user_profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        return response_to_render(request, True)

    user_resume =  UserResume.objects.get(id=user_resume_id)
    print user_resume.file_location
    resume_url = "%s/webapp/resume/user_resume.file_location" % (_get_domain_addr())

    response = render_to_response(
            'candidate.html', locals(), context_instance=RequestContext(request)
        )

    return response

@csrf_exempt
def rate_candidate(request, user_resume_id):
    print request.raw_post_data
    rating = request.POST['Rating']
    email = request.POST['Email']
    user_resume = UserResume.objects.get(id=user_resume_id)

    CandidateRating.objects.create(user_resume=user_resume,
                                   rating = rating, email=email)

    return HttpResponse("Candidate rating has been saved", True)


def _get_domain_addr():
    import socket
    ipaddr = socket.gethostbyname(socket.gethostname())
    return  "http://%s:8000" % (ipaddr)


def download_resumes(request, emailid):

     tr_data = braintree.Transaction.tr_data_for_sale(
            {"transaction": {"type": "sale",
                             "amount": "10",
                             "options": {"submit_for_settlement": True}}},
            "%s/webapp/fullfil/%s/" % (_get_domain_addr(), 1))

     braintree_url = braintree.TransparentRedirect.url()
     #return render_template("download_resumes.html", tr_data=tr_data,
     #                      braintree_url=braintree_url)

     response = render_to_response(
         "download_resumes.html", locals(), context_instance=RequestContext(request)
     )
     return response


def fullfil_purchase(request, emailid):

    query_string = urlparse.urlparse(request.get_full_path()).query

    result = braintree.TransparentRedirect.confirm(query_string)
    if result.is_success:
        message = "Transaction Successful: %s. Amount: %s" % (
                        result.transaction.status, result.transaction.amount)
    else:
        message = "Errors: %s" % " ".join(error.message for error in
                                                   result.errors.deep_errors)
    return render_to_response("fullfil_purchase.html",
                              locals(), context_instance=RequestContext(request))