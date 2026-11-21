from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.db import IntegrityError
from .models import *
from .forms import *
from django.db.models import Q



from datetime import datetime, timedelta
from django.db import IntegrityError
from django.utils import timezone


def build_15min_slots(start_time, end_time, step=15):
    base = datetime(2000, 1, 1)
    s = datetime.combine(base.date(), start_time)
    e = datetime.combine(base.date(), end_time)

    out = []
    cur = s
    while cur + timedelta(minutes=step) <= e:
        out.append(cur.time())
        cur += timedelta(minutes=step)
    return out


def in_break(t, b1, b2):
    if not b1 or not b2:
        return False
    return b1 <= t < b2




# Create your views here.
def login2(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user=Login.objects.get(email=email)
                print(user)
                if check_password(password,user.password):
                    if user.usertype=='user':
                        request.session['userid']=user.id
                        return redirect('user')
                    elif user.usertype=='doctor' and user.status == 1:
                        request.session['userid']=user.id
                        return redirect('doctorhome')
                    elif user.usertype=='admin':
                        request.session['userid']=user.id
                        return redirect('adminhome')
                   
                else:
                    messages.error(request,'Invalid Password')
            except Login.DoesNotExist:
                messages.error(request,'User does not exist')
    else:
        form=LoginForm
    return render(request,"login2.html",{'form':form})


def logout(request):
    request.session.flush()
    return redirect('login2')

def adminhome(request):
   
    doctor_count = Doctor.objects.count()
    patient_count = Registration.objects.count()
    
 
    feedback_list = Feedback.objects.select_related('login_id', 'doctor_id').all().order_by('-id')[:5]
    complaint = Complaint.objects.select_related('login_id').all().order_by('-id')[:5]

    context = {
        'doc_count': doctor_count,
        'patient_count': patient_count,
        'feedback_list': feedback_list,
        'complaints_list':complaint,
    }
    
    return render(request, "admin.html", context)

def index(request):
    # Fetch counts for the stats section
    doctor_count = Doctor.objects.count()
    patient_count = Registration.objects.count()

    # Fetch the latest feedbacks (limited to 6 for the carousel)
    feedback_list = Feedback.objects.all().order_by('-id')[:6]

    # Pass all data to the template
    return render(request, "index.html", {
        "doctor_count": doctor_count,
        "patient_count": patient_count,
        "feedback_list": feedback_list
    })

def user(request):
    return render(request,"user.html")

def doctorhome(request):
    return render(request,"doctorhome.html")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                logid = Login.objects.create(
                    email=form.cleaned_data["email"],
                    password=make_password(form.cleaned_data["password"]),
                    usertype='user',
                )
                
                # FIX: Add skin_type here
                reg = Registration.objects.create(
                    name=form.cleaned_data["name"],
                    age=form.cleaned_data["age"],
                    gender=form.cleaned_data["gender"],
                    contact=form.cleaned_data["contact"],
                    skin_type=form.cleaned_data["skin_type"], # <--- ADD THIS LINE
                    loginid=logid
                )
                return redirect("login2")
            except IntegrityError:
                form.add_error("email", "This email is already registered")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})
def docreg(request):
    if request.method == "POST":
        form=DoctorRegister(request.POST)
        print(form)
        if form.is_valid():
            print(form)
            try:
                logid=Login.objects.create(
                    email=form.cleaned_data["email"],
                    password=make_password(form.cleaned_data["password"]),
                    usertype='doctor',
                )
                print(logid)
                regi=Doctor.objects.create(
                    name=form.cleaned_data["name"],
                    age=form.cleaned_data["age"],
                    gender=form.cleaned_data["gender"],
                    specialization=form.cleaned_data["specialization"],
                    hospital=form.cleaned_data["hospital"],
                    experience=form.cleaned_data["experience"],
                    qualification=form.cleaned_data["qualification"],
                    contact=form.cleaned_data["contact"],
                    consultation_fee=form.cleaned_data["consultation_fee"],
                    loginid=logid
                )
                print(regi)
                return redirect("login2")
            except IntegrityError:
                form.add_error("email","this email is already registered")
    else:
        form=DoctorRegister()
    return render(request,"docreg.html",{"form":form})

def datatables(request):
    users=Registration.objects.all()
    return render(request,"datatables.html",{"users":users})

def doctorlist(request):
    doc=Doctor.objects.select_related('loginid').all()
    return render(request,"doctorlist.html",{"doc":doc})

def request_refund(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        # logic: Change status to 2 (Refunded) after they click submit
        appointment.cancel = 2 
        # Optional: appointment.refund_reason = request.POST.get('reason')
        appointment.save()
        
        messages.success(request, "Refund processed successfully!")
        return redirect('userappoint')

    # Shows the refund page for the specific appointment
    return render(request, 'request_refund.html', {'p': appointment})

def profiledoc(request):
    a=request.session.get('userid')
    if not a:
        return redirect('login2')
    b=get_object_or_404(Doctor,loginid=a)
    c=get_object_or_404(Login,id=a)
    if request.method=='POST':
        form=PROFILE_DOCTOR(request.POST,instance=b)
        login=LOGIN_EDIT(request.POST,instance=c)
        if form.is_valid() and login.is_valid():
            form.save()
            login.save()
            return redirect('doctorhome')
    else:
     form=PROFILE_DOCTOR(instance=b)
     login=LOGIN_EDIT(instance=c)  
    return render(request,"profiledoc.html",{'pro':form,'log':login})

def profileuser(request):
    a=request.session.get('userid')
    if not a:
        return redirect('login2')
    b=get_object_or_404(Registration,loginid=a)
    c=get_object_or_404(Login,id=a)
    if request.method=='POST':
        form=PROFILE_USER(request.POST,instance=b)
        login=LOGIN_EDIT(request.POST,instance=c)
        if form.is_valid() and login.is_valid():
            form.save()
            login.save()
            return redirect('user')
    else:
        form=PROFILE_USER(instance=b)
        login=LOGIN_EDIT(instance=c)
    return render(request,"profileuser.html",{'pro':form,"log":login})

# def docsearch(request):
#     users=Registration.objects.all()
#     doc=Doctor.objects.all()
#     search=request.GET.get('search')
#     if search:
#         doc=Doctor.objects.filter(Q(name__icontains=search)|Q(hospital__icontains=search)|Q(specialization__icontains=search))
#     return render(request,"docsearch.html",{"users":users,"doc":doc})

def docsearch(request):
    a=request.session.get('userid')
    if not a:
        return redirect('login2')
    users = Registration.objects.all()
    doc = Doctor.objects.all()
    
    # Use login_id and doctor_id to fetch related data in one go
    feedbacks = Feedback.objects.select_related('login_id', 'doctor_id').all().order_by('-id')[:6]

    search = request.GET.get('search')
    if search:
        doc = Doctor.objects.filter(
            Q(name__icontains=search) | 
            Q(hospital__icontains=search) | 
            Q(specialization__icontains=search)
        )
    
    return render(request, "docsearch.html", {
        "users": users, 
        "doc": doc, 
        "feedback_list": feedbacks
    })

def admin_feedback_view(request):
    # Fetch all feedback objects
    feedbacks = Feedback.objects.all().order_by('-id')
    
    # Pass them to the template
    return render(request, 'adminfeedback.html', {'feedbacks': feedbacks})

# def appointment(request, doctor_id):
#     doctor=get_object_or_404(Doctor,id=doctor_id)
#     print(doctor)
#     a=request.session.get('userid')
#     c=get_object_or_404(Registration,loginid=a)
#     if request.method == "POST":
#         form=APPOINTMENT(request.POST)
#         #print(form)
#         if form.is_valid():
#             d=form.save(commit=False)
#             d.doctor_id=doctor
#             d.loginid=c
#             d.save()
#             return redirect("payment",d.id,doctor.consultation_fee)
#     else:
#         form=APPOINTMENT()
#     return render(request,"appointment.html",{"form":form,"doctor":doctor})


# ============================================================
#  views.py  —  appointment booking (fixed)
# ============================================================
from datetime import datetime, timedelta, time as dt_time
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
 
 
def appointment(request, doctor_id):
    login_id = request.session.get('userid')
    if not login_id:
        return redirect('login2')
    patient  = get_object_or_404(Registration, loginid=login_id)
    doctor   = get_object_or_404(Doctor, id=doctor_id)
 
    date_str = request.GET.get("date") or request.POST.get("date")
    selected_date = None
 
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = None
 
    slots = []
 
    if selected_date:
        s = (
            slot.objects.filter(d_id=doctor, slot_date=selected_date).first()
            or slot.objects.filter(d_id=doctor, slot_date__isnull=True).first()
        )
 
        if s:
            all_times = build_15min_slots(s.starttime, s.endtime, step=15)
            all_times = [t for t in all_times if not in_break(t, s.break_start, s.break_end)]
 
            # ── Filter past slots when selected date is today ──────────────
            now = timezone.localtime()
            if selected_date == now.date():
                all_times = [
                    t for t in all_times
                    # FIX: use timezone.make_aware instead of combine(…, tzinfo=…)
                    if timezone.make_aware(
                        datetime.combine(selected_date, t)
                    ) >= now
                ]
 
            # ── Booked slots: store as "HH:MM:SS" strings for comparison ──
            #    Appointment.time is a CharField, so values_list returns strings.
            #    We normalise both sides to "HH:MM:SS" to avoid type mismatch.
            booked_raw = Appointment.objects.filter(
                doctor_id=doctor,
                date=selected_date,
                cancel=0,           # only active (not cancelled) appointments
            ).values_list("time", flat=True)
 
            # Normalise DB values → "HH:MM:SS" (handles "HH:MM" edge cases too)
            booked = set()
            for raw in booked_raw:
                raw = str(raw).strip()
                if len(raw) == 5:          # "HH:MM"  → "HH:MM:SS"
                    raw = raw + ":00"
                booked.add(raw)
 
            for t in all_times:
                time_str = t.strftime("%H:%M:%S")   # always "HH:MM:SS"
                slots.append({
                    "value":    time_str,
                    "label":    t.strftime("%I:%M %p"),
                    "disabled": time_str in booked,   # FIX: compare strings to strings
                })
 
    # ── Handle POST (save booking) ─────────────────────────────────────────
    if request.method == "POST":
        form = APPOINTMENT(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.loginid    = patient
            a.doctor_id  = doctor
            a.cancel     = 0
 
            if not selected_date:
                form.add_error("date", "Please select a valid date.")
            else:
                a.date = selected_date
 
                # Build the set of currently-allowed slot strings
                allowed = {x["value"] for x in slots if not x["disabled"]}
 
                # Normalise the submitted time value
                chosen = str(a.time).strip()
                if len(chosen) == 5:
                    chosen = chosen + ":00"
 
                if chosen not in allowed:
                    form.add_error(
                        "time",
                        "This slot is not available. Please choose another."
                    )
                else:
                    try:
                        with transaction.atomic():
                            a.save()
                        return redirect("payment", a.id, doctor.consultation_fee)
                    except IntegrityError:
                        # Caught by the DB unique_together constraint (see model below)
                        form.add_error(
                            "time",
                            "This slot was just booked by someone else. Please choose another."
                        )
        # form invalid — fall through and re-render with errors
    else:
        form = APPOINTMENT(initial={"date": date_str})
 
    return render(request, "appointment.html", {
        "form":          form,
        "doctor":        doctor,
        "selected_date": selected_date.strftime("%Y-%m-%d") if selected_date else "",
        "slots":         slots,
    })







def payment(request,appoint_id,consultation_fee):
      g=int(consultation_fee)
      a= request.session.get('userid')
      if not a:
        return redirect('login2')
      b= get_object_or_404(Login,id=a)
      appoint=get_object_or_404(Appointment,id=appoint_id)
      print(a)
      if request.method=="POST":
          form=PAYMENT(request.POST)
          if form.is_valid():
              Payment.objects.create(
                name=form.cleaned_data["name"],
                card_number=form.cleaned_data["card_number"],
                cvv=form.cleaned_data["cvv"],          
                expiry_date=form.cleaned_data["expiry_date"],
                amount=g,
                appoint_id=appoint,
                login_id=b              
                )
              appoint.payment_status=1
              appoint.save()
              return redirect('userappoint')
      else:
          form=PAYMENT()
      return render(request,"payment.html",{"form":form})

def userheader(request):
    
    return render(request,"userheader.html")

def appointlist(request):
    a = request.session.get('userid')
    if not a:
        return redirect('login2')
    b = get_object_or_404(Doctor, loginid=a)
    # Select related fields to reduce queries
    c = Appointment.objects.filter(doctor_id=b,payment_status=1)
    search=request.GET.get('search')
    if search:
        c=Appointment.objects.filter(Q(date__icontains=search)|Q(time__icontains=search))
    return render(request, "appointlist.html", {"users":c})

def userappoint(request):
    user_id = request.session.get('userid')
    if not user_id:
        return redirect('login2')
    user_profile = get_object_or_404(Registration, loginid=user_id)
    
    search = request.GET.get('search')
    appointments = Appointment.objects.filter(loginid=user_profile)
    
    if search:
        appointments = appointments.filter(Q(doctor_id__name__icontains=search))
        
    return render(request, "userappoint.html", {"users": appointments})

def editappoint(request,appoint_id):
    a=get_object_or_404(Appointment,id=appoint_id)
    b = request.session.get('userid')
    if not b:
        return redirect('login2')
    if request.method == "POST":
        form = APPOINTMENT(request.POST,instance=a)
        if form.is_valid():   
            form.date = form.cleaned_data["date"]
            form.time = form.cleaned_data["time"]
            form.save()
            return redirect("userappoint")
    else:
        form=APPOINTMENT(instance=a)
    return render(request, "editappoint.html", {"form": form})



def editprescription(request,prescription_id,appoint_id):
    a=get_object_or_404(Prescription,id=prescription_id)
    b=get_object_or_404(Appointment,id=appoint_id)
    if request.method == "POST":
        form= PRESCRIPTION(request.POST,instance=a)
        if form.is_valid():
            form.prescription=form.cleaned_data["prescription"]
            form.save()
            return redirect("prescription",b.id)
    else:
        form= PRESCRIPTION(instance=a)
    return render(request,"editprescription.html",{"form":form})

def deleteprescription(request,prescription_id,appoint_id):
    a=get_object_or_404(Prescription,id=prescription_id)
    b=get_object_or_404(Appointment,id=appoint_id)
    a.delete()
    return redirect("prescription",b.id)
    
def appointcancel(request,appoint_id):
     a=get_object_or_404(Appointment,id=appoint_id)
     a.cancel=1
     a.save()
     return redirect("userappoint")

def prescription(request, appoint_id):
    appoint=get_object_or_404(Appointment,id=appoint_id)
    print(appoint)
    prescriptions=Prescription.objects.filter(appoint_id=appoint_id)
    a=request.session.get('userid')
    c=get_object_or_404(Doctor,loginid=a)
    if request.method == "POST":
        form=PRESCRIPTION(request.POST)
        #print(form)
        if form.is_valid():
            Prescription.objects.create(
                 prescription=form.cleaned_data["prescription"],
                 appoint_id=appoint,      
                 )
            return redirect("appointlist")
    else:
        form=PRESCRIPTION()
    return render(request,"prescription.html",{"form":form,"appoint":appoint,"pre":prescriptions})

def userprescription(request,appoint_id):
    a=get_object_or_404(Appointment,id=appoint_id)
    b=request.session.get('userid')
    if not b:
        return redirect('login2')
    c=get_object_or_404(Registration,loginid=b)
    d=Prescription.objects.filter(appoint_id=a.id )
    print(d)
    return render(request, "userprescription.html",{"form":d})

def complaint(request):
    a=request.session.get('userid')
    if not a:
        return redirect('login2')
    c=get_object_or_404(Login,id=a)
    if request.method == "POST":
        form=COMPLAINT(request.POST)
        if form.is_valid():
            Complaint.objects.create(
                 complaint=form.cleaned_data["complaint"],
                 login_id=c
                 )
            return redirect("user")
    else:
        form=COMPLAINT()
    return render(request,"complaint.html",{"form":form})

def admincomplaintview(request):
    a=Complaint.objects.all().select_related('login_id__patient')
    return render(request,"admincomplaint.html",{"a":a})

def editcomplaint(request,complaint_id):
    a=get_object_or_404(Complaint,id=complaint_id)
    b=request.session.get('userid')
    if not b:
        return redirect('login2')
    c=get_object_or_404(Login,id=b)
    if request.method == "POST":
        form= COMPLAINT(request.POST,instance=a)
        if form.is_valid():
            form.complaint=form.cleaned_data["complaint"]
            form.save()
            return redirect("viewcomplaint")
    else:
        form= COMPLAINT(instance=a)
    return render(request,"editcomplaint.html",{"form":form})

def deletecomplaint(request,complaint_id):
    a=get_object_or_404(Complaint,id=complaint_id)
    b=request.session.get('userid')
    if not b:
        return redirect('login2')
    c=get_object_or_404(Registration,loginid=b)
    a.delete()
    return redirect("viewcomplaint")

def viewcomplaint(request):
    b=request.session.get('userid')
    if not b:
        return redirect('login2')
    c=get_object_or_404(Login,id=b)
    d=Complaint.objects.filter(login_id=c.id )
    print(d)
    return render(request, "viewcomplaint.html",{"form":d})

def complaintreply(request,complaint_id):
    a=request.session.get('userid')
    if not a:
        return redirect('login2')
    b=get_object_or_404(Login,id=a)
    c=get_object_or_404(Complaint,id=complaint_id)
    if request.method=='POST':
        form=COMPLAINTREPLY(request.POST,instance=c)
        if form.is_valid():
            form.save()
            return redirect('admincomplaint')
    else:
        form=COMPLAINTREPLY(instance=c)    
    return render(request,"complaintreply.html",{"form":form})



# def chat(request, user_id):
#     login_id = request.session.get('userid')

#     if not login_id:
#         return redirect('login2')

#     current_user = get_object_or_404(Login, id=login_id)
#     other_user = get_object_or_404(Login, id=user_id)

#     messages = Chat.objects.filter(
#         Q(sender=current_user, receiver=other_user) |
#         Q(sender=other_user, receiver=current_user)
#     ).order_by('timestamp')

#     return render(request, 'chat.html', {
#         'messages': messages,
#         'other_user': other_user,
#         'current_user': current_user,
#     })



def chat(request, user_id):
    login_id = request.session.get('userid')
    if not login_id:
        return redirect('login2')
 
    current_user = get_object_or_404(Login, id=login_id)
    other_user   = get_object_or_404(Login, id=user_id)
 
    # ── Resolve display name for current logged-in user ──────
    # Check Doctor first, then Registration (patient)
    try:
        current_name = current_user.doctor_set.first().name  # Doctor has ForeignKey to Login
    except AttributeError:
        try:
            current_name = current_user.patient.name         # Registration has OneToOne 'patient'
        except AttributeError:
            current_name = current_user.email
 
    # ── Resolve display name for the other user ───────────────
    try:
        other_name = other_user.doctor_set.first().name
    except AttributeError:
        try:
            other_name = other_user.patient.name
        except AttributeError:
            other_name = other_user.email
 
    # ── Patient list for sidebar (exclude current user) ───────
    patient_list = Login.objects.exclude(id=current_user.id)
 
    # ── Message history ───────────────────────────────────────
    messages = Chat.objects.filter(
        Q(sender=current_user, receiver=other_user) |
        Q(sender=other_user,   receiver=current_user)
    ).order_by('timestamp')
 
    return render(request, 'chat.html', {
        'messages':     messages,
        'other_user':   other_user,
        'current_user': current_user,
        'patient_list': patient_list,
        'current_name': current_name,   # ← resolved real name
        'other_name':   other_name,     # ← resolved real name
    })


from django.http import HttpResponseForbidden

def send_message(request):
    if request.method != "POST":
        return HttpResponseForbidden("Invalid request method")

    login_id = request.session.get('userid')
    if not login_id:
        return redirect('login2')

    sender = get_object_or_404(Login, id=login_id)

    receiver_id = request.POST.get('receiver_id')
    if not receiver_id:
        return redirect('chat', user_id=sender.id)

    receiver = get_object_or_404(Login, id=receiver_id)

    message = request.POST.get('message')
    if message:
        Chat.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )

    return redirect('chat', user_id=receiver.id)

def feedback(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user_id = request.session.get('userid')
    if not user_id:
        return redirect('login2')
    
    # Fetch the data using the correct column 'login_id'
    # We name the variable 'feedback' to match your HTML loop exactly
    user_data = Feedback.objects.filter(doctor_id=doctor_id, login_id=user_id)

    if request.method == "POST":
        feedback_text = request.POST.get('feedback')
        rating_value = request.POST.get('rating', 0)
        user_login = get_object_or_404(Login, id=user_id)
        
        Feedback.objects.create(
            doctor_id=doctor,
            login_id=user_login,
            feedback=feedback_text,
            rating=rating_value
        )
        # Stay on the feedback page to see the new entry
        return redirect('feedback', doctor_id=doctor_id)

    context = {
        'doctor': doctor,
        'feedback': user_data, # This MUST match {% for a in feedback %}
    }
    return render(request, 'feedback.html', context)

def editfeedback(request, feedback_id):
    # Fetch the specific feedback the user wants to change
    a = get_object_or_404(Feedback, id=feedback_id)
    user_id = request.session.get('userid')
    if not user_id:
        return redirect('login2')
    
    if request.method == "POST":
        # Pass the new POST data to the existing record 'a'
        form = FEEDBACK(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return redirect("userappoint")
    else:
        # Pre-fill the form with the current record 'a'
        form = FEEDBACK(instance=a)
        
    return render(request, "editfeedback.html", {"form": form})


def deletefeedback(request, feedback_id):
    feedback_item = get_object_or_404(Feedback, id=feedback_id)
    user_id = request.session.get('userid')
    if not user_id:
        return redirect('login2')

    # Security check: Does this record belong to the current user?
    if feedback_item.login_id_id == user_id:
        doc_id = feedback_item.doctor_id_id
        feedback_item.delete()
        return redirect('feedback', doctor_id=doc_id)
    
    return redirect('userappoint')

# def editfeedback(request,feedback_id):
#     a=get_object_or_404(Feedback,id=feedback_id)
#     b=request.session.get('userid')
#     c=get_object_or_404(Login,id=b)
#     if request.method == "POST":
#         form= FEEDBACK(request.POST,instance=a)
#         if form.is_valid():
#             form.feedback=form.cleaned_data["feedback"]
#             form.save()
#             return redirect("userappoint")
#     else:
#         form= FEEDBACK(instance=a)
#     return render(request,"editfeedback.html",{"form":form})

# def deletefeedback(request,feedback_id):
#     a=get_object_or_404(Feedback,id=feedback_id)
#     b=request.session.get('userid')
#     c=get_object_or_404(Registration,loginid=b)
#     a.delete()
#     return redirect("userappoint")


# def feedback(request,doctor_id):
#     doctor=get_object_or_404(Doctor,id=doctor_id)
#     feedback=Feedback.objects.filter(doctor_id=doctor_id)
#     a=request.session.get('userid')
#     c=get_object_or_404(Login,id=a)
#     if request.method == "POST":
#         form=FEEDBACK(request.POST)
#         if form.is_valid():
#             Feedback.objects.create(
#                  feedback=form.cleaned_data["feedback"],
#                  rating=form.cleaned_data["rating"],
#                  login_id=c,
#                  doctor_id=doctor
#                  )
#             return redirect("userappoint")
#     else:
#         form=FEEDBACK()
#     return render(request,"feedback.html",{"form":form,"doctor":doctor,"feedback":feedback})




















from django.shortcuts import render
from PIL import Image
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor
from serpapi import GoogleSearch
import os

# Load model and processor only once
repo_name = "Jayanth2002/dinov2-base-finetuned-SkinDisease"
image_processor = AutoImageProcessor.from_pretrained(repo_name)
model = AutoModelForImageClassification.from_pretrained(repo_name)
HIGH_SEVERITY = {
    "Melanoma",
    "Squamous Cell Carcinoma",
    "Basal Cell Carcinoma",
    # add any others you consider high risk…
}
# Your class names
class_names = [
    'Basal Cell Carcinoma', 'Darier_s Disease', 'Epidermolysis Bullosa Pruriginosa',
    'Hailey-Hailey Disease', 'Herpes Simplex', 'Impetigo', 'Larva Migrans',
    'Leprosy Borderline', 'Leprosy Lepromatous', 'Leprosy Tuberculoid', 'Lichen Planus',
    'Lupus Erythematosus Chronicus Discoides', 'Melanoma', 'Molluscum Contagiosum',
    'Mycosis Fungoides', 'Neurofibromatosis', 'Papilomatosis Confluentes And Reticulate',
    'Pediculosis Capitis', 'Pityriasis Rosea', 'Porokeratosis Actinic', 'Psoriasis',
    'Tinea Corporis', 'Tinea Nigra', 'Tungiasis', 'actinic keratosis', 'dermatofibroma',
    'nevus', 'pigmented benign keratosis', 'seborrheic keratosis',
    'squamous cell carcinoma', 'vascular lesion'
]
# SERPAPI KEY

from django.conf import settings
SERPAPI_API_KEY = settings.SERPAPI_KEY


def search_serpapi(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # First try to get a snippet from the answer box
    if "answer_box" in results and "snippet" in results["answer_box"]:
        snippet = results["answer_box"]["snippet"]
        link = results.get("answer_box", {}).get("link", "https://www.google.com/search?q=" + query)
        return snippet, link

    # Fallback to the first organic result
    elif "organic_results" in results and len(results["organic_results"]) > 0:
        first_result = results["organic_results"][0]
        snippet = first_result.get("snippet", "Information not found.")
        link = first_result.get("link", "https://www.google.com/search?q=" + query)
        return snippet, link

    # If nothing useful is found
    return "Information not found.", "https://www.google.com/search?q=" + query

from django.http import JsonResponse

from django.http import JsonResponse
import torch.nn.functional as F

def predict_skin_disease(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # 1) Load & preprocess
        image = Image.open(request.FILES['image']).convert("RGB")
        inputs = image_processor(images=image, return_tensors="pt")

        # 2) Inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        # 3) Softmax → probs
        probs = F.softmax(logits, dim=-1)[0]
        confidence, idx = torch.max(probs, dim=0)
        confidence = confidence.item()
        idx        = idx.item()

        # 4) Threshold check
        THRESHOLD = 0.6
        if confidence < THRESHOLD:
            return JsonResponse({
                "error": "I’m not confident this is a skin lesion.Please upload a high-resolution image for better analysis.",
                "confidence": confidence
            })

        # 5) Valid prediction
        predicted_class = class_names[idx]

        # 6) Severity check
        if predicted_class in HIGH_SEVERITY:
            return JsonResponse({
                "predicted_class": predicted_class,
                "confidence": round(confidence, 3),
                "alert": (
                  "⚠️ This appears to be a high-risk condition. "
                  "Please consult a dermatologist or healthcare professional as soon as possible."
                )
            })

        # 7) Fetch from web for non-high severity
        remedy_snippet, remedy_link     = search_serpapi(f"home remedy for {predicted_class}")
        medicine_snippet, medicine_link = search_serpapi(f"medicine for {predicted_class}")

        return JsonResponse({
            "predicted_class": predicted_class,
            "confidence": round(confidence, 3),
            "remedy": remedy_snippet,
            "remedy_link": remedy_link,
            "medicine": medicine_snippet,
            "medicine_link": medicine_link
        })

    return render(request, 'skinpredict.html')


def save_disease(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        disease_text = request.POST.get("disease", "").strip()
        if disease_text:
            appointment.disease = disease_text
            appointment.save()
    return redirect("appointlist")




import random

def search_tips_for_disease(topic="general skin care"):
    params = {
        "engine": "google",
        "q": f"tips for {topic}",
        "api_key": SERPAPI_API_KEY,
        "num": 10,  # fetch more results to have more variety
    }

    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])

    tips = []
    links = []

    for res in results:
        snippet = res.get("snippet")
        link = res.get("link")
        if snippet:
            tips.append(snippet)
            links.append(link)

    if not tips:
        return {
            "tips": "📝 No skin care tips found at the moment. Try asking later!",
            "link": "#"
        }

    # Randomly pick 2-3 tips each time
    selected_tips = random.sample(tips, min(3, len(tips)))
    # Randomly pick one source link from available links
    selected_link = random.choice(links) if links else "#"

    return {
        "tips": " ".join(selected_tips),
        "link": selected_link
    }

def search_products_for_disease(topic="skin care", num_results=8):
    # domains = ["sephora.com", "ulta.com", "amazon.com", "nykaa.com", "maccosmetics.com","boots.com", "netmeds.com", "1mg.com", "pharmeasy.in", "dermstore.com"]
    # query = f"best products for {topic}"
    query = f"best products for {topic} skin treatment"


    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results,
    }

    search = GoogleSearch(params)
    results = search.get_dict().get("shopping_results", [])

    products = []
    for r in results:
        # link = r.get("link", "")
        # if not any(domain in link for domain in domains):
        #     continue

        products.append({
            "title": r.get("title"),
            "snippet": r.get("snippet", ""),
            "link":    r.get("link") or r.get("product_link", "#"),
            "image":   r.get("thumbnail") or None,
            "price":   r.get("price", ""),
            "source":  r.get("source", ""),
        })
        if len(products) >= num_results:
            break

    return products



def recommended_products(request):
    user_master = Login.objects.get(id=request.session["userid"])
    reg=get_object_or_404(Registration,loginid=user_master)
    appts = Appointment.objects.filter(loginid=reg, disease__isnull=False)
    diseases = {a.disease.strip() for a in appts if a.disease}

    recommendations = []
    for disease in diseases:
        # FIXED — passes the actual diagnosed condition
        products = search_products_for_disease(topic=disease)
        tips_info = search_tips_for_disease(topic=disease)
        recommendations.append({
            "disease": disease,          # ← add this
            "products": products,
            "tips": tips_info["tips"],
            "tips_link": tips_info["link"]
        })

    return render(request, 'recommended_products.html', {
        "recommendations": recommendations
    })

def fetch_products_from_serpapi(query):
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_API_KEY,  # replace with your actual API key
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    products = []
    for product in results.get("shopping_results", []):
        products.append({
            "title": product.get("title"),
            "link": product.get("link") or product.get("product_link"),  # <-- fallback to product_link
            "price": product.get("price"),
            "thumbnail": product.get("thumbnail"),
        })

    return products
def personalized_products(request):
    
    user_master = Login.objects.get(id=request.session["userid"])

    userinfo = Registration.objects.get(loginid=user_master)

    query = f"skin care products for {userinfo.skin_type} skin for {'men' if userinfo.gender == 'M' else 'women'}"

    products = fetch_products_from_serpapi(query)

    return render(request, "personalized_products.html", {
        "products": products
    })



# import requests
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.conf import settings
# import json
# import re
# from django.http import JsonResponse
# import json
# import requests
# from django.conf import settings

# def chatbot_response(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)  # <-- load JSON from body
#         chat_history = data.get('messages', [])

#         # Extract latest user input
#         if not chat_history or chat_history[-1]['role'] != 'user':
#             return JsonResponse({'reply': "⚠️ Invalid message format."})
        
#         user_input = chat_history[-1]['content']

#         # Check if the message is related to skin
#         skin_keywords = [
#             "skin", "acne", "pimple", "eczema", "rash", "psoriasis", "dermatitis",
#             "itch", "itching", "allergy", "allergic", "burn", "scar", "wrinkle",
#             "melasma", "pigmentation", "dark spots", "dry skin", "oily skin",
#             "redness", "irritation", "blister", "mole", "wart", "freckle","rashes","please","help","product","remedy"
#         ]

#         if not any(keyword in user_input.lower() for keyword in skin_keywords):
#             return JsonResponse({'reply': "⚠️ I can only assist with skin-related health issues. Please ask something about skin care, skin diseases, or skin conditions."})

#         # Send full chat history to NeMoTron API
#         api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
#         headers = {
#             'Authorization': f"Bearer {settings.NEMOTRON_API_KEY}",
#             'Content-Type': 'application/json'
#         }
#         payload = {
#             "model": "nvidia/llama-3.1-nemotron-70b-instruct",
#             "messages": chat_history,
#             "temperature": 0.5,
#             "top_p": 1,
#             "max_tokens": 1024,
#             "stream": False  # or True if you handle streaming
#         }

#         try:
#             response = requests.post(api_url, json=payload, headers=headers)
#             response.raise_for_status()

#             result = response.json()
#             reply_text = result['choices'][0]['message']['content']

#             return JsonResponse({'reply': reply_text})
#         except Exception as e:
#             print(e)
#             return JsonResponse({'reply': "❌ Sorry, something went wrong. Please try again later."})
# def chatbot_response(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('message', '')
        

#         # First, check if the message is related to skin
#         skin_keywords = [
#             "skin", "acne", "pimple", "eczema", "rash", "psoriasis", "dermatitis",
#             "itch", "itching", "allergy", "allergic", "burn", "scar", "wrinkle",
#             "melasma", "pigmentation", "dark spots", "dry skin", "oily skin",
#             "redness", "irritation", "blister", "mole", "wart", "freckle"
#         ]

#         # Simple keyword-based filtering
#         if not any(keyword in user_input.lower() for keyword in skin_keywords):
#             return JsonResponse({'reply': "⚠️ I can only assist with skin-related health issues. Please ask something about skin care, skin diseases, or skin conditions."})

#         # NeMoTron API Endpoint
#         api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
#         headers = {
#             'Authorization': f"Bearer {settings.NEMOTRON_API_KEY}",
#             'Content-Type': 'application/json'
#         }
#         payload = {
#             "model": "nvidia/llama-3.1-nemotron-70b-instruct",
#             "messages": [{"role": "user", "content": user_input}],
#             "temperature": 0.5,
#             "top_p": 1,
#             "max_tokens": 1024,
#             "stream": True
#         }

#         try:
#             # Send request to NeMoTron API
#             response = requests.post(api_url, json=payload, headers=headers, stream=True)

#             if response.status_code == 200:
#                 bot_reply = ""
#                 for line in response.iter_lines():
#                     if line:
#                         try:
#                             line_data = json.loads(line.decode("utf-8").replace("data: ", ""))
#                             delta_content = line_data.get("choices", [{}])[0].get("delta", {}).get("content")
#                             if delta_content:
#                                 bot_reply += delta_content
#                         except json.JSONDecodeError:
#                             continue
#             else:
#                 bot_reply = f"Error: {response.status_code}, {response.text}"

#         except Exception as e:
#             bot_reply = f"API Error: {str(e)}"

#         return JsonResponse({'reply': bot_reply})

#     return JsonResponse({'error': 'Invalid request method.'}, status=400)


# def chatb(request):
#     return render(request, 'chatbot.html')


import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Appointment


def videoconference(request, id):
    a = get_object_or_404(Appointment, id=id)
    return render(request, 'videoconference.html', {'a': a})


def save_appointment_url(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')

            if url:
                appointment = get_object_or_404(Appointment, id=id)
                appointment.videourl = url
                appointment.save()

                return JsonResponse({
                    'success': True,
                    'message': 'URL saved successfully'
                })

            return JsonResponse({
                'success': False,
                'message': 'No URL provided'
            }, status=400)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    }, status=400)








from datetime import timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
 
 
from datetime import timedelta # Don't forget this!

# ============================================================
#  views.py — add this delete_slot view
# ============================================================
 
def delete_slot(request, slot_id):
    """Delete a slot. Only the owning doctor can delete."""
    p = request.session.get('userid')
    q = get_object_or_404(Doctor, loginid=p)
    s = get_object_or_404(slot, id=slot_id, d_id=q)   # ensures doctor owns it
    if request.method == "POST":
        s.delete()
        messages.success(request, "Slot deleted successfully.")
    return redirect('slot')
 
 
# ============================================================
#  views.py — update slotadding to pass slots to template
#  so the panel can show existing slots
# ============================================================
 
def slotadding(request):
    p = request.session.get('userid')
    q = get_object_or_404(Doctor, loginid=p)
 
    if request.method == "POST":
        form = TimeslotForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            base_defaults = {
                "starttime":   data["starttime"],
                "endtime":     data["endtime"],
                "break_start": data.get("break_start"),
                "break_end":   data.get("break_end"),
                "weekday":     None,
            }
 
            created_count = 0
            updated_count = 0
 
            if data["mode"] == "single":
                _, created = slot.objects.update_or_create(
                    d_id=q,
                    slot_date=data["slot_date"],
                    defaults=base_defaults,
                )
                if created:
                    created_count = 1
                else:
                    updated_count = 1
            else:
                selected_weekdays = data["weekdays"]
                current = data["start_date"]
                while current <= data["end_date"]:
                    if int(current.weekday()) in [int(w) for w in selected_weekdays]:
                        _, created = slot.objects.update_or_create(
                            d_id=q,
                            slot_date=current,
                            defaults=base_defaults,
                        )
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                    current += timedelta(days=1)
 
            if created_count and updated_count:
                messages.success(request, f"Created {created_count} and updated {updated_count} slot(s).")
            elif created_count:
                messages.success(request, f"Saved {created_count} slot{'s' if created_count != 1 else ''}.")
            elif updated_count:
                messages.info(request, f"Updated timings for {updated_count} existing slot{'s' if updated_count != 1 else ''}.")
            else:
                messages.warning(request, "No slots were saved. Check that selected weekdays fall within your date range.")
 
            return redirect('slot')
    else:
        form = TimeslotForm()
 
    # ← Pass existing slots to template so panel can display them
    doctor_slots = slot.objects.filter(d_id=q).order_by('slot_date')
 
    return render(request, 'slot.html', {
        'form': form,
        'slots': doctor_slots,   # ← NEW
    })


def doctorapprove(request,id):
    a= get_object_or_404(Login,id=id)
    a.status=1
    a.save()
    return redirect("doctorlist")

def doctorreject(request,id):
    a= get_object_or_404(Login,id=id)
    a.status=2
    a.save()
    return redirect("doctorlist")

import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Login   # change if your model name is different
from django.contrib.auth.hashers import make_password

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = Login.objects.get(email=email)
            otp = str(random.randint(100000, 999999))

            request.session['reset_email'] = email
            request.session['reset_otp'] = otp

            send_mail(
                subject='SkinSense Password Reset OTP',
                message=f'Your OTP for password reset is: {otp}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email.")
            return redirect('verify_otp')

        except Login.DoesNotExist:
            messages.error(request, "Email not found.")

    return render(request, 'forgot_password.html')


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("reset_otp")

        if entered_otp == session_otp:
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP.")

    return render(request, 'verify_otp.html')


def reset_password(request):
    if not request.session.get("otp_verified"):
        return redirect('forgot_password')

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        email = request.session.get("reset_email")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        try:
            user = Login.objects.get(email=email)

            # save hashed password
            user.password = make_password(new_password)
            user.save()

            request.session.pop('reset_email', None)
            request.session.pop('reset_otp', None)
            request.session.pop('otp_verified', None)

            messages.success(request, "Password reset successful. Please login.")
            return redirect('login2')

        except Login.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')

    return render(request, 'reset_password.html')
