from django.conf.urls import url
from .views import *

urlpatterns = [

	
	url(r'^home/$', ManagerHomeView.as_view(), name = 'manager_home'),

	
	url(r'^rank/$', ManagerRankListView.as_view(), name = 'manager_rank_list'),
	url(r'^rank/create/$', ManagerRankCreateView.as_view(), name = 'manager_rank_create'),
	url(r'^rank/update/(?P<pk>[0-9]+)/$', ManagerRankUpdateView.as_view(), name = 'manager_rank_update'),
	
	
	url(r'^competition/$', ManagerCompetitionListView.as_view(), name = 'manager_competition'),
	url(r'^competition/create/$', ManagerCompetitionCreateView.as_view(), name = 'manager_competition_create'),
	url(r'^competition/update/(?P<pk>[0-9]+)/$', ManagerCompetitionUpdateView.as_view(),
		name = 'manager_competition_update'),
	url(r'^competition/rank/update/(?P<pk>[0-9A-Za-z\_]+)/$', ManagerCompetitionRankUpdateView.as_view(),
		name = 'manager_competition_competitionrank_change'),
	url(r'^competition/rank/create/$', ManagerCompetitionRankCreateView.as_view(),
		name = 'manager_competition_competitionrank_add'),
	
	
	url(r'^login/$', ManagerLoginView.as_view(), name = 'manager_login'),
	url(r'^logout/$', ManagerLoginView.logout, name = 'manager_logout'),
	
	
	url(r'^news/$', ManagerNewsView.as_view(), name = 'manager_news'),
	url(r'^news/create/$', ManagerNewsCreateView.as_view(), name = 'manager_news_create'),
	url(r'^news/update/(?P<pk>[0-9]+)/$', ManagerNewsUpdateView.as_view(), name = 'manager_news_update'),
	url(r'^news/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', ManagerNewsCategoryUpdateView.as_view(),
		name = 'manager_web_medeeangilal_change'),
	url(r'^news/category/create/$', ManagerNewsCategoryCreateView.as_view(),
		name = 'manager_web_medeeangilal_add'),
	
	
	url(r'^about/$', ManagerAboutView.as_view(), name = 'manager_about'),
	url(r'^about/create/$', ManagerAboutCreateView.as_view(), name = 'manager_about_create'),

	
	url(r'^lesson/$', ManagerLessonView.as_view(), name = 'manager_lesson'),
	url(r'^lesson/create/$', ManagerLessonCreateView.as_view(), name = 'manager_lesson_create'),
	url(r'^lesson/update/(?P<pk>[0-9]+)/$', ManagerLessonUpdateView.as_view(), name = 'manager_lesson_update'),
	url(r'^lesson/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', ManagerLessonCategoryUpdateView.as_view(),
		name = 'manager_web_surgaltangilal_change'),
	url(r'^lesson/category/create/$', ManagerLessonCategoryCreateView.as_view(),
		name = 'manager_web_surgaltangilal_add'),

	
	url(r'^research/$', ManagerResearchView.as_view(), name = 'manager_research'),
	url(r'^research/create/$', ManagerResearchCreateView.as_view(), name = 'manager_research_create'),
	url(r'^research/update/(?P<pk>[0-9]+)/$', ManagerResearchUpdateView.as_view(),
		name = 'manager_research_update'),
	url(r'^research/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', ManagerResearchCategoryUpdateView.as_view(),
		name = 'manager_web_sudalgaaangilal_change'),
	url(r'^research/category/create/$', ManagerResearchCategoryCreateView.as_view(),
		name = 'manager_web_sudalgaaangilal_add'),
	
	
	url(r'^users/$', ManagerUserListView.as_view(), name = 'manager_user_list'),
	

	url(r'^admin/users/$', ManagerAdminUserListView.as_view(), name = 'manager_admin_user_list'),
	url(r'^admin/users/create/$', ManagerAdminUserCreateView.as_view(), name = 'manager_admin_user_create'),
	url(r'^admin/users/update/(?P<pk>[0-9]+)/$', ManagerAdminUserUpdateView.as_view(), name = 'manager_admin_user_update'),


	url(r'^mymodal/$', MyModal.as_view(), name='mymodal'),
	url(r'^mymodal/update/(?P<pk>[0-9]+)/$', MyModalUpdate.as_view(), name='mymodal_update'),

	
	url(r'competition/register/$', ManagerCompetitionRegisterView.as_view(), name = 'manager_competition_register'),
	url(r'competition/register/(?P<id>[0-9]+)/$', manager_competition_register_view, name = 'manager_competition_register_def'),


	url(r'finance/$', ManagerFinanceView.as_view(), name = 'manager_finance'),

	url(r'support/message/(?P<id>[0-9]+)/$', ManagerSupportMessageView.as_view(), name = 'manager_support_message'),
	url(r'support/message/all/(?P<id>[0-9]+)/$', manager_support_message_view, name = 'manager_support_message_all'),

]