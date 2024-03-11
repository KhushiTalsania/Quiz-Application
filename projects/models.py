from django.db import models
import uuid
from django.db.models.signals import post_save, post_delete

# Create your models here.
    
class Department(models.Model):
    id = models.IntegerField(primary_key = True, auto_created = True)
    name = models.CharField(max_length = 300)

    def __str__(self):
        return self.name
    
class Exam(models.Model):
    id = models.IntegerField(primary_key = True, auto_created = True)
    name = models.ForeignKey(Department, on_delete = models.CASCADE)
    question = models.ManyToManyField('Question', blank=True)
    code = models.CharField(max_length = 6, unique=True, default=None)

    def __str__(self):
        return self.name.name
    
class Question(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    question = models.TextField(unique = True)
    options = models.JSONField(null = False, blank= True, default=dict)
    answer = models.CharField(max_length = 100)

    def __str__(self):
        return self.question
    
class Participant(models.Model):
    choice = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 200)
    # department = models.ForeignKey(Department, on_delete = models.CASCADE)
    code = models.CharField(max_length = 6, default = 0, null = True, blank = True)
    gender = models.CharField(max_length = 20, choices = choice, default = None, null=True, blank = True)
    email = models.EmailField(max_length = 100)
    mobile = models.BigIntegerField(null = True, blank = True)
    address = models.TextField(max_length = 300, null = True, blank = True)
    experience = models.IntegerField(default=0, null = True, blank = True)

    def __str__(self):
        return self.name
   
class Result(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete = models.CASCADE)
    result = models.IntegerField(blank = True, default = 0)

    class Meta:
        unique_together = [['participant', 'exam']]

    def __str__(self):
        return self.participant.name

class Outcome(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 100, default = 0)
    mark = models.IntegerField(blank = True, default = 0)

    def __str__(self):
        return self.participant.name

def examUpdated(sender, instance, created, **kwargs):
    if created:
        print('Exam Created !!')
    else:
        print('Exam Updated !!')

def examDeleted(sender, instance, **kwargs):
    print("Exam Deleted !!")

post_save.connect(examUpdated, sender=Exam)
post_delete.connect(examDeleted, sender=Exam)

