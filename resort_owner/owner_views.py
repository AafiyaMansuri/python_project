import sys
import random
from urllib import request

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from resort_admin import models
from resort_admin.forms import ownerForm, roomForm, facilitiesForm, packageForm, serviceForm, galleryForm
from resort_admin.models import resort_owner, room, package, gallery, booking, facilities, service, resort


def owner_Login(request):
    if request.method == "POST":
        email = request.POST["email"]
        pssword = request.POST["pass"]
        val = resort_owner.objects.filter(owner_email=email, owner_pass=pssword).count()
        print("---------------", email, "--------------", pssword)
        print("-----------val----", val)
        if val == 1:
            print("+++++++++++++inside if+++++++++++++")
            data = resort_owner.objects.filter(owner_email=email, owner_pass=pssword)
            for item in data:
                request.session['owner_email'] = item.owner_email
                request.session['owner_password'] = item.owner_pass
                request.session['owner_id'] = item.owner_id
            if request.POST.get("remember"):
                response1 = redirect("/owner/room/")
                response1.set_cookie('c_owner_email', request.POST["email"], 3600 * 24 * 365 * 2)
                response1.set_cookie('c_owner_password', request.POST["pass"], 3600 * 24 * 365 * 2)
                return response1
            return redirect('/owner/room/')
        else:
            print("=================")
            messages.error(request, "Invalid username and Password")
            return redirect('/owner/ownerlogin/')
    else:
        if request.COOKIES.get("c_owner_email"):
            return render(request, "owner_login.html", {'owner_cookie_email': request.COOKIES['c_owner_email'],
                                                        'owner_cookie_password': request.COOKIES['c_owner_password']})
        else:
            return render(request, "owner_login.html")


def owner_register(request):
    r = resort.objects.all()
    print(request.method)
    if request.method == "POST":
        form = ownerForm(request.POST)
        print("--------------", form.errors)
        print(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('/owner/ownerlogin/')
            except:
                print("---------------", sys.exc_info())
    else:
        print("get")
        form = ownerForm()

    return render(request, "owner_registration.html", {'form': form, 'resort': r})


def forgotpass(request):
    return render(request, 'Forget_pass.html')


def otp_send(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']

    request.session['temail'] = e

    obj = resort_owner.objects.filter(owner_email=e).count()

    if obj == 1:
        val = resort_owner.objects.filter(owner_email=e).update(otp=otp1, otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

        return render(request, 'set_pass.html')


def set_pass(request):
    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['pass']
        T_cpass = request.POST['cpass']

        if T_pass == T_cpass:

            e = request.session['temail']
            val = resort_owner.objects.filter(owner_email=e, otp=T_otp, otp_used=0).count()

            if val == 1:
                resort_owner.objects.filter(owner_email=e).update(otp_used=1, owner_pass=T_pass)
                return redirect("/owner/ownerlogin/")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "Forgot_pass.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set_pass.html")

    else:
        return redirect("/Forgot_pass/")


def select_profile(request):
    owner_id = request.session['owner_id']
    passw = request.session['owner_password']
    val = resort_owner.objects.get(owner_id=owner_id)
    return render(request, 'owner_profile.html', {'details': val})


def profile_update(request):
    print("=================")
    id = request.session['owner_id']
    email = request.session['owner_email']
    password = request.session['owner_password']

    val = resort_owner.objects.filter(owner_email=email, owner_pass=password).count()
    users = resort_owner.objects.get(owner_id=id)
    print("------------------------------", val)
    if val == 1:
        us = resort_owner.objects.get(owner_id=id)
        form = ownerForm(request.POST, instance=us)
        print("-----------------", form.errors)
        if form.is_valid():
            form.save()
            return redirect("/ownertable/")
        return render(request, 'owner_profile.html', {'profile': us})
    return render(request, 'owner_profile.html', {'details': users})


def logout(request):
    email = request.session['owner_email']
    del request.session['owner_email']
    return redirect("/owner/ownerlogin/")


def roomt(request):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    g1 = {}
    for data in b:
        resorts = data.Resort_id
        g1 = room.objects.filter(Resort_id=resorts)
    return render(request, "roomtable.html", {'room1': g1})


def packaget(request):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    g1 = {}
    for data in b:
        resorts = data.Resort_id
        g1 = package.objects.filter(Resort_id=resorts)
    return render(request, "packagetable.html", {'pac': g1})


def galleryt(request):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    g1 = {}
    for data in b:
        resorts = data.Resort_id
        g1 = gallery.objects.filter(Resort_id=resorts)
    return render(request, "gallerytable.html", {"gallery": g1, 'owner': b})


def bookingt(request):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    print("========\n\n\n\n\n\n\n", b)
    all_data = []
    for data in b:
        # g1 = booking.objects.filter(package_id__Resort_id=data.Resort_id)
        # g2 = booking.objects.filter(room_id__Resort_id=data.Resort_id)
        # print("hhhhhhhhhhhh", type(g1))
        # all_data.append(g1)
        # all_data.append(g2)
        resorts = data.Resort_id
        g1 = booking.objects.filter(Resort_id=resorts)
    print("==========\n\n\n\n\n\n", g1)
    return render(request, "bookingtable.html", {"booking": all_data, 'owner': b})


def facilityt(request):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    print("========\n\n\n\n\n\n\n", b)
    for data in b:
        g1 = facilities.objects.filter(package_id__Resort_id=data.Resort_id)
    return render(request, "facilitytable.html", {"facilitiy": g1, 'owner': b})


def servicet(request):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    print("========\n\n\n\n\n\n\n", b)
    for data in b:
        g1 = service.objects.filter(room_id__Resort_id=data.Resort_id)
    return render(request, "servicetable.html", {"service": g1, 'owner': b})


def deleteroom(request, id):
    a2 = room.objects.get(room_id=id)
    a2.delete()
    return redirect('/owner/room/')


def deletegallry(request, id):
    g2 = gallery.objects.get(Gallery_id=id)
    g2.delete()
    return redirect('/owner/gallery/')


def deletepackage(request, id):
    p2 = package.objects.get(package_id=id)
    p2.delete()
    return redirect('/owner/package/')


def deletefacilities(request, id):
    f2 = facilities.objects.get(f_id=id)
    f2.delete()
    return redirect('/owner/facility/')


def deleteservice(request, id):
    s2 = service.objects.get(service_id=id)
    s2.delete()
    return redirect('/owner/servicetable/')


def roomselect(request, id):
    c = resort.objects.all()
    au = room.objects.get(room_id=id)
    return render(request, 'roomtableupdate.html', {'room': au, 'resort': c})


def roomupdate(request, id):
    au = room.objects.get(room_id=id)
    form = roomForm(request.POST, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/owner/room/")
    return render(request, 'roomtableupdate.html', {'room': au})


def facilityselect(request, id):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    for data in b:
        g1 = package.objects.filter(Resort_id=data.Resort_id)
        print("||||||||||||||||||||||||", g1)
    au = facilities.objects.get(f_id=id)
    return render(request, 'facilitytableupdate.html', {'facility': au, 'package': g1})


def facilityupdate(request, id):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    for data in b:
        g1 = package.objects.filter(Resort_id=data.Resort_id)
        print("||||||||||||||||||||||||", g1)
    au = facilities.objects.get(f_id=id)
    form = facilitiesForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/owner/facility/")
    return render(request, 'facilitytableupdate.html', {'facility': au, 'package': g1})


def packageselect(request, id):
    c = resort.objects.all()
    r = room.objects.all()
    au = package.objects.get(package_id=id)
    return render(request, 'Packagetableupdate.html', {'package': au, 'resort': c, 'room': r})


def packageupdate(request, id):
    c = resort.objects.all()
    au = package.objects.get(package_id=id)
    form = packageForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/owner/package/")
    return render(request, 'Packagetableupdate.html', {'package': au, 'resort': c})


def serviceselect(request, id):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    for data in b:
        g1 = room.objects.filter(Resort_id=data.Resort_id)
    au = service.objects.get(service_id=id)
    return render(request, 'servicetableupdate.html', {'service': au, 'room': g1})


def serviceupdate(request, id):
    u = request.session['owner_id']
    b = resort_owner.objects.filter(owner_id=u)
    for data in b:
        g1 = room.objects.filter(Resort_id=data.Resort_id)
    au = service.objects.get(service_id=id)
    form = serviceForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/owner/service/")
    return render(request, 'servicetableupdate.html', {'service': au, 'room': g1})


def galleryselect(request, id):
    c = resort.objects.all()
    au = gallery.objects.get(Gallery_id=id)
    return render(request, 'gallerytableupdate.html', {'gallery': au, 'resort': c})


def galleryupdate(request, id):
    c = resort.objects.all()
    au = gallery.objects.get(Gallery_id=id)
    form = galleryForm(request.POST, request.FILES, instance=au)
    print('----------------------', form.errors)
    if form.is_valid():
        form.save()
        return redirect("/owner/gallery/")
    return render(request, 'gallerytableupdate.html', {'gallery': au, 'resort': c})
