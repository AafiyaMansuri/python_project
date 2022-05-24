from django.contrib import admin
from django.urls import path
from resort_client import client_views

urlpatterns = [
    path('signin/', client_views.login),
    path('signup/', client_views.register),
    path('forgot/', client_views.forgot),
    path('sendotp/', client_views.send_otp),
    path('setpass/', client_views.set_password),
    path('clientprofile/', client_views.cprofile),
    path('logout/', client_views.logout),
    path('clientselect/', client_views.Profile_select),
    path('home/', client_views.home),
    path('querytable/', client_views.show_contact),
    path('contactus/', client_views.contactUs),
    path('thanku/', client_views.thanku),
    path('aboutus/', client_views.about),
    path('resort/', client_views.resort),
    path('rooms/', client_views.rooms),
    # path('client_header_menu/', client_views.load_menu),
    path('resort_details/', client_views.resort_details),
    path('Update_password/', client_views.update_pass),
    path('packages/', client_views.packages),
    path('search_product/', client_views.autosuggest, name='area_search'),
    path('search12/', client_views.search),
    path('sawresort/', client_views.saw_resort),
    path('membership/', client_views.membership),
    path('fdetails/<int:id>', client_views.f_packagedetail),
    path('bookresort/<int:id>/<str:name_p>', client_views.book),
    path('resortdetails/<int:id>', client_views.resort_details),
    path('insert_booking/<int:id>/', client_views.book_package),
    path('insert_room/<int:id>/', client_views.book_room),
    path('insert_feedback/', client_views.insert_feedback),
    path('checkout/', client_views.checkout),
    path('rdetails/<int:id>', client_views.roomdetail),
    path('bookroom/<int:id>/<str:name_p>', client_views.bookroom),
    path('feedroom/',client_views.insert_feedback_room),
    path('getmembership/<int:id>',client_views.get_membership),
    path('room_checkout/',client_views.room_checkout),
    path('blog/',client_views.blog),
    path('success/<int:id>',client_views.success),
    path('cencel/<int:id>',client_views.cencle),
    path('mem_success/<int:id>',client_views.mem_success),
    path('mem_cencle/',client_views.mem_cencle),
    path('error/',client_views.error),
    path('header/',client_views.city_name),
    path('home1/<int:id>',client_views.goback),

]
