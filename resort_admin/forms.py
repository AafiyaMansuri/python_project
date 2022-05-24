from django import forms
from parsley.decorators import parsleyfy
from resort_admin.models import city, service, facilities, package, gallery, resort, Membership_package, \
    resort_owner, customer, contact, room, booking


@parsleyfy
class customerForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ["c_name","c_email","password","contact_no","address","pincode",'Is_admin']


class cityForm(forms.ModelForm):
    class Meta:
        model = city
        fields = ["city_name"]


class memberForm(forms.ModelForm):
    pack_img = forms.FileField()
    class Meta:
        model = Membership_package
        fields = ["Package_name", "m_description", "Ammount","validity", "pack_img"]


class resortForm(forms.ModelForm):
    cover_image = forms.FileField()
    class Meta:
        model = resort
        fields = ["Resort_address", "r_description","cover_image","city_id"]


class galleryForm(forms.ModelForm):
    g_image = forms.FileField()
    class Meta:
        model = gallery
        fields = ["g_image", "Resort_id"]


class packageForm(forms.ModelForm):
    image_path = forms.FileField()
    class Meta:
        model = package
        fields = ["package_name","room_id", "ammount", "p_Description", "Resort_id", "image_path"]


class facilitiesForm(forms.ModelForm):
    class Meta:
        model = facilities
        fields = ["f_description", "package_id"]


class serviceForm(forms.ModelForm):
    class Meta:
        model = service
        fields = [ "service_d", "room_id"]


class ownerForm(forms.ModelForm):

    class Meta:
        model=resort_owner
        fields=["owner_name", "owner_email", "owner_pass", "owner_contactno", "owner_address", "Resort_id"]


class serviceImageupd(forms.ModelForm):
    service_image = forms.FileField()

    class Meta:
        model = service
        fields = ["service_image"]


class galleryImageupd(forms.ModelForm):
    g_image = forms.FileField()

    class Meta:
        model = gallery
        fields = ["g_image"]


class packageImageupd(forms.ModelForm):
    image_path = forms.FileField()

    class Meta:
        model = package
        fields = ["image_path"]


class QueryForm(forms.ModelForm):

    class Meta:
        model = contact
        fields = ["name", "number", "email", "dis"]


class updateForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ["c_name", "c_email", "contact_no", "address", "pincode", 'Is_admin']


class Password(forms.ModelForm):
    class Meta:
        model = customer
        fields = ["c_email", 'password']


class roomForm(forms.ModelForm):
    room_img = forms.FileField()
    class Meta:
        model = room
        fields = ["Resort_id", "room_des", "room_name","price","room_img"]


class bookpackage(forms.ModelForm):
    class Meta:
        model = booking
        fields = ["checkIn_date", "checkOut_date"]
