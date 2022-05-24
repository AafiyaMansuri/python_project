from django.contrib import admin
from django.urls import path
from resort_owner import owner_views

urlpatterns = [
    path('ownerlogin/',owner_views.owner_Login),
    path('ownerregister/',owner_views.owner_register),
    path('forgetpass/',owner_views.forgotpass),
    path('otpsend/',owner_views.otp_send),
    path('resetpass/',owner_views.set_pass),
    path('profileselect/',owner_views.select_profile),
    path('updateprofile/',owner_views.profile_update),
    path('ownerlogout/',owner_views.logout),
    path('room/',owner_views.roomt),
    path('package/',owner_views.packaget),
    path('roomdelete/<int:id>',owner_views.deleteroom),
    path('gallery/',owner_views.galleryt),
    path('booking/',owner_views.bookingt),
    path('facility/',owner_views.facilityt),
    path('service/',owner_views.servicet),
    path('gallerydelete/<int:id>',owner_views.deletegallry),
    path('packagedelete/<int:id>',owner_views.deletepackage),
    path('facilitydelete/<int:id>',owner_views.deletefacilities),
    path('servicedelete/<int:id>',owner_views.deleteservice),
    path('roomedit/<int:id>',owner_views.roomselect),
    path('roomupdate/<int:id>',owner_views.roomupdate),
    path('facilityedit/<int:id>',owner_views.facilityselect),
    path('facilityupdate/<int:id>',owner_views.facilityupdate),
    path('packageedit/<int:id>',owner_views.packageselect),
    path('packageupdate/<int:id>',owner_views.packageupdate),
    path('serviceedit/<int:id>',owner_views.serviceselect),
    path('servcieupadte/<int:id>',owner_views.serviceupdate),
    path('galleryedit/<int:id>',owner_views.galleryselect),
    path('galleryupdate/<int:id>',owner_views.galleryupdate),


]