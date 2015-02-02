from django.conf.urls import patterns, include, url
from django.contrib import admin
from blogapp import views
from blogapp.views import RegisterView

urlpatterns = patterns('',
                        url(r'^$', views.home, name='home'),
                        url(r'^(?P<page>\d+)$', views.main, name='main'),
                        url(r'^admin/', include(admin.site.urls)),
                        url(r'^register/', RegisterView.as_view(), name='register'),
                        url(r'^login/', views.login, name='login'),
                        url(r'^(?P<page>\d+)/submission/$', views.post_submission, name= "submission"),
                        url(r'^(?P<page>\d+)/submission/(?P<submission_id>\d+)/like/$', views.like_button, name='like'),
                        url(r'^(?P<page>\d+)/submission/(?P<submission_id>\d+)/dislike/$', views.dislike_button, name='dislike')
                       )
