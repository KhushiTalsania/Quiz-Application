from django.contrib import admin
from .models import Department, Exam, Question, Outcome, Result, Participant

# Register your models here.
admin.site.register(Department)
admin.site.register(Participant)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Outcome)
admin.site.register(Result)