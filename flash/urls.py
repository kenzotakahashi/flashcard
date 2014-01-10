from django.conf.urls import patterns, url
from flash import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.userLogin, name='login'),
	url(r'^logout/$', views.userLogout, name='logout'),
	url(r'^dashboard/(?P<cardset_id>\d+)/(?P<option>\w*)/$', views.dashboard, name='dashboard'),
	url(r'^add_question/(?P<cardset_id>\d+)/$', views.addQuestion, name='addQuestion'),
	url(r'^edit_question/(?P<question_id>\d+)/$', views.editQuestion, name='editQuestion'),
	url(r'^test/(?P<test_id>\d+)/(?P<cardset_id>\d+)/(?P<question_id>\d+)/(?P<option>\d?)$',
	 	views.test, name='test'),
	url(r'^example/$', views.example, name='example'),
	)