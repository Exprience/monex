# !/usr/bin/python/env
# -*- coding:utf-8 -*-


from django.conf.urls import url
import views as v


urlpatterns = [
	
	url(r'^home/$', v.Home.as_view(), name = 'home'),

	
	url(r'^competition/$', v.CompetitionList.as_view(), name = 'competition_list'),
	url(r'^competition/create/$', v.CompetitionCreate.as_view(), name = 'competition_create'),
	url(r'^competition/update/(?P<pk>[0-9]+)/$', v.CompetitionUpdate.as_view(), name = 'competition_update'),
	url(r'^competition/category/create/$', v.CompetitionCategoryCreate.as_view(), name = 'competition_category_create'),
	url(r'^competition/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.CompetitionCategoryCreate.as_view(), name = 'competition_category_update'),
	url(r'^competition/category/delete/(?P<pk>[0-9A-Za-z\_]+)/$', v.CompetitionCategoryDelete.as_view(), name = 'competition_category_delete'),
	url(r'^competition/filter/$', v.CompetitionFilter.as_view(), name = 'competition_filter'),
	
	
	url(r'^login/$', v.Login.as_view(), name = 'manager_login'),
	url(r'^logout/$', v.Login.logout, name = 'manager_logout'),
	
	
	url(r'^news/$', v.NewsList.as_view(), name = 'news'),
	url(r'^news/create/$', v.NewsCreate.as_view(), name = 'news_create'),
	url(r'^news/update/(?P<pk>[0-9]+)/$', v.NewsUpdate.as_view(), name = 'news_update'),
	url(r'^news/delete/(?P<pk>[0-9]+)/$', v.NewsDelete.as_view(), name = 'news_delete'),
	url(r'^news/category/create/$', v.NewsCategoryCreate.as_view(), name = 'news_category_create'),
	url(r'^news/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.NewsCategoryCreate.as_view(), name = 'news_category_update'),
	url(r'^news/category/delete/(?P<pk>[0-9A-Za-z\_]+)/$', v.NewsCategoryDelete.as_view(), name = 'news_category_delete'),

	
	url(r'^lesson/$', v.LessonList.as_view(), name = 'lesson_list'),
	url(r'^lesson/create/$', v.LessonCreate.as_view(), name = 'lesson_create'),
	url(r'^lesson/update/(?P<pk>[0-9]+)/$', v.LessonUpdate.as_view(), name = 'lesson_update'),
	url(r'^lesson/delete/(?P<pk>[0-9]+)/$', v.LessonDelete.as_view(), name = 'lesson_delete'),
	url(r'^lesson/category/create/$', v.LessonCategoryCreate.as_view(), name = 'lesson_category_create'),
	url(r'^lesson/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.LessonCategoryCreate.as_view(), name = 'lesson_category_update'),
	url(r'^lesson/category/delete/(?P<pk>[0-9A-Za-z\_]+)/$', v.LessonCategoryDelete.as_view(), name = 'lesson_category_delete'),

	
	url(r'^research/$', v.ResearchList.as_view(), name = 'research_list'),
	url(r'^research/create/$', v.ResearchCreate.as_view(), name = 'research_create'),
	url(r'^research/update/(?P<pk>[0-9]+)/$', v.ResearchUpdate.as_view(), name = 'research_update'),
	url(r'^research/delete/(?P<pk>[0-9]+)/$', v.ResearchDelete.as_view(), name = 'research_delete'),
	url(r'^research/category/create/$', v.ResearchCategoryCreate.as_view(), name = 'research_category_create'),
	url(r'^research/category/update/(?P<pk>[0-9A-Za-z\_]+)/$', v.ResearchCategoryCreate.as_view(), name = 'research_category_update'),
	url(r'^research/category/delete/(?P<pk>[0-9A-Za-z\_]+)/$', v.ResearchCategoryDelete.as_view(), name = 'research_category_delete'),
	
	
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


	url(r'^users/$', v.UserList.as_view(), name = 'user_list'),
	
	
	url(r'^info/$', v.AdminInfo.as_view(), name = 'info'),
	url(r'^password/update/$', v.AdminPasswordUpdate.as_view(), name = 'password_update'),
	url(r'^admin/users/$', v.AdminList.as_view(), name = 'manager_list'),
	url(r'^admin/users/create/$', v.AdminCreate.as_view(), name = 'manager_create'),
	url(r'^admin/users/update/(?P<pk>[0-9]+)/$', v.AdminCreate.as_view(), name = 'manager_update'),
	url(r'^admin/password/reset/$', v.AdminPasswordReset.as_view(), name = 'password_reset'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', v.AdminPasswordSet.as_view()),

	

	url(r'competition/register/$', v.CompetitionRegister.as_view(), name = 'competition_register'),
	url(r'competition/register/(?P<pk>[0-9]+)/$', v.CompetitionRegisterUser.as_view(), name = 'competition_register_user_list'),
	url(r'competition/register/approve/(?P<ck>[0-9]+)/(?P<pk>[0-9]+)/$', v.approve, name = 'approve'),
	url(r'competition/register/decline/(?P<ck>[0-9]+)/(?P<pk>[0-9]+)/$', v.decline, name = 'decline'),


	url(r'finance/$', v.ManagerFinanceView.as_view(), name = 'manager_finance'),
	
]