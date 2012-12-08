from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import simplejson
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

import os
from webapp.models import UserResume, CandidateRating
from singly.models import UserProfile
from singly.singly import Singly

import urllib



def index(request, template='index1.html'):
    services = [
        'LinkedIn'
    ]

    if request.user.is_authenticated():
        user_profile = request.user.get_profile()
        # We replace single quotes with double quotes b/c of python's strict json requirements
        profiles = simplejson.loads(user_profile.profiles.replace("'", '"'))

        mode = request.GET.get('mode', '_cand')
        if mode == '_recruiter':
            return fullfil_purchase(request, 'someemail@email.com')

    #default to candidate or login page
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
    )

    return response


@login_required
@csrf_exempt
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

    data = "%s/webapp/candidate/%s/resume/%s" % (_get_domain_addr(), userid, user_resume_id)

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
    print 'in get_candidate_info'
    try:
        print 'userid=', userid
        user_profile = UserProfile.objects.get(id=userid)
    except UserProfile.DoesNotExist as e:
        print e
        return render_to_response(request, True)

    host_name = _get_domain_addr()
    user_resume =  UserResume.objects.get(id=user_resume_id)
    print user_resume.file_location

    resume_url = "%s/webapp/resume/%s" % (_get_domain_addr(), user_resume.id)

    response = render_to_response(
            'candidate.html', locals(), context_instance=RequestContext(request)
        )

    return response

def get_rate(request):
    response = render_to_response(
            'rate.html', locals(), context_instance=RequestContext(request)
        )

    return response



@csrf_exempt
def rate_candidate(request, user_resume_id):
    print request.raw_post_data
    rating = request.GET['Rating']
    email = request.GET['Email']


    print 'email=', email
    user_resume = UserResume.objects.get(id=user_resume_id)

    CandidateRating.objects.create(user_resume=user_resume,
                                   rating = rating, email=email)

    print 'returing after rate_candidate'
    return HttpResponse("Candidate rating has been saved", content_type='text/html')


def _get_domain_addr():
    import socket
    ipaddr = socket.gethostbyname(socket.gethostname())
    return  "http://%s:8000" % (ipaddr)


def download_resumes(request, emailid):
    emailid = 'freegyan@gmail.com'
    #return render_template("download_resumes.html", tr_data=tr_data,
    #                      braintree_url=braintree_url)

    response = render_to_response(
        "download_resumes.html", locals(), context_instance=RequestContext(request)
    )
    return response

def fullfil_purchase(request, emailid):

    #query_string = urlparse.urlparse(request.get_full_path()).query

    print 'fdsafsaasfsafsasf'
    result = True ; #braintree.TransparentRedirect.confirm(query_string)
    records = list()
    if result:

        print 'Checking for email=', emailid
        cand_list  = CandidateRating.objects.filter(email=emailid)

        for cand in cand_list:
            user_profile = cand.user_resume.user
            access_token = user_profile.access_token
            file_location = "%s/webapp/resume/%s" % (_get_domain_addr(),
                                                     cand.user_resume.id)

            rating = cand.rating
            s = Singly(settings.SINGLY_CLIENT_ID, settings.SINGLY_CLIENT_SECRET, access_token)
            linkedin_profile = s.make_request('/services/linkedin/self')
            twitter_profile = s.make_request('/services/twitter/self')

            picture_url = linkedin_profile[0]['data']['pictureUrl']
            name = linkedin_profile[0]['data']['lastName'] + "," + \
                   linkedin_profile[0]['data']['firstName']
            linkedin_url = linkedin_profile[0]['data']['publicProfileUrl']

            print twitter_profile[0]['data']['screen_name']
            records.append([picture_url, name, linkedin_url, file_location,
                            rating, twitter_profile[0]['data']['screen_name']])
            

    else:
        message = "Errors: %s" % " ".join(error.message for error in
                                                   result.errors.deep_errors)
    return render_to_response("recruiter.html",
                              locals(),
    context_instance=RequestContext(request))
