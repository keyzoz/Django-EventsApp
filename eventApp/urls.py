from .views import *
from django.urls import path

urlpatterns = [
    path('',EventHome.as_view(),name='home'),
    path('add_event/',AddEvent.as_view(),name='add_event'),
    path('add_category/',AddCategory.as_view(),name='add_category'),
    path('login/',LoginUser.as_view(),name='login'),
    path('register/',RegisterUser.as_view(),name='register'),
    path('logout/',userLogout,name='logout'),
    path('event/<slug:event_slug>/',EventDetail.as_view(),name='detail_event'),
    path('category/<slug:cat_slug>/',EventCategory.as_view(),name='category')
]