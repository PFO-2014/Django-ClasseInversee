# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from MonEtablissement import views

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'ClasseInversee1.views.home', name='home'),
    url(r'^$', include('MonEtablissement.urls'), name='home'),
    url(r'^login/', views.login),
    url(r'^welcome', views.welcome),
    url(r'^profile', views.show_profile),
    url(r'^MonEtablissement/', include('MonEtablissement.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^exampleform/', views.exampleform),
    url(r'^register/', views.register),
    url(r'^questionform', views.my_questionform),
    url(r'^testd3js', views.your_view),
    url(r'.pdf', views.pdf_view),
    url(r'questionform_(?P<activity_id>\d+)', views.my_questionform),

    
)
