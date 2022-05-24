import sys
from django.http import HttpResponse
import random
import datetime
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from resort_admin.forms import customerForm, QueryForm, updateForm
from resort_admin.functions import gst
from resort_admin.models import customer, booking, contact, resort, city, package, room, gallery, facilities, \
    Feedback, service, Membership_package, resort_owner


def login(request):
    print("====INSIDE LOGIN ==========")
    if request.method == "POST":
        print("====INSIDE IFFFFFFFFFFFFFFFFFFFFFFFF")
        email = request.POST["email"]
        pssword = request.POST["pass"]
        val = customer.objects.filter(c_email=email, password=pssword, Is_admin=0).count()
        print("---------------", email, "--------------", pssword)
        if val == 1:
            data = customer.objects.filter(c_email=email, password=pssword, Is_admin=0)
            for item in data:
                request.session['client_email'] = item.c_email
                request.session['client_password'] = item.password
                request.session['client_id'] = item.c_id
                print("=====SESSION====", request.session['client_email'])
            if request.POST.get("remember"):
                response = redirect("/Client/home/")
                response.set_cookie('c_client_email', request.POST["email"], 3600 * 24 * 365 * 2)
                response.set_cookie('c_client_password', request.POST["pass"], 3600 * 24 * 365 * 2)
                return response
            return redirect('/Client/home/')
        else:
            messages.error(request, "Invalid username and Password")
            return redirect('/Client/signin/')
    else:
        if request.COOKIES.get("c_client_email"):
            return render(request, "sign-in.html", {'client_cookie_email': request.COOKIES['c_client_email'],
                                                    'client_cookie_password': request.COOKIES['c_client_password']})
        else:
            return render(request, "sign-in.html")


def register(request):
    print(request.method)
    if request.method == "POST":
        form = customerForm(request.POST)
        print("--------------", form.errors)
        print(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('/Client/signin/')
            except:
                print("---------------", sys.exc_info())
    else:
        print("get")
        form = customerForm()

    return render(request, "sign-up.html", {'form': form})


def forgot(request):
    return render(request, 'forget_password.html')


def send_otp(request):
    print("=======================")
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']
    request.session['temail'] = e

    obj = customer.objects.filter(c_email=e).count()

    if obj == 1:
        val = customer.objects.filter(c_email=e).update(otp=otp1, otp_used=0)
        print("********************************************", val)

        subject = 'OTP Verification'
        message = f'\n Your otp for change password:{otp1}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

        return render(request, 'set-password.html')


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
                return redirect("/Client/signin/")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "forget_password.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set-password.html")

    else:
        return redirect("/Client/forgot/")


def cprofile(request):
    print("=======C PROFILE")
    id = request.session['client_id']
    email = request.session['client_email']
    password = request.session['client_password']

    val = customer.objects.filter(c_email=email, password=password).count()
    users = customer.objects.get(c_id=id)
    print("------------------------------", val)
    if val == 1:
        us = customer.objects.get(c_id=id)
        form = updateForm(request.POST, instance=us)
        print("-----------------", form.errors)
        if form.is_valid():
            form.save()
            print("===========form valid")
            return redirect("/Client/clientselect/")
        return render(request, 'client_profile.html', {'profile': us})
    return render(request, 'client_profile.html', {'details': users})
    # return render(request, 'client_profile.html')


def Profile_select(request):
    print("=====")
    try:
        ct_id = request.session['client_id']
        passw = request.session['client_password']
        b1 = booking.objects.filter(c_id=ct_id)
        val = customer.objects.get(c_id=ct_id)
    except:
        return redirect("/Client/signin/")
    return render(request, 'client_profile.html', {'details': val, "book": b1})


def logout(request):
    print("+++++++++++++++++++++++++++++++++===============")
    user_email = request.session['client_email']
    userpass = request.session['client_password']
    uid = request.session['client_id']
    del request.session['client_email']
    del request.session['client_password']
    del request.session['client_id']
    return redirect('/Client/signin/')


def home(request):
    feed = Feedback.objects.all()
    return render(request, 'home.html', {'feedback': feed})


def show_contact(request):
    c1 = contact.objects.all()
    return render(request, "show_contact.html", {"contact": c1})


def contactUs(request):
    c = resort_owner.objects.all()
    print(request.method)
    if request.method == "POST":
        form = QueryForm(request.POST)
        print("--------------", form.errors)
        print(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('/Client/thanku/')
            except:
                print("---------------", sys.exc_info())
    else:
        print("get")
        form = QueryForm()

    return render(request, "contact-us.html", {'form': form, 'owner': c})


def thanku(request):
    return render(request, "ThankYou.html")


def about(request):
    feed = Feedback.objects.all()
    return render(request, "aboutUs.html", {'feedback': feed})


def rooms(request):
    return render(request, "client_room.html")


def packages(request):
    print("====INSIDE FUNCTION")
    return render(request, "client_package.html")


# def load_menu(request):
#     c = resort.objects.all()
#     #s = SubCatagory.objects.all()
#
#     return render(request, "test.html", {"cat": c})


def resort_details(request, id):
    r = resort.objects.get(Resort_id=id)
    packages = package.objects.filter(Resort_id=id)
    print("+++++++++", packages)
    rooms = room.objects.filter(Resort_id=id)
    g = gallery.objects.filter(Resort_id=id)
    print("=\n\n\n\n\n\n\n\n\n===", r)

    return render(request, "resort_detail.html", {"resort": r, "packages": packages, "rooms": rooms, "gallery": g})


def update_pass(request):
    print("Riya")
    User_lemail = request.session['client_email']
    passw = request.session['client_password']
    id1 = request.session['client_id']
    T_pass = request.POST['pass']
    T_cpass = request.POST['cpass']

    val = customer.objects.filter(c_email=User_lemail, password=passw, c_id=id1).count()
    user = customer.objects.get(c_id=id1)
    print("------------------------------", val)

    if T_pass == T_cpass:
        val = customer.objects.filter(c_email=User_lemail).count()
        if val == 1:
            customer.objects.filter(c_email=User_lemail).update(password=T_pass)
            return redirect("/Client/clientselect/")
        else:
            messages.error(request, "Something went Wrong")
            return render(request, "forget_password.html")
    else:
        messages.error(request, "New password and Confirm password does not match ")
        return render(request, 'client_profile.html', {'details': user})


def autosuggest(request):
    if 'term' in request.GET:
        qs = city.objects.filter(city_name__icontains=request.GET.get('term'))

        names = list()

        for x in qs:
            names.append(x.city_name)
        return JsonResponse(names, safe=False)
    return render(request, "header_footer.html")


def search(request):
    if request.method == "POST":
        name = request.POST["city_name"]
        a = resort.objects.filter(city_id__city_name=name)

        if a:
            return render(request, "all_resorts.html", {'resort': a})
        else:

            return render(request, "404page.html")

    return render(request, "all_resorts.html", {'resort': a})


# def search(request):
#     if request.method == "POST":
#         name = request.POST["area_name"]
#         r = resort.objects.get(city_id__city_name=name)
#         return redirect("/Client/resortdetails/%s" % r.Resort_id)
#
#     else:
#         r = city.objects.all()
#         return redirect("/Client/error/")
#     return render(request, "resort_detail.html", {"resort": r})


def saw_resort(request):
    a = resort.objects.all()
    return render(request, "all_resorts.html", {'resort': a})


def membership(request):
    c = request.session['client_id']
    cd = customer.objects.get(c_id=c)
    m = Membership_package.objects.all()

    return render(request, "membership.html", {'mem': m, 'cus': cd})


def f_packagedetail(request, id):
    pac = package.objects.filter(package_id=id)
    print("=====Package id====", pac)
    f = facilities.objects.filter(package_id=id)
    f1 = Feedback.objects.filter(package_id=id)
    print("packages details", pac)
    f2 = Feedback.objects.filter(package_id=id).count()
    rating = 0
    for data in f1:
        rating += data.rate
    count_rate = 0
    if f2 > 0:
        count_rate = rating / f2
    return render(request, "f_package_detail.html",
                  {'pac': pac, 'fac': f, 'fe': f1, 'package_id': id, 'fc': f2, 'avg': count_rate})


def book(request, id, name_p):
    print("=========\n\n\n\n\n\n\n", name_p)
    u = request.session['client_id']
    c = customer.objects.get(c_id=u)
    today_date = date.today()
    today_date = today_date.strftime('%Y-%m-%d')
    package_id = package.objects.get(package_id=id)
    return render(request, "book.html",
                  {'packages': package_id, 'cus': c, 'name_p': name_p, 'today_date': today_date})


def bookroom(request, id, name_p):
    print("=========\n\n\n\n\n\n\n", name_p)
    u = request.session['client_id']
    c = customer.objects.get(c_id=u)
    room_id = room.objects.get(room_id=id)
    today_date = date.today()
    today_date = today_date.strftime('%Y-%m-%d')
    print("==============", today_date)
    return render(request, "book.html", {'rooms': room_id, 'cus': c, 'name_p': name_p, 'today_date': today_date})


def book_package(request, id):
    print("================================================================")
    if request.method == "POST":
        print("||||||||||||||||||")
        try:
            checkin = request.POST.get("checkin")
            print("|||||||||||||||", checkin)
            checkout = request.POST.get("checkout")
            resort_id = request.POST.get("Resort_id")
            print("================id====", resort_id)
            u = request.session["client_id"]
            p = request.POST.get('amount')
            print("================pay====", p)
            ps = request.POST.get('payment_status')
            print("================pay====", ps)
            pck_id = id
            d = date.today().strftime("%Y-%m-%d")
            print("|||||||||||||||||||||||||||||||||||||||||||||", pck_id)
            # print("|||||||||||||||||||||||||||||||||||||||||||||", roomid)
            print("-------------", u, d)
            ci = str(checkin)
            co = str(checkout)
            r = days_between(ci, co)
            print("[[[[[[[[[[def]]]]]]]]",r)
            if r < 0:
                messages.error(request, "Please Select Valid check out date")
                print("[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]")
                return redirect('/Client/bookresort/%s/package1' % pck_id )
            else:
                C = booking(c_id_id=u, package_id_id=pck_id, Resort_id_id=resort_id, booking_date=d, total=p,
                            checkIn_date=checkin,
                            checkOut_date=checkout, payment_status=ps, booking_status=0, room_id_id=None)
                C.save()
                return redirect('/Client/checkout/')
        except:
            print("-------", sys.exc_info())
    return render(request, 'book.html')


def book_room(request, id):
    print("==========================roomm======================================")
    if request.method == "POST":
        print("||||||||||||||||||")
        try:
            checkin = request.POST.get("checkin")
            print("|||||||||||||||", checkin)
            checkout = request.POST.get("checkout")
            resort_id = request.POST.get("Resort_id")
            print("================id====", resort_id)
            u = request.session["client_id"]
            p = request.POST.get('amount')
            ps = request.POST.get('payment_status')
            print("================pay====", ps)
            pck_id = id
            r = room.objects.filter(room_id=pck_id)
            for val in r:
                p = val.room_id
            print("[[[[[[[[[[[[[[", p)
            d = date.today().strftime("%Y-%m-%d")
            print("|||||||||||||||", d)
            print("[[[[[[[[id]]]]]]", pck_id)
            ci = str(checkin)
            co = str(checkout)
            r = days_between(ci, co)
            if r < 0:
                messages.error(request, "Please Select Valid check out date")
                return redirect('/Client/bookroom/%s/room1' % pck_id)
            else:
                C = booking(c_id_id=u, package_id_id=None, Resort_id_id=resort_id, booking_date=d, total=p,
                            checkIn_date=checkin,
                            checkOut_date=checkout, payment_status=ps, booking_status=0, room_id_id=id)
                C.save()
                return redirect('/Client/room_checkout/')
        except:
            print("-------", sys.exc_info())
    return render(request, 'book.html')


def insert_feedback(request):
    if request.method == "POST":
        try:
            d = date.today()
            disc = request.POST.get("feedback")
            id = request.POST.get("package_id")
            roomid = request.POST.get("room_id")
            uid = request.session["client_id"]
            rating = request.POST['rate']
            print("=====", id)
            print("======++++ date=", d, "feedback", disc, "package id ", id, "customer id ", uid, "Room Id====",
                  roomid)
            f = Feedback(c_id_id=uid, feedback_date=d, feedback=disc, package_id_id=id, rate=rating, room_id_id=None)
            f.save()
            return redirect('/Client/fdetails/%s' % id)
        except:
            print("--------------", sys.exc_info())
    else:
        pass
    return render(request, "f_package_detail.html")


def insert_feedback_room(request):
    print("============================")
    if request.method == "POST":
        try:
            d = date.today()
            disc = request.POST.get("feedback")
            # id = request.POST.get("package_id")
            roomid = request.POST.get("room_id")
            uid = request.session["client_id"]
            rating = request.POST['rate']
            print("=====", id)
            print("======++++ date=", d, "feedback", disc, "customer id ", uid, "Room Id====",
                  roomid)
            f = Feedback(c_id_id=uid, feedback_date=d, feedback=disc, package_id_id=None, rate=rating,
                         room_id_id=roomid)
            f.save()
            return redirect('/Client/rdetails/%s' % roomid)
        except:
            print("--------------", sys.exc_info())
    else:
        pass
    return render(request, "roomdetails.html")


def checkout(request):
    u = request.session['client_id']
    c = customer.objects.get(c_id=u)
    b = booking.objects.filter(c_id_id=u, booking_status=0).exclude(package_id_id=None)
    total = 0
    for val in b:
        id = val.booking_id
        if val.package_id:
            total = total + val.package_id.ammount

    g = (float(total) * (5 / 100))
    gst = float(total) + g
    t = gst * 100
    s = (float(total) * (7 / 100))
    print("++++++++++++++++++++silver dis++++++", s)
    s1 = gst - s
    g1 = (float(total) * (10 / 100))
    g2 = gst - g1
    p = (float(total) * (15 / 100))
    p1 = gst - p
    for val in b:
        ps = val.payment_status
    e = request.session['client_email']
    obj = customer.objects.filter(c_email=e).count()
    if obj == 1:
        val = customer.objects.filter(c_email=e)
        subject = 'Your Booking is confirmed...'
        for data in b:
            if data.payment_status == '2':
                message = f' Your Booking is Confirmed, Your Booking Details are as below...\n'
                message += f' Your Booking id is: {data.booking_id}\n'
                if data.c_id:
                    message += f'\n Customer Name: {data.c_id.c_name}\n'
                if data.package_id:
                    message += f'\n Package Name: {data.package_id.package_name}\n'
                message += f'\n Booking Date: {data.booking_date}\n'
                message += f'\n CheckIn Date: {data.checkIn_date}\n'
                message += f'\n CheckOut Date: {data.checkOut_date}\n'
                message += f'\n Your Total Amount is: {data.total}\n'
                message += f'\n Payment Status: Cash\n'
            else:
                message = f' Your Payment is Pending...\n'
            print("===========booking id----", data.booking_id, "=======total======", data.total)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
    return render(request, "checkout.html", {"book": b, 'cus': c, 'gst': int(g), 'total': int(gst), 'ps': ps,
                                             'silver': int(s), 'gold': int(g1), 'platinum': int(p),
                                             'stotal': int(s1), 'gtotal': int(g2), 'ptotal': int(p1), 't1': t,
                                             'bid': id})


def roomdetail(request, id):
    rooms = room.objects.get(room_id=id)
    r = room.objects.filter(room_id=id)
    s = service.objects.filter(room_id=id)
    f1 = Feedback.objects.filter(room_id=id)
    f2 = Feedback.objects.filter(room_id=id).count()
    rating = 0
    for data in f1:
        rating += data.rate
    count_rate = 0
    if f2 > 0:
        count_rate = rating / f2
    return render(request, "roomdetails.html",
                  {'room': rooms, 'ser': s, 'rooms': r, 'feed': f1, 'fc': f2, 'avg': count_rate})


def get_membership(request, id):
    u = request.session['client_id']
    c = customer.objects.get(c_id=u)
    membership_date = date.today()
    mp_id = Membership_package.objects.filter(Member_id=id)
    for data in mp_id:
        mid = data.Member_id
        print("Member id: ", mid)
    today_date1 = date.today()
    today_date1 = today_date1.strftime('%d-%m-%y')
    today_date2 = date.today()
    today_date2 = today_date2.strftime('%y')
    y = int(today_date2)
    for data in mp_id:
        v = data.validity
        t = y + v
    td = str(t)
    print("===========year========", td)
    today_date3 = date.today()
    today_date3 = today_date3.strftime('%d')
    today_date4 = date.today()
    today_date4 = today_date4.strftime('%m')
    d = int(today_date3)
    m = int(today_date4)
    print("===month=", m, "=====date=", d, "====year==", td)
    y = v + 1
    YEAR_CHOICES = [(r) for r in range(2022, date.today().year + y)]
    print("yEar===========", YEAR_CHOICES)
    y1 = YEAR_CHOICES[-1]
    print("=======year", y1)
    startDate = date(y1, d, m)
    endDate = date(startDate.year, startDate.day, startDate.month)

    print("==========end date===", endDate)
    return render(request, "get_membership.html",
                  {'membership_date': membership_date, 'member': mp_id, 'cus': c, 'mem': mid, 'today_date': today_date1,
                   'ex_year': endDate})


from datetime import datetime


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return ((d2 - d1).days)


def room_checkout(request):
    u = request.session['client_id']
    c = customer.objects.get(c_id=u)
    b = booking.objects.filter(c_id_id=u, booking_status=0).exclude(room_id_id=None)
    print("======================================", b)
    total = 0
    for val in b:
        id = val.booking_id
        if val.room_id:
            t = val.room_id.price
            total = total + val.room_id.price
            cin = val.checkIn_date
            cout = val.checkOut_date
    print("checkin date----", cin, "checkoutdate----", cout)
    ci = str(cin)
    co = str(cout)
    r = abs(days_between(ci, co))
    to = r * t
    print("diff total====", to)
    print("deffrenece==============", r)
    g = (float(to) * (5 / 100))
    gst = float(to) + g
    t = gst * 100
    s = (float(to) * (7 / 100))
    print("++++++++++++++++++++silver dis++++++", s)
    s1 = gst - s
    g1 = (float(to) * (10 / 100))
    g2 = gst - g1
    p = (float(to) * (15 / 100))
    p1 = gst - p
    ps1=0
    for val in b:
        ps1 = val.payment_status
    print("+++++++++++GST++++++++++++++++", g)
    print("===========Final Total=====", gst)
    print("=====================", total)
    e = request.session['client_email']
    obj = customer.objects.filter(c_email=e).count()
    if obj == 1:
        val = customer.objects.filter(c_email=e)
        subject = 'Your Booking is confirmed...'
        for data in b:
            if data.payment_status == '2':
                message = f' Your Booking is Confirmed, Your Booking Details are as below...\n'
                message += f' Your Booking id is: {data.booking_id}\n'
                if data.c_id:
                    message += f'\n Customer Name: {data.c_id.c_name}\n'
                if data.room_id:
                    message += f'\n Package Name: {data.room_id.room_name}\n'
                message += f'\n Booking Date: {data.booking_date}\n'
                message += f'\n CheckIn Date: {data.checkIn_date}\n'
                message += f'\n CheckOut Date: {data.checkOut_date}\n'
                message += f'\n Your Total Amount is: {data.total}\n'
                message += f'\n Payment Status: Cash\n'
            else:
                message = f' Your Payment is Pending...\n'
            print("===========booking id----", data.booking_id, "=======total======", data.total)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
    return render(request, "room_checkout.html", {"book": b, 'cus': c, 'gst': int(g), 'total': int(gst), 'ps': ps1,
                                                  'silver': int(s), 'gold': int(g1), 'platinum': int(p),
                                                  'stotal': int(s1), 'gtotal': int(g2), 'ptotal': int(p1), 't1': t,
                                                  'bid': id, 'def': to})


def blog(request):
    return render(request, "blog.html")


def success(request, id):
    bid = id
    print("===========id=====", bid)
    b = booking.objects.filter(booking_id=bid)
    e = request.session['client_email']
    obj = customer.objects.filter(c_email=e).count()
    if obj == 1:
        val = customer.objects.filter(c_email=e)
        subject = 'Your Payment is Successful'
        message = 0
        for data in b:
            message = f' Your Booking is Confirmed, Your Booking Details are as below...\n'
            message += f' Your Booking id is: {data.booking_id}\n'
            if data.c_id:
                message += f'\n Customer Name: {data.c_id.c_name}\n'
            if data.package_id:
                message += f'\n Package Name: {data.package_id.package_name}\n'
            elif data.room_id:
                message += f'\n Room Name: {data.room_id.room_name}\n'
            message += f'\n Booking Date: {data.booking_date}\n'
            message += f'\n CheckIn Date: {data.checkIn_date}\n'
            message += f'\n CheckOut Date: {data.checkOut_date}\n'
            message += f'\n Your Total Amount is: {data.total}\n'
            message += f'\n Payment Status : Net Banking\n'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
    return render(request, "success.html")


def cencle(request, id):
    bid = id
    b1 = booking.objects.filter(booking_id=bid)
    print("========id=========", bid)
    b1.delete()
    return render(request, "cencle.html")


def mem_cencle(request):
    return render(request, "mem_cencle.html")


def insert_membership(request, id):
    mp_id = Membership_package.objects.filter(Member_id=id)
    dt = date.today().strftime("%Y-%m-%d")
    today_date2 = date.today()
    today_date2 = today_date2.strftime('%y')
    y = int(today_date2)
    for data in mp_id:
        v = data.validity
        t = y + v
    td = str(t)
    today_date3 = date.today()
    today_date3 = today_date3.strftime('%d')
    today_date4 = date.today()
    today_date4 = today_date4.strftime('%m')
    d = int(today_date3)
    m = int(today_date4)
    y = v + 1
    YEAR_CHOICES = [(r) for r in range(2022, datetime.date.today().year + y)]
    print("yEar===========", YEAR_CHOICES)
    y1 = YEAR_CHOICES[-1]
    print("=======year", y1)
    # year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    # a = today_date1.replace(year=today_date1.year + 2)
    startDate = date(y1, d, m)
    endDate = date(startDate.year, startDate.month, startDate.day)
    print("==========end date===", endDate)
    e = request.session['client_id']
    o = customer.objects.filter(c_id=e).update(Member_id=id, membership_date=dt, membership_ex_date=endDate)


def mem_success(request, id):
    mid = id
    print("+++++++++++++++++", mid)
    insert_membership(request, mid)
    return render(request, "mem_success.html")


def error(request):
    return render(request, "404page.html")


def city_name(request):
    c = resort.objects.all()
    print("===============", c)
    return render(request, "header_footer.html", {'city': c})


def goback(request,id):
    bid = id
    b1 = booking.objects.filter(booking_id=bid)
    print("========id=========", bid)
    b1.delete()
    return render(request, "home.html")



