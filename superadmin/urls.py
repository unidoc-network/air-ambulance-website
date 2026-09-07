from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from superadmin import views
app_name = 'superadmin'

urlpatterns = [
    path('', views.LoginPageView.as_view(), name='login'),
    path('Dashboard', views.Dashboard.as_view(), name='Dashboard'),
    path('Profile', views.Profile.as_view(), name='Profile'),
    path('Logout', views.Logout.as_view(), name='Logout'),

    # Contact Messages
    path('ContactList', views.ContactList.as_view(), name='ContactList'),
    path('ContactDelete/<int:id>', views.ContactDelete.as_view(), name='ContactDelete'),

    # News & Stories
    path('News-Stories', views.NewsList.as_view(), name='NewsList'),
    path('News-Stories-Add', views.NewsAdd.as_view(), name='NewsAdd'),
    path('News-Stories-Sequence', views.UpdateBlogSequence.as_view(), name='UpdateBlogSequence'),
    path('News-Stories-Update/<int:id>', views.NewsAdd.as_view(), name='NewsUpdate'),

    # Categories
    path('Categories', views.CategoryList.as_view(), name='CategoryList'),
    path('Category-Add', views.CategoryAdd.as_view(), name='CategoryAdd'),
    path('Category-Update/<int:id>', views.CategoryAdd.as_view(), name='CategoryUpdate'),

    # Careers
    path('CareerList', views.CareerList.as_view(), name='CareerList'),
    path('CareerAdd', views.CareerAdd.as_view(), name='CareerAdd'),
    path('CareerUpdate/<int:id>', views.CareerAdd.as_view(), name='CareerUpdate'),
    path('CareerStatus', views.CareerStatus.as_view(), name='CareerStatus'),
    path('CareerDelete', views.CareerDelete.as_view(), name='CareerDelete'),
    path('CareerDetail', views.CareerDetail.as_view(), name='CareerDetail'),
    path('CareerArabicDetail', views.CareerArabicDetail.as_view(), name='CareerArabicDetail'),

    # Career Applications
    path('ApplicationList', views.CareerApplicationList.as_view(), name='ApplicationList'),
    path('ApplicationDelete', views.CareerApplicationDelete.as_view(), name='ApplicationDelete'),

]