from django.conf.urls import patterns, include, url
from django.contrib import admin
from blogapp import views

urlpatterns = patterns('',
                       url(r'^$', views.main, name='main'),
                       url(r'^admin/', include(admin.site.urls)),
                        url(r'^submission/$', views.post_submission, name= "submission")
                       )
