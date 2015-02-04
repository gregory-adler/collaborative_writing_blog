from django.conf.urls import patterns, include, url
from django.contrib import admin
from blogapp import views
from blogapp.views import RegisterView

urlpatterns = patterns('',
                        url(r'^$', views.home, name='home'),
                        url(r'^(?P<page>\d+)$', views.main, name='main'),
                        url(r'^admin/', include(admin.site.urls)),
                        url(r'^register/$', RegisterView.as_view(), name='register'),
                        url(r'^login/$', views.login_page, name='login'),
                        url(r'^newstory/$', views.new_story, name='new_story'),
                        url (r'^add_new_story/$', views.add_new_story, name='addnewstory'), 
                        url(r'^login/submit/$', views.try_login, name='trylogin'),
                        url(r'^logout/submit$', views.try_logout, name='trylogout'),
                        url(r'^(?P<page>\d+)/submission/$', views.post_submission, name= "submission"),
                        url(r'^(?P<page>\d+)/submission/(?P<submission_id>\d+)/like/$', views.like_button, name='like'),
                        url(r'^(?P<page>\d+)/submission/(?P<submission_id>\d+)/dislike/$', views.dislike_button, name='dislike')
                       )
