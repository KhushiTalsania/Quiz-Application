from django.urls import path
from . import views

urlpatterns = [
    path('', views.quizapp, name='quizapp'),
    path('login/', views.loginUser, name="loginUser"),
    path('logout/', views.logoutUser, name="logoutUser"),
    path("registerUser/", views.registerUser, name="registerUser"),
    path('home/', views.home, name='home'),
    path('department/<str:dept_id>/', views.department, name='department'),
    path('create-participant/', views.createParticipant, name='create-participant'),
    path('create-question/<str:dept_id>/', views.createQuestion, name='create-question'),
    path('update-question/<str:dept_id>/<str:exam_id>/<str:que_id>/', views.updateQuestion, name='update-question'),
    path('create-department/', views.createDepartment, name='create-department'),
    path('create-exam/<str:dept_id>/', views.createExam, name='create-exam'),
    path('update-exam/<str:dept_id>/<str:exam_id>/', views.updateExam, name='update-exam'),
    path('delete-exam/<str:dept_id>/<str:exam_id>/', views.deleteExam, name='delete-exam'),
    path('department/<str:dept_id>/<str:exam_id>', views.exam, name='exam'),
    path('email-verification/<str:part_id>/', views.emailVerification, name="email-verification")
]
