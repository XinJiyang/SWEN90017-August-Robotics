"""AugustRoboticsBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from AccountManagement import views as av
from DataProcess import client as dc
from DataProcess import job as dj
from . import views as views
from django.urls import re_path
from django.views.static import serve
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from AccountManagement.views import (
    MyTokenObtainPairView,
)

from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path("user/<str:username>/", av.UserAPIView.as_view(), name="user"),
                  path("user/register", av.register, name="register"),
                  path("", views.docs, name="docs"),
                  path('client/add', dc.add_client, name="client_add"),
                  path('client/update', dc.update_client, name="client_update"),
                  path('client/get/ID=<str:client_id>', dc.get_client, name="get_client"),
                  path('client/delete/ID=<str:client_id>', dc.delete_client, name="delete_client"),
                  path('client/list/itemsPerPage=<int:items_per_page>&page=<int:page>/', dc.client_list,
                       name="get_client_list"),
                  path('client/list/itemsPerPage=<int:items_per_page>&page=<int:page>&search=<str:search>/',
                       dc.client_list_search, name="get_client_list_search"),
                  path(
                      'client/list/itemsPerPage=<int:items_per_page>&page=<int:page>/sortBy=<str:attribute>&sortingOrder=<str:order>/',
                      dc.client_list_sort, name="get_client_list_sort"),
                  path(
                      'client/list/itemsPerPage=<int:items_per_page>&page=<int:page>&search=<str:search>/sortBy=<str:attribute>&sortingOrder=<str:order>/',
                      dc.client_list_sort_search, name="get_client_list_sort_search"),
                  path('client/list/name', dc.get_client_name_list, name="get_client_name_list"),
                  path('client/summary', dc.client_data, name="get_client_summary"),

                  path('job/list/itemsPerPage=<int:items_per_page>&page=<int:page>&search=<str:search>/',
                       dj.job_list_search, name="job_list_search"),
                  path(
                      'job/list/itemsPerPage=<int:items_per_page>&page=<int:page>/sortBy=<str:attribute>&sortingOrder=<str:order>/',
                      dj.job_list_sort, name="job_list_sort"),
                  path(
                      'job/list/itemsPerPage=<int:items_per_page>&page=<int:page>&search=<str:search>/sortBy=<str:attribute>&sortingOrder=<str:order>/',
                      dj.job_list_search_sort, name="job_list_search_sort"),

                  path('job/list', dj.job_list, name="job_list"),
                  path('job/list/itemsPerPage=<int:items_per_page>&page=<int:page>/', dj.job_list,
                       name="job_list_custom"),
                  path('job/add', dj.job_add, name="job_add"),
                  path('job/delete/ID=<int:job_id>', dj.job_delete, name="job_delete"),
                  path('job/<int:job_id>', dj.job_basic_detail, name="job_basic_detail"),
                  path('job/summary/<int:job_id>', dj.job_summary, name="job_summary"),
                  path('job/<int:job_id>/markingJobs', dj.markingJob_list, name="markingJob_list"),
                  path('job/<int:job_id>/markingJobs/<int:markingJob_id>', dj.markingJob_detail,
                       name="markingJob_detail"),
                  path('job/<int:job_id>/performance', dj.performance_detail, name="performance_detail"),
                  path('job/generalInfo/<int:job_id>', dj.job_general_info, name='job_general_info'),
                  path('job/generalInfo/markingDays/<int:job_id>', dj.job_general_info_marking_day,
                       name='job_general_info_marking_day'),
                  path('client/<int:client_id>/hall', dj.hall_list, name="hall_list"),
                  path('client/hall/<int:hall_id>', dj.hall_detail, name="hall_detail"),
                  path('client/job/<int:job_id>/halls', dj.hall_list_by_job, name="hall_list_by_job"),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('user/login', MyTokenObtainPairView.as_view(), name='login'),
              ] + static(settings.DOCS_URL, document_root=settings.DOCS_ROOT)
