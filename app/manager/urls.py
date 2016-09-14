# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.conf.urls import url
import views as v


urlpatterns = [

	
	url(r'^home/$', v.HomeView.as_view(), name = 'manager_home'),

	
	url(r'^competition/$', v.CompetitionListView.as_view(), name = 'competition_list'),
	url(r'^competition/create/$', v.CompetitionCreateView.as_view(), name = 'competition_create'),
	url(r'^competition/update/(?P<pk>[0-9]+)/$', v.CompetitionUpdateView.as_view(), name = 'competition_update'),
	url(r'^competition/category/create/$', v.CompetitionCategoryCreateUpdateView.as_view(), name = 'competition_category_create'),
	url(r'^competition/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.CompetitionCategoryCreateUpdateView.as_view(), name = 'competition_category_update'),
	url(r'^competition/category/delete/(?P<pk>[0-9A-Za-z\_]+)/$', v.CompetitionCategoryDeleteView.as_view(), name = 'competition_category_delete'),
	url(r'^competition/filter/$', v.CompetitionFilter.as_view(), name = 'competition_filter'),
	
	
	url(r'^login/$', v.LoginView.as_view(), name = 'manager_login'),
	url(r'^logout/$', v.LoginView.logout, name = 'manager_logout'),
	
	
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

	
	url(r'^research/$', v.ResearchListView.as_view(), name = 'research_list'),
	url(r'^research/create/$', v.ResearchCreateView.as_view(), name = 'research_create'),
	url(r'^research/update/(?P<pk>[0-9]+)/$', v.ResearchUpdateView.as_view(), name = 'research_update'),
	url(r'^research/delete/(?P<pk>[0-9]+)/$', v.ResearchUpdateView.as_view(), name = 'research_delete'),
	url(r'^research/category/create/$', v.ResearchCategoryCreateUpdateView.as_view(), name = 'research_category_create'),
	url(r'^research/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.ResearchCategoryCreateUpdateView.as_view(), name = 'research_category_update'),
	url(r'^research/category/delete/(?P<pk>[0-9A-Za-z\_]+)/$', v.ResearchCategoryDeleteView.as_view(), name = 'research_category_delete'),
	
	
	url(r'^bank/$', v.BankListView.as_view(), name = 'bank_list'),
	url(r'^bank/create/$', v.BankCreateUpdateView.as_view(), name = 'bank_create'),
	url(r'^bank/update/(?P<pk>[0-9]+)/$', v.BankCreateUpdateView.as_view(), name = 'bank_update'),
	url(r'^bank/delete/(?P<pk>[0-9]+)/$', v.BankDeleteView.as_view(), name = 'bank_delete'),


	url(r'^currency/$', v.CurrencyListView.as_view(), name = 'currency_list'),
	url(r'^currency/create/$', v.CurrencyCreateUpdateView.as_view(), name = 'currency_create'),
	url(r'^currency/update/(?P<pk>[0-9]+)/$', v.CurrencyCreateUpdateView.as_view(), name = 'currency_update'),
	url(r'^currency/delete/(?P<pk>[0-9]+)/$', v.CurrencyDeleteView.as_view(), name = 'currency_delete'),

	url(r'^currency/value/$', v.CurrencyValueListView.as_view(), name = 'currency_value_list'),
	url(r'^currency/value/create/$', v.CurrencyValueCreateView.as_view(), name = 'currency_value_create'),


	url(r'^stock/$', v.StockListView.as_view(), name = 'stock_list'),
	url(r'^stock/create/$', v.StockCreateUpdateView.as_view(), name = 'stock_create'),
	url(r'^stock/update/(?P<pk>[0-9]+)/$', v.StockCreateUpdateView.as_view(), name = 'stock_update'),
	url(r'^stock/delete/(?P<pk>[0-9]+)/$', v.StockDeleteView.as_view(), name = 'stock_delete'),

	url(r'^stock/value/$', v.StockValueListView.as_view(), name = 'stock_value_list'),
	url(r'^stock/value/create/$', v.StockValueCreateView.as_view(), name = 'stock_value_create'),

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