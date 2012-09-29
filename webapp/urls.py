from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('webapp.views',
    url(r'', include('singly.urls')),
    url(r'^$', 'index', name='index'),
    url(r'^accounts/login/$', 'index'),
    url(r'^webapp/resume/upload/$', 'upload_view' ),
    url(r'^webapp/candidate/(?P<userid>\d+)/resume/(?P<user_resume_id>\d+)$', 'get_candidate_info'),
    url(r'^webapp/qrcode/(?P<userid>\d+)/resume/(?P<user_resume_id>\d+)$',
        'save_qr_code'),
    url(r'^webapp/resume/(?P<user_resume_id>\d+)$',
        'get_resume'),
    url(r'^webapp/rating/(?P<user_resume_id>\d+)/$',
        'rate_candidate'),
    url(r'^webapp/download/(?P<emailid>\w+)/$',
        'download_resumes'),
    url(r'^webapp/fullfil/(?P<emailid>\w+)/$',
        'fullfil_purchase'),
)
