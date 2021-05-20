from django.urls import path,include
from .views import *
from django.contrib.auth import views as Auth_Views
urlpatterns = [
    path('',Login,name="login"),
    path('dashboard',UserDashboard,name="dashboard"),
    path('logout',Logout,name="logout"),
    path('delete/<pk>',DeleteQuiz,name="delete"),
    path('Add/Questions/<pk>',AddQuestions,name="addquestions"),
    path('Quiz/Start/<pk>',BeginQuiz,name="startquiz"),
    path('Quiz/end/<pk>',ResultQuiz,name="endquiz"),
    path('Quiz/report/<pk>',detailedreport,name="report"),
    
# User Authentication APIs
    path('login',LoginAPI,name="loginapi"),
    path('signup',SignupAPI,name="signupapi"),
    path('Checkanswer',CheckAnswer,name="answercheck"),

# Password Reset Urls
    path('reset_password',Auth_Views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),
    path('reset/password/Done',Auth_Views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>',Auth_Views.PasswordResetConfirmView.as_view(template_name="password_change_form.html"),name="password_reset_confirm"),
    path('reset/complete',Auth_Views.PasswordResetCompleteView.as_view(template_name="password_complete.html"),name="password_reset_complete"),
]
