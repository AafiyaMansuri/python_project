from django.db import models


# Create your models here.
class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50)

    class Meta:
        db_table = "city"


class Membership_package(models.Model):
    Member_id = models.AutoField(primary_key=True)
    Package_name = models.CharField(max_length=50)
    m_description = models.CharField(max_length=500)
    Ammount = models.IntegerField()
    validity = models.IntegerField()
    pack_img = models.CharField(max_length=150)

    # Member_image = models.CharField(null=True)

    class Meta:
        db_table = "Membership_package"


class customer(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=50)
    c_email = models.EmailField(max_length=50)
    password = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    Is_admin = models.IntegerField()
    Member_id = models.ForeignKey(Membership_package, on_delete=models.CASCADE, null=True)
    membership_date = models.DateField(null=True)
    membership_ex_date = models.DateField(null=True)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField(null=True)

    class Meta:
        db_table = "customer"


class resort(models.Model):
    Resort_id = models.AutoField(primary_key=True)
    Resort_address = models.CharField(max_length=200)
    r_description = models.CharField(max_length=1000)
    cover_image = models.CharField(max_length=150)
    city_id = models.ForeignKey(city, on_delete=models.CASCADE)

    class Meta:
        db_table = "resort"


class gallery(models.Model):
    Gallery_id = models.AutoField(primary_key=True)
    g_image = models.CharField(max_length=150)
    Resort_id = models.ForeignKey(resort, on_delete=models.CASCADE)

    class Meta:
        db_table = "gallery"


class room(models.Model):
    room_id = models.AutoField(primary_key=True)
    Resort_id = models.ForeignKey(resort, on_delete=models.CASCADE)
    room_des = models.CharField(max_length=500)
    room_name = models.CharField(max_length=60)
    price = models.IntegerField()
    room_img = models.CharField(max_length=150)

    class Meta:
        db_table = "room"


class package(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=50)
    ammount = models.IntegerField()
    p_Description = models.CharField(max_length=1000)
    Resort_id = models.ForeignKey(resort, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=100)
    room_id=models.ForeignKey(room,on_delete=models.CASCADE)

    class Meta:
        db_table = "package"


class booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    c_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    Resort_id = models.ForeignKey(resort, on_delete=models.CASCADE)
    room_id = models.ForeignKey(room, on_delete=models.CASCADE, null=True)
    package_id = models.ForeignKey(package, on_delete=models.CASCADE, null=True)
    booking_date = models.DateField()
    checkIn_date = models.DateField()
    checkOut_date = models.DateField()
    payment_status = models.CharField(max_length=20)
    booking_status = models.IntegerField()
    total=models.IntegerField()

    class Meta:
        db_table = "booking"


class review(models.Model):
    review_id = models.AutoField(primary_key=True)
    c_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    review = models.CharField(max_length=100)
    review_date = models.DateField()
    Resort_id = models.ForeignKey(resort, on_delete=models.CASCADE)

    class Meta:
        db_table = "review"


class facilities(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_description = models.CharField(max_length=100)
    package_id = models.ForeignKey(package, on_delete=models.CASCADE)

    class Meta:
        db_table = "facilities"


class service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_d = models.CharField(max_length=100)
    room_id = models.ForeignKey(room, on_delete=models.CASCADE)

    class Meta:
        db_table = "service"


class resort_owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    Resort_id = models.ForeignKey(resort, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=50)
    owner_email = models.EmailField(max_length=50)
    owner_pass = models.CharField(max_length=30)
    owner_contactno = models.CharField(max_length=15)
    owner_address = models.CharField(max_length=100)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField(null=True)

    class Meta:
        db_table = "resort_owner"


class contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    number = models.CharField(max_length=15)
    email = models.EmailField(max_length=60)
    dis = models.CharField(max_length=200)

    class Meta:
        db_table = "contact"


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    c_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    package_id = models.ForeignKey(package, on_delete=models.CASCADE, null=True)
    room_id = models.ForeignKey(room, on_delete=models.CASCADE, null=True)
    feedback = models.CharField(max_length=200)
    rate = models.IntegerField()
    feedback_date = models.DateField()

    class Meta:
        db_table = "Feedback"


