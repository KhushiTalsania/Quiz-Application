from django.urls import path
from . import views

urlpatterns = [
     path('result/<str:part_id>/<str:exam_id>', views.result, name='result'),
     path('quiz/<str:exam_id>/<str:part_id>', views.quiz, name="quiz"),
]
