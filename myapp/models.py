from django.db import models

class Login(models.Model):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128)
    usertype=models.CharField(max_length=50, default=0)
    status=models.IntegerField(default=0)


class Registration(models.Model):
    SKIN_TYPE_CHOICES = [
        ("dry", "Dry"),
        ("oily", "Oily"),
        ("combination", "Combination"),
        ("sensitive", "Sensitive"),
        ("normal", "Normal"),
    ]
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES, null=True, blank=True)
    name=models.CharField(max_length=100)
    age=models.CharField(max_length=3)
    gender=models.CharField(max_length=10,default='other')
    contact=models.CharField(max_length=15)
    loginid=models.OneToOneField(Login,on_delete=models.CASCADE,related_name='patient')
   

class Doctor(models.Model):
    name=models.CharField(max_length=100)
    age=models.CharField(max_length=3)
    gender=models.CharField(max_length=10,default='other')
    specialization=models.CharField(max_length=25)
    hospital=models.CharField(max_length=50)
    experience=models.CharField(max_length=40)
    qualification=models.CharField(max_length=50)
    contact=models.CharField(max_length=15)
    consultation_fee=models.IntegerField(default=0)
    loginid=models.ForeignKey(Login,on_delete=models.CASCADE)
    
    


class Appointment(models.Model):
    date=models.DateField()
    time=models.CharField(max_length=50)
    loginid=models.ForeignKey(Registration,on_delete=models.CASCADE)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cancel=models.IntegerField(null=True)
    refund_status=models.CharField(max_length=20,default="none")
    payment_status=models.IntegerField(default=0)
    disease=models.CharField(max_length=1000, null=True, blank=True)
    videourl = models.CharField(max_length=1000, null=True, blank=True)
    class Meta:
        # Blocks duplicate (doctor + date + time) at DB level.
        # cancel=1 (cancelled) rows are EXCLUDED from the booked query
        # above, so a cancelled slot becomes bookable again automatically.
        unique_together = [("doctor_id", "date", "time")]





class Prescription(models.Model):
    prescription=models.CharField(max_length=500)
    appoint_id=models.ForeignKey(Appointment,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    name=models.CharField(max_length=100)
    card_number=models.CharField(max_length=20,null=True)
    cvv=models.CharField(max_length=10,null=True)
    current_date=models.DateField(auto_now_add=True)
    expiry_date=models.CharField(max_length=20)
    amount=models.IntegerField(null=True)
    appoint_id=models.ForeignKey(Appointment,on_delete=models.CASCADE)
    login_id=models.ForeignKey(Login,on_delete=models.CASCADE,default=0)


class Complaint(models.Model):
    complaint=models.CharField(max_length=200)
    login_id=models.ForeignKey(Login,on_delete=models.CASCADE,default=0)
    current_date=models.DateField(auto_now_add=True)
    reply=models.TextField(null=True,blank=True)
    
class Chat(models.Model):
    message=models.TextField()
    sender=models.ForeignKey(Login,on_delete=models.CASCADE,related_name='sender')
    receiver=models.ForeignKey(Login,on_delete=models.CASCADE,related_name='receiver')
    timestamp=models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    feedback=models.CharField(max_length=200)
    login_id=models.ForeignKey(Login,on_delete=models.CASCADE,default=0)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    current_date=models.DateField(auto_now_add=True)
    rating=models.IntegerField(null=True)

    

class slot(models.Model):
    d_id = models.ForeignKey('Doctor', on_delete=models.CASCADE)

    slot_date = models.DateField(null=True, blank=True)
    weekday = models.IntegerField(null=True, blank=True)  # 0=Mon ... 6=Sun

    starttime = models.TimeField()
    endtime = models.TimeField()

    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)

    currentdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Prevent duplicates for weekly schedule entries
            models.UniqueConstraint(fields=["d_id", "weekday"], name="uniq_doctor_weekday_slot"),
            # Prevent duplicates for date-specific entries
            models.UniqueConstraint(fields=["d_id", "slot_date"], name="uniq_doctor_date_slot"),
        ]

