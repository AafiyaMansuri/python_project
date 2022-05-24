import sys
import random
from django.http import HttpResponse
from django.contrib import messages

from django.core.mail import send_mail

from django.shortcuts import render, redirect

from django.conf import settings
from resort_admin.forms import cityForm,  memberForm, resortForm, galleryForm, packageForm, facilitiesForm, \
    serviceForm, ownerForm, serviceImageupd, galleryImageupd, customerForm, packageImageupd, roomForm
from resort_admin.functions import handle_uploaded_file
from resort_admin.models import customer, city, Membership_package, resort, gallery, package, booking, review, \
    facilities, service, resort_owner, room, Feedback

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View


# Create your views here.
def show_data(request):
    c1 = customer.objects.all()
    return render(request, "data-table.html", {"customer": c1})



def show_city(request):
    c1 = city.objects.all()
    return render(request, "city.html", {"city": c1})


def show_feedback(request):
    f = Feedback.objects.all()
    return render(request, "feedback.html", {'feedback': f})


def show_member(request):
    m1 = Membership_package.objects.all()
    return render(request, "membership_package.html", {"Membership_package": m1})


def show_resort(request):
    r1 = resort.objects.all()
    return render(request, "resort.html", {"resort": r1})


def show_gallery(request):
    g1 = gallery.objects.all()
    return render(request, "gallery.html", {"gallery": g1})


def show_package(request):
    p1 = package.objects.all()
    return render(request, "package.html", {"package": p1})


def show_booking(request):
    b1 = booking.objects.all()
    return render(request, "booking.html", {"booking": b1})


def show_facility(request):
    f1 = facilities.objects.all()
    return render(request, "facility.html", {"facilitiy": f1})


def show_service(request):
    s1 = service.objects.all()
    return render(request, "service.html", {"service": s1})


def show_room(request):
    r2 = room.objects.all()
    return render(request, "room.html", {"room": r2})


def show_owner(request):
    a1 = resort_owner.objects.all()
    return render(request, "resort_owner.html", {"owner": a1})


def insert_city(request):
    if request.method == "POST":
        form = cityForm(request.POST)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/citytable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = cityForm()

    return render(request, "city_insert.html", {'form': form})


def delete_city(request, id):
    c2 = city.objects.get(city_id=id)
    c2.delete()
    return redirect('/citytable')



def delete_feed(request, id):
    a2 = Feedback.objects.get(feedback_id=id)
    a2.delete()
    return redirect('/feedbacktable/')


def delete_room(request, id):
    a2 = room.objects.get(room_id=id)
    a2.delete()
    return redirect('/roomtable/')



def insert_room(request):
    c = resort.objects.all()
    if request.method == "POST":
        form = roomForm(request.POST, request.FILES)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['room_img'])
                form.save()
                return redirect('/roomtable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = roomForm()

    return render(request, "room_insert.html", {'form': form, 'room': c})


def insert_owner(request):
    c = city.objects.all()
    b = resort.objects.all()
    if request.method == "POST":
        form = ownerForm(request.POST)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/ownertable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = ownerForm()

    return render(request, "Owner_insert.html", {'form': form, 'city': c, 'resort': b})


def delete_mem(request, id):
    m2 = Membership_package.objects.get(Member_id=id)
    m2.delete()
    return redirect('/membertable/')


def delete_resort(request, id):
    r2 = resort.objects.get(Resort_id=id)
    r2.delete()
    return redirect('/resorttable/')


def delete_owner(request, id):
    m2 = resort_owner.objects.get(owner_id=id)
    m2.delete()
    return redirect('/ownertable/')


def delete_gallery(request, id):
    g2 = gallery.objects.get(Gallery_id=id)
    g2.delete()
    return redirect('/gallerytable/')


def delete_package(request, id):
    p2 = package.objects.get(package_id=id)
    p2.delete()
    return redirect('/packagetable/')


def delete_facilities(request, id):
    f2 = facilities.objects.get(f_id=id)
    f2.delete()
    return redirect('/facilitytable/')


def delete_service(request, id):
    s2 = service.objects.get(service_id=id)
    s2.delete()
    return redirect('/servicetable/')


def insert_member(request):
    if request.method == "POST":
        print("===========")
        form = memberForm(request.POST, request.FILES)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['pack_img'])
                form.save()
                return redirect('/membertable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = memberForm()

    return render(request, "memberpackage_insert.html", {'form': form})


def insert_resort(request):
    c = city.objects.all()
    if request.method == "POST":
        form = resortForm(request.POST, request.FILES)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['cover_image'])
                form.save()
                return redirect('/resorttable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = resortForm()

    return render(request, "resort_insert.html", {'form': form, 'city': c})


def insert_gallery(request):
    c = resort.objects.all()
    if request.method == "POST":
        form = galleryForm(request.POST, request.FILES)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_image'])
                form.save()
                return redirect('/gallerytable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = galleryForm()

    return render(request, "gallery_insert.html", {'form': form, 'resort': c})


def insert_package(request):
    c = resort.objects.all()
    r = room.objects.all()
    if request.method == "POST":
        form = packageForm(request.POST, request.FILES)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['image_path'])
                form.save()
                return redirect('/packagetable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = packageForm()

    return render(request, "package_insert.html", {'form': form, 'package': c, 'room': r})


def insert_facility(request):
    c = package.objects.all()
    if request.method == "POST":
        form = facilitiesForm(request.POST)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/facilitytable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = facilitiesForm()

    return render(request, "facility_insert.html", {'form': form, 'facility': c})


def insert_service(request):
    c = room.objects.all()
    if request.method == "POST":

        print("=======")
        form = serviceForm(request.POST)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/servicetable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = serviceForm()

    return render(request, "service_insert.html", {'form': form, 'service': c})



def room_select(request, id):
    c = resort.objects.all()
    au = room.objects.get(room_id=id)
    return render(request, 'room_update.html', {'room': au, 'resort': c})


def room_update(request, id):
    c = resort.objects.all()
    au = room.objects.get(room_id=id)
    form = roomForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/roomtable/")
    return render(request, 'room_update.html', {'room': au, 'resort': c})


def city_select(request, id):
    au = city.objects.get(city_id=id)
    return render(request, 'city_update_form.html', {'city': au})


def city_update(request, id):
    au = city.objects.get(city_id=id)
    form = cityForm(request.POST, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/citytable/")
    return render(request, 'city_update_form.html', {'city': au})


def facility_select(request, id):
    c = package.objects.all()
    au = facilities.objects.get(f_id=id)
    return render(request, 'facility_update.html', {'facility': au, 'package': c})


def facility_update(request, id):
    c = package.objects.all()
    au = facilities.objects.get(f_id=id)
    form = facilitiesForm(request.POST, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/facilitytable/")
    return render(request, 'facility_update.html', {'facility': au, 'package': c})


def gallery_select(request, id):
    c = resort.objects.all()
    au = gallery.objects.get(Gallery_id=id)
    return render(request, 'gallery_update.html', {'gallery': au, 'resort': c})


def gallery_update(request, id):
    c = resort.objects.all()
    au = gallery.objects.get(Gallery_id=id)
    form = galleryForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/gallerytable/")
    return render(request, 'gallery_update.html', {'gallery': au, 'resort': c})


def member_select(request, id):
    au = Membership_package.objects.get(Member_id=id)
    return render(request, 'memberpackage_upadte.html', {'member': au})


def member_update(request, id):
    au = Membership_package.objects.get(Member_id=id)
    form = memberForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/membertable/")
    return render(request, 'memberpackage_upadte.html', {'member': au})


def resort_select(request, id):
    c = city.objects.all()
    au = resort.objects.get(Resort_id=id)
    return render(request, 'resort_update.html', {'resort': au, 'city': c})


def resort_update(request, id):
    c = city.objects.all()
    au = resort.objects.get(Resort_id=id)
    form = resortForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/resorttable/")
    return render(request, 'resort_update.html', {'resort': au, 'city': c})


def service_select(request, id):
    c = room.objects.all()
    au = service.objects.get(service_id=id)
    return render(request, 'service_update.html', {'service': au, 'room': c})


def service_update(request, id):
    c = room.objects.all()
    au = service.objects.get(service_id=id)
    form = serviceForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/servicetable/")
    return render(request, 'service_update.html', {'service': au, 'room': c})


def package_select(request, id):
    c = resort.objects.all()
    r = room.objects.all()
    au = package.objects.get(package_id=id)
    return render(request, 'Package_update.html', {'package': au, 'resort': c, 'room': r})


def package_update(request, id):
    c = resort.objects.all()
    au = package.objects.get(package_id=id)
    form = packageForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/packagetable/")
    return render(request, 'Package_update.html', {'package': au, 'resort': c})


def forgot(request):
    return render(request, 'Forgot_password.html')


def send_otp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']

    request.session['temail'] = e

    obj = customer.objects.filter(c_email=e).count()

    if obj == 1:
        val = customer.objects.filter(c_email=e).update(otp=otp1, otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

        return render(request, 'set_password.html')


def set_password(request):
    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['pass']
        T_cpass = request.POST['cpass']

        if T_pass == T_cpass:

            e = request.session['temail']
            val = customer.objects.filter(c_email=e, otp=T_otp, otp_used=0).count()

            if val == 1:
                customer.objects.filter(c_email=e).update(otp_used=1, password=T_pass)
                return redirect("/Login/")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "Forgot_password.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set_password.html")

    else:
        return redirect("/Forgot_password/")


def logout(request):
    email = request.session['admin_email']
    del request.session['admin_email']
    return redirect("/Login/")


def dashboard(request):
    package1 = package.objects.all().count()
    customer1 = customer.objects.all().count()
    Booking1 = booking.objects.all().count()
    city1 = city.objects.all().count()
    b2 = booking.objects.all()
    return render(request, "deshboard.html",
                  {'package_count': package1, 'customer1_count': customer1, 'booking_count': Booking1,
                   'city_count': city1, "book": b2})


def img_ser(request, id):
    c = resort.objects.all()
    if request.method == "POST":

        print("=======")
        form = serviceImageupd(request.POST, request.FILES)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['service_image'])
                form.save()
                return redirect('/servicetable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = serviceImageupd()

    return render(request, "Service_image_update.html", {'form': form, 'service': c})


def select_img_service(request, id):
    au = service.objects.get(service_id=id)
    return render(request, 'Service_image_update.html', {'service': au})


def img_gallery(request, id):
    c1 = resort.objects.all()
    if request.method == "POST":

        print("=======")
        form = galleryImageupd(request.POST, request.FILES)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_image'])
                form.save()
                return redirect('/gallerytable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = galleryImageupd()

    return render(request, "Gallery_image_update.html", {'form': form, 'gallery': c1})


def select_img_gallery(request, id):
    au1 = gallery.objects.get(Gallery_id=id)
    return render(request, 'Gallery_image_update.html', {'gallery': au1})


def img_package(request, id):
    c1 = resort.objects.all()
    if request.method == "POST":

        print("=======")
        form = packageImageupd(request.POST, request.FILES)
        print("--------------", form.errors)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['image_path'])
                form.save()
                return redirect('/packagetable/')
            except:
                print("---------------", sys.exc_info())
    else:
        form = packageImageupd()

    return render(request, "Package_image_update.html", {'form': form, 'package': c1})


def select_img_package(request, id):
    au1 = package.objects.get(package_id=id)
    return render(request, 'Package_image_update.html', {'package': au1})


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        pssword = request.POST["pass"]
        val = customer.objects.filter(c_email=email, password=pssword).count()
        print("---------------", email, "--------------", pssword)
        if val == 1:
            data = customer.objects.filter(c_email=email, password=pssword, Is_admin=1)
            for item in data:
                request.session['admin_email'] = item.c_email
                request.session['admin_password'] = item.password
                request.session['admin_id'] = item.c_id
            if request.POST.get("remember"):
                response1 = redirect("/index/")
                response1.set_cookie('c_admin_email', request.POST["email"], 3600 * 24 * 365 * 2)
                response1.set_cookie('c_admin_password', request.POST["pass"], 3600 * 24 * 365 * 2)
                return response1
            return redirect('/index/')
        else:
            messages.error(request, "Invalid username and Password")
            return redirect('/Login/')
    else:
        if request.COOKIES.get("c_admin_email"):
            return render(request, "Login.html", {'admin_cookie_email': request.COOKIES['c_admin_email'],
                                                  'admin_cookie_password': request.COOKIES['c_admin_password']})
        else:
            return render(request, 'Login.html')


def profile(request):
    print("=================")
    id = request.session['admin_id']
    email = request.session['admin_email']
    password = request.session['admin_password']

    val = customer.objects.filter(c_email=email, password=password).count()
    users = customer.objects.get(c_id=id)
    print("------------------------------", val)
    if val == 1:
        us = customer.objects.get(c_id=id)
        form = customerForm(request.POST, instance=us)
        print("-----------------", form.errors)
        if form.is_valid():
            form.save()
            return redirect("/customer/")
        return render(request, 'profile.html', {'profile': us})
    return render(request, 'profile.html', {'details': users})


def Profile_select(request):
    admin_id = request.session['admin_id']
    passw = request.session['admin_password']
    val = customer.objects.get(c_id=admin_id)
    return render(request, 'profile.html', {'details': val})


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "deshboard.html")


class ProjectChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        cursor = connection.cursor()
        cursor.execute(
            '''SELECT (select city_name from city where city_id = r.city_id_id) as name , count(*) as count FROM booking b join package p JOIN resort r JOIN city c where b.package_id_id = p.package_id and p.Resort_id_id = r.Resort_id and r.city_id_id = c.city_id GROUP by city_id;''')
        qs = cursor.fetchall()

        labels = []
        default_items = []
        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


def accept_booking(request, id):
    b = booking.objects.get(booking_id=id)
    b.booking_status = 1
    b.save()
    e = request.session['client_email']
    obj = customer.objects.filter(c_email=e).count()
    if obj == 1:
        val = customer.objects.filter(c_email=e)
        subject = 'Regarding Your Booking in our Resort'
        message = f' Your Booking is Accepted By the Owner.\n'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [e, ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('/bookingtable/')


def reject_booking(request, id):
    print("=====================", )
    b = booking.objects.get(booking_id=id)
    b.booking_status = 2
    b.save()
    print("=====================", )
    e = request.session['client_email']
    print("==========email===========", e)
    obj = customer.objects.filter(c_email=e).count()
    print("==========obj===========", obj)
    if obj == 1:
        val = customer.objects.filter(c_email=e)
        subject = 'Regarding Your Booking in our Resort'
        message = f' Your Booking is Rejected By the Owner due to some reasons.\n'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [e, ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('/bookingtable/')


def booking_report1(request):
    sql = "SELECT 1 as booking_id, (select city_name from city where city_id = r.city_id_id) as name , count(*) as count FROM booking b join package p JOIN resort r JOIN city c where b.package_id_id = p.package_id and p.Resort_id_id = r.Resort_id and r.city_id_id = c.city_id GROUP by city_id;"
    d = booking.objects.raw(sql)
    return render(request, "Booking Report.html", {"booking": d})


def booking_report2(request):
    sql = "SELECT 1 as booking_id, (select city_name from city where city_id = r.city_id_id) as name , count(*) as count FROM booking b join room p JOIN resort r JOIN city c where b.room_id_id = p.room_id and p.Resort_id_id = r.Resort_id and r.city_id_id = c.city_id GROUP by city_id;"
    d = booking.objects.raw(sql)
    return render(request, "Booking Report1.html",{"booking": d})


from django.utils.dateparse import parse_date
def dynamic_report(request):
    if request.method == "POST":
        s_d = request.POST.get('start_date')
        e_d = request.POST.get('end_date')
        start = parse_date(s_d)
        end = parse_date(e_d)
        ord = booking.objects.filter(booking_date__range=[start, end])
        #sql = "SELECT * FROM order_table o JOIN order_item i where o.order_id = i.order_id_id and o.order_date >= %s and o.order_date <= %s;"
        #ord = Order_item.objects.raw(sql,[s_d,e_d])
    else:
        ord = booking.objects.all()
    return render(request, "report_date.html", {"book": ord})


def dynamic_report2(request):
    if request.method == "POST":
        city = request.POST.get('city_name')
        r = resort.objects.all()
        for data in r:
            if data.city_id.city_name == city:
                val=data.city_id
                print("============", val)
            else:
                print("=====No Resort Found=======")
    else:
        return render(request,"report_city.html")

