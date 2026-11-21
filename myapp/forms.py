from django import forms
from .models import *

class RegistrationForm(forms.Form):
    name=forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder":"Enter your name"})

    )
    age = forms.CharField(
                 label="Age", max_length=3, widget=forms.TextInput(attrs={"placeholder": "Enter your age"})
        )
    gender = forms.ChoiceField(
        label="Gender", choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
        )
    skin_type = forms.ChoiceField(
        label="skin_type", choices=[('dry', 'Dry'), ('oily', 'Oily'), ('combination', 'Combination'),('sensitive', 'Sensitive'),('normal', 'Normal')]
        )

    contact=forms.CharField(
        label="Contact",
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder":"Enter your contact"})
    )
    

    email=forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder":"Enter your email"})

    )

    password=forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"})
    )

class LoginForm(forms.Form):
    email=forms.EmailField(
    label="Email",
    widget=forms.EmailInput(attrs={"placeholder":"Enter your email"})

    )
    password=forms.CharField(
    label="Password",
    widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"})
    )

class DoctorRegister(forms.Form):
     name=forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder":"Enter your name"})

    )
     age = forms.CharField(
                 label="Age", max_length=3, widget=forms.TextInput(attrs={"placeholder": "Enter your age"})
        )
     gender = forms.ChoiceField(
        label="Gender", choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
        )

     contact=forms.CharField(
        label="Contact",
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder":"Enter your contact"})
    )
     specialization = forms.ChoiceField(
        label="Specialization",
        choices=[
        ('general', 'General Dermatology'),
        ('cosmetic', 'Cosmetic Dermatology'),
        ('pediatric', 'Pediatric Dermatology'),
        ('Trichology', 'Trichology'),
        ('laser', 'Laser Dermatology'),
    ]
)
     hospital = forms.CharField(
       label="Hospital", max_length=40, widget=forms.TextInput(attrs={"placeholder": "Enter your hospital"})
       
    )
     experience= forms.CharField(
                 label="Experience", max_length=40, widget=forms.TextInput(attrs={"placeholder": "Enter your experience"})
    )
     qualification=forms.ChoiceField(
        label="Qualification",
        choices=[
        ('mbbsmd', 'MBBS-MD'),
        ('mbbsdnb', 'MBBS-DNB'),
        ('mbbsdvd', 'MBBS-DVD'),
        ]
        
       
    )
     consultation_fee=forms.IntegerField(
        label="Consultation Fee",
        widget=forms.TextInput(attrs={"placeholder":"Enter Your Consultation Fee"})

    )
     email=forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder":"Enter your email"})

    )

     password=forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"})
    )
     
class PROFILE_DOCTOR(forms.ModelForm):
    
        class Meta:
          model= Doctor
          fields=['name','age','gender','specialization','hospital','experience','qualification','contact','consultation_fee']

class LOGIN_EDIT(forms.ModelForm):
       class Meta:
            model=Login
            fields=['email']
class PROFILE_USER(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'age', 'gender', 'contact', 'skin_type']
        widgets = {
            'skin_type': forms.Select(attrs={'class': 'input-seamless form-select'}),
        }


class APPOINTMENT(forms.ModelForm):
        class Meta:
           model= Appointment
           fields=['date','time']

class PRESCRIPTION(forms.ModelForm):
     class Meta:
          model= Prescription
          fields=['prescription']

class PAYMENT(forms.ModelForm):
     class Meta:
          model= Payment
          fields=['name','card_number','cvv','expiry_date']

class COMPLAINT(forms.ModelForm):
     class Meta:
          model=Complaint
          fields=['complaint']

class COMPLAINTREPLY(forms.ModelForm):
     class Meta:
          model=Complaint
          fields=['reply']

class FEEDBACK(forms.ModelForm):
     class Meta:
          model=Feedback
          fields=['feedback','rating']





class TimeslotForm(forms.ModelForm):
    MODE_CHOICES = [
        ("single", "Single day"),
        ("recurring", "Repeat for a period"),
    ]

    WEEKDAY_CHOICES = [
        ("0", "Monday"),
        ("1", "Tuesday"),
        ("2", "Wednesday"),
        ("3", "Thursday"),
        ("4", "Friday"),
        ("5", "Saturday"),
        ("6", "Sunday"),
    ]

    mode = forms.ChoiceField(
        choices=MODE_CHOICES,
        widget=forms.RadioSelect,
        initial="single",
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        help_text="First day to apply the schedule",
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        help_text="Last day to apply the schedule",
    )
    weekdays = forms.MultipleChoiceField(
        required=False,
        choices=WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Pick at least one weekday",
    )

    class Meta:
        model = slot
        fields = ["slot_date", "starttime", "endtime", "break_start", "break_end"]
        widgets = {
            "slot_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "starttime": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "endtime": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "break_start": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "break_end": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }

from django.utils import timezone
 
def clean(self):
    cleaned = super().clean()
    today = timezone.localdate()          # ← respects your TIME_ZONE setting
 
    mode        = cleaned.get("mode")
    slot_date   = cleaned.get("slot_date")
    start_date  = cleaned.get("start_date")
    end_date    = cleaned.get("end_date")
    weekdays    = cleaned.get("weekdays") or []
    starttime   = cleaned.get("starttime")
    endtime     = cleaned.get("endtime")
    break_start = cleaned.get("break_start")
    break_end   = cleaned.get("break_end")
 
    # ── Time validations (unchanged) ────────────────────────
    if starttime and endtime and starttime >= endtime:
        self.add_error("endtime", "End time must be after start time.")
 
    if break_start and break_end:
        if break_start >= break_end:
            self.add_error("break_end", "Break end must be after break start.")
        if starttime and break_start <= starttime:
            self.add_error("break_start", "Break must be within the working window.")
        if endtime and break_end >= endtime:
            self.add_error("break_end", "Break must end before the working window ends.")
 
    # ── Mode validations (past-date checks added) ───────────
    if mode == "single":
        if not slot_date:
            self.add_error("slot_date", "Choose a date for the slot.")
        elif slot_date < today:                               # ← NEW
            self.add_error("slot_date", "Slot date cannot be in the past.")
 
    elif mode == "recurring":
        if not start_date or not end_date:
            self.add_error("start_date", "Select both start and end dates.")
        else:
            if start_date < today:                            # ← NEW
                self.add_error("start_date", "Start date cannot be in the past.")
            if end_date < today:                              # ← NEW
                self.add_error("end_date", "End date cannot be in the past.")
            if end_date < start_date:
                self.add_error("end_date", "End date must be on or after start date.")
 
        if not weekdays:
            self.add_error("weekdays", "Pick at least one weekday.")
        cleaned["weekdays"] = [int(day) for day in weekdays]
 
    else:
        self.add_error("mode", "Select a valid scheduling option.")
 
    return cleaned

