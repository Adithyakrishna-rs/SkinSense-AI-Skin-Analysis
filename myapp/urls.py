from django.urls import path
from .import views

urlpatterns = [
     
   path("",views.index,name='index'),
   
   path("login2/",views.login2,name='login2'),

   path("adminhome/",views.adminhome,name='adminhome'),

   path("user/",views.user,name='user'),

   path("register/",views.register,name='register'),

   path("docreg/",views.docreg,name='docreg'),

   path("datatables/",views.datatables,name='datatables'),

   path("doctorlist/",views.doctorlist,name='doctorlist'),

   path("doctorhome/",views.doctorhome,name='doctorhome'),

   path("profiledoc/",views.profiledoc,name='profiledoc'),

   path("profileuser/",views.profileuser,name='profileuser'),

   path("docsearch/",views.docsearch,name='docsearch'),

   path('appointment/<int:doctor_id>/', views.appointment, name='appointment'),

   path("userheader/",views.userheader,name='userheader'),

   path("appointlist/",views.appointlist,name='appointlist'),

   path("userappoint/",views.userappoint,name='userappoint'),

   path("editappoint/<int:appoint_id>/",views.editappoint,name='editappoint'),

   path("appointcancel/<int:appoint_id>/",views.appointcancel,name='appointcancel'),

   path("prescription/<int:appoint_id>/",views.prescription,name='prescription'),

   path("userprescription/<int:appoint_id>/",views.userprescription,name='userprescription'),

   path("editprescription/<int:prescription_id>/<int:appoint_id>/",views.editprescription,name='editprescription'),

   path("deleteprescription/<int:prescription_id>/<int:appoint_id>/",views.deleteprescription,name='deleteprescription'),

   path("payment/<int:appoint_id>/<int:consultation_fee>/",views.payment,name='payment'),

   path("complaint/",views.complaint,name='complaint'),

   path("admincomplaint/",views.admincomplaintview,name='admincomplaint'),

   path("editcomplaint/<int:complaint_id>/",views.editcomplaint,name='editcomplaint'),

   path("deletecomplaint/<int:complaint_id>/",views.deletecomplaint,name='deletecomplaint'),

   path("viewcomplaint/",views.viewcomplaint,name='viewcomplaint'),

   path("complaintreply/<int:complaint_id>/",views.complaintreply,name='complaintreply'),

   path('chat/<int:user_id>/', views.chat, name='chat'),
   
   path('send-message/', views.send_message, name='send_message'),

   path("feedback/<int:doctor_id>/",views.feedback,name='feedback'),

   path("editfeedback/<int:feedback_id>/",views.editfeedback,name='editfeedback'),

   path("deletefeedback/<int:feedback_id>/",views.deletefeedback,name='deletefeedback'),

   path("request_refund/<int:id>/",views.request_refund,name='request_refund'),

   path('adminfeedback/', views.admin_feedback_view, name='adminfeedback'),





   path("predict_skin_disease/", views.predict_skin_disease,name="predict_skin_disease"),
   path("save_disease/<int:appointment_id>/", views.save_disease, name="save_disease"),
   path('recommended-products/', views.recommended_products, name='recommended_products'),
   path('personalized_products/', views.personalized_products, name='personalized_products'),
   # path("chatb/", views.chatb,name="chatb"),  
   # path('chat/', views.chatbot_response, name='chatbot_response'),

   path('videoconference/<int:id>/', views.videoconference, name='videoconference'),
   path('save-appointment-url/<int:id>/', views.save_appointment_url, name='save_appointment_url'),

   path('slot/',views.slotadding,name='slot'),


   path('logout/',views.logout,name='logout'),

   path('doctorapprove/<int:id>/',views.doctorapprove,name='doctorapprove'),

   path('doctorreject/<int:id>/',views.doctorreject,name='doctorreject'),

   path('delete-slot/<int:slot_id>/', views.delete_slot, name='delete_slot'),
   path("forgot-password/", views.forgot_password, name='forgot_password'),
   path("verify-otp/", views.verify_otp, name='verify_otp'),
   path("reset-password/", views.reset_password, name='reset_password'),
   


]