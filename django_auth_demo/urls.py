from django.conf.urls import patterns, include, url
import django_auth_demo

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'auth_demo.views.home', name='home'),
    url(r'^home/', 'auth_demo.views.home', name='home'),
    url(r'^register/$', 'auth_demo.views.register', name='register'),
    url(r'^login/$', 'auth_demo.views.login', name='login'),
    url(r'^login_ajax/$', 'auth_demo.views.login_ajax', name='login_ajax'),
    url(r'^logout/$', 'auth_demo.views.logout', name='logout'),
    url(r'^me/$', 'auth_demo.views.me', name='me'),
    # url(r'^django_auth_demo/', include('django_auth_demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
