"""resort URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path, include
from resort_admin import views

from django.conf.urls import url
from resort_admin.views import HomeView, ProjectChart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', views.show_data),
    path('citytable/', views.show_city),
    path('membertable/', views.show_member),
    path('resorttable/', views.show_resort),
    path('gallerytable/', views.show_gallery),
    path('packagetable/', views.show_package),
    path('bookingtable/', views.show_booking),
    path('feedbacktable/', views.show_feedback),
    path('facilitytable/', views.show_facility),
    path('servicetable/', views.show_service),
    path('ownertable/', views.show_owner),
    path('roomtable/', views.show_room),
    path('insert/', views.insert_city),
    path('deletecity/<int:id>', views.delete_city),
    path('deleteroom/<int:id>', views.delete_room),
    path('deletefeed/<int:id>', views.delete_feed),
    path('deletemember/<int:id>', views.delete_mem),
    path('deleteresort/<int:id>', views.delete_resort),
    path('deletegallery/<int:id>', views.delete_gallery),
    path('deletepackage/<int:id>', views.delete_package),
    path('deletefacility/<int:id>', views.delete_facilities),
    path('deleteservice/<int:id>', views.delete_service),
    path('deleteowner/<int:id>', views.delete_owner),
    path('insertmember/', views.insert_member),
    path('insertresort/', views.insert_resort),
    path('insertgallery/', views.insert_gallery),
    path('insertpackage/', views.insert_package),
    path('insertfacility/', views.insert_facility),
    path('insertservice/', views.insert_service),
    path('insertowner/', views.insert_owner),
    path('insertroom/', views.insert_room),
    path('editroom/<int:id>', views.room_select),
    path('updateroom/<int:id>', views.room_update),
    path('editcity/<int:id>', views.city_select),
    path('updatecity/<int:id>', views.city_update),
    path('editfacility/<int:id>', views.facility_select),
    path('updatefacility/<int:id>', views.facility_update),
    path('editgallery/<int:id>', views.gallery_select),
    path('updategallery/<int:id>', views.gallery_update),
    path('editmember/<int:id>', views.member_select),
    path('updatemember/<int:id>', views.member_update),
    path('editresort/<int:id>', views.resort_select),
    path('updateresort/<int:id>', views.resort_update),
    path('editservice/<int:id>', views.service_select),
    path('updateservice/<int:id>', views.service_update),
    path('editpackage/<int:id>', views.package_select),
    path('updatepackage/<int:id>', views.package_update),
    path('Login/', views.login),
    path('forget/', views.forgot),
    path('send_otp/', views.send_otp),
    path('reset/', views.set_password),
    path('logout/', views.logout),
    path('index/', views.dashboard),
    path('simageup/<int:id>', views.img_ser),
    path('showimgservice/<int:id>', views.select_img_service),
    path('gimageup/<int:id>', views.img_gallery),
    path('showimggallery/<int:id>', views.select_img_gallery),
    path('pimageup/<int:id>', views.img_package),
    path('showimgpackage/<int:id>', views.select_img_package),
    path('profile/', views.profile),
    path('select_profile/', views.Profile_select),
    path('accept_booking/<int:id>',views.accept_booking),
    path('reject_booking/<int:id>',views.reject_booking),
    path('report/',views.booking_report1),
    path('report1/',views.booking_report2),
    path('report2/',views.dynamic_report),
    path('report3/',views.dynamic_report2),
    url(r'charthome', HomeView.as_view(), name='home'),
    url(r'^api/chart/data/$', ProjectChart.as_view(), name="api-data"),

    path('Client/', include('resort_client.urls')),
    path('owner/', include('resort_owner.urls')),
]
