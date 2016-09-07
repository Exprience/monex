# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.conf.urls import url
import views as v


urlpatterns = [

	
	url(r'^home/$', v.ManagerHomeView.as_view(), name = 'manager_home'),

	
	url(r'^rank/$', v.ManagerRankListView.as_view(), name = 'manager_rank_list'),
	url(r'^rank/create/$', v.ManagerRankCreateView.as_view(), name = 'manager_rank_create'),
	url(r'^rank/update/(?P<pk>[0-9]+)/$', v.ManagerRankUpdateView.as_view(), name = 'manager_rank_update'),
	
	
	url(r'^competition/$', v.ManagerCompetitionListView.as_view(), name = 'manager_competition'),
	url(r'^competition/create/$', v.ManagerCompetitionCreateView.as_view(), name = 'manager_competition_create'),
	url(r'^competition/update/(?P<pk>[0-9]+)/$', v.ManagerCompetitionUpdateView.as_view(), name = 'manager_competition_update'),
	url(r'^competition/rank/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.ManagerCompetitionRankUpdateView.as_view(), name = 'manager_competition_competitionrank_change'),
	url(r'^competition/rank/create/$', v.ManagerCompetitionRankCreateView.as_view(), name = 'manager_competition_competitionrank_add'),
	url(r'^competition/filter/$', v.ManagerCompetitionFilter.as_view(), name = 'manager_competition_filter'),
	
	
	url(r'^login/$', v.ManagerLoginView.as_view(), name = 'manager_login'),
	url(r'^logout/$', v.ManagerLoginView.logout, name = 'manager_logout'),
	
	
	url(r'^news/$', v.NewsListView.as_view(), name = 'news'),
	url(r'^news/create/$', v.NewsCreateView.as_view(), name = 'news_create'),
	url(r'^news/update/(?P<pk>[0-9]+)/$', v.NewsUpdateView.as_view(), name = 'news_update'),
	url(r'^news/delete/(?P<pk>[0-9]+)/$', v.NewsDeleteView.as_view(), name = 'news_delete'),
	url(r'^news/category/create/$', v.NewsCategoryCreateUpdateView.as_view(), name = 'news_category_create'),
	url(r'^news/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.NewsCategoryCreateUpdateView.as_view(), name = 'news_category_update'),
	url(r'^news/category/delete/(?P<pk>[0-9A-Za-z\_]+)/$', v.NewsCategoryDeleteView.as_view(), name = 'news_category_delete'),

	
	url(r'^lesson/$', v.LessonListView.as_view(), name = 'lesson_list'),
	url(r'^lesson/create/$', v.LessonCreateView.as_view(), name = 'lesson_create'),
	url(r'^lesson/update/(?P<pk>[0-9]+)/$', v.LessonUpdateView.as_view(), name = 'lesson_update'),
	url(r'^lesson/delete/(?P<pk>[0-9]+)/$', v.LessonDeleteView.as_view(), name = 'lesson_delete'),
	url(r'^lesson/category/create/$', v.LessonCategoryCreateUpdateView.as_view(), name = 'lesson_category_create'),
	url(r'^lesson/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.LessonCategoryCreateUpdateView.as_view(), name = 'lesson_category_update'),
	url(r'^lesson/category/delete/(?P<pk>[0-9A-Za-z\_]+)/$', v.LessonCategoryDeleteView.as_view(), name = 'lesson_category_delete'),

	
	url(r'^research/$', v.ManagerResearchView.as_view(), name = 'manager_research'),
	url(r'^research/create/$', v.ResearchCreateView.as_view(), name = 'manager_research_create'),
	url(r'^research/update/(?P<pk>[0-9]+)/$', v.ManagerResearchUpdateView.as_view(), name = 'manager_research_update'),
	url(r'^research/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.ManagerResearchCategoryUpdateView.as_view(), name = 'research_category_change'),
	url(r'^research/category/create/$', v.ManagerResearchCategoryCreateView.as_view(), name = 'research_category_create'),
	
	
	url(r'^users/$', v.ManagerUserListView.as_view(), name = 'user_list'),
	
	
	url(r'^info/$', v.ManagerInfoView.as_view(), name = 'info'),
	url(r'^password/update/$', v.PasswordUpdateView.as_view(), name = 'password_update'),
	url(r'^admin/users/$', v.ManagerListView.as_view(), name = 'manager_list'),
	url(r'^admin/users/create/$', v.ManagerCreateUpdateView.as_view(), name = 'manager_create'),
	url(r'^admin/users/update/(?P<pk>[0-9]+)/$', v.ManagerCreateUpdateView.as_view(), name = 'manager_update'),

	
	url(r'competition/register/$', v.ManagerCompetitionRegisterView.as_view(), name = 'manager_competition_register'),
	url(r'competition/register/(?P<id>[0-9]+)/$', v.manager_competition_register_view, name = 'manager_competition_register_def'),


	url(r'finance/$', v.ManagerFinanceView.as_view(), name = 'manager_finance'),

	#url(r'support/message/(?P<id>[0-9]+)/$', ManagerSupportMessageView.as_view(), name = 'manager_support_message'),
	#url(r'support/message/all/(?P<id>[0-9]+)/$', manager_support_message_view, name = 'manager_support_message_all'),

	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', v.ManagerSetPasswordView.as_view()),
]