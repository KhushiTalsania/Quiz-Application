from django.shortcuts import render, redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages

from projects.models import Exam, Participant, Outcome, Question, Result

# Create your views here.

index = 0
submit = False

# quiz page
def quiz(request, exam_id, part_id):
    participantObj = Participant.objects.get(id = part_id)
    examObj = Exam.objects.get(id = exam_id)
    questionObj_list = examObj.question.all()
    que_id_list = []
    global index, submit
    for que in questionObj_list:
        que_id_list.append(que.id)
    if request.method == "POST":
        questionObj = Question.objects.get(id = questionObj_list[index].id)
        outcome = Outcome.objects.get(participant = participantObj, question = questionObj)
        try: 
            outcome.answer = request.POST['answer']
        except:
            outcome.answer = ""
        if outcome.answer == questionObj.answer:
            outcome.mark = 1
        else:
            outcome.mark = 0
        outcome.save()
        if "previous" in request.POST:
            if index > 0:
                index = index - 1
            submit = False
        elif "next" in request.POST:
            submit = False
            if index < len(que_id_list) - 1:
                index = index + 1
                if index == len(que_id_list) - 1:
                    submit = True
        elif "submit" in request.POST:
            index = 0
            submit = False
            return redirect("result", part_id, exam_id) 
    else:
        index = 0
    if index < len(que_id_list):
        question = questionObj_list[index]
    questionObj = Question.objects.get(id = questionObj_list[index].id)
    outcome1, created = Outcome.objects.get_or_create(participant = participantObj, question = questionObj)
    context = {'exam': examObj, 'participant': participantObj , 'que': index+1 , 'question': question, "submit": submit, "outcome": outcome1}
    return render(request, 'profile.html', context)

# this function will redirect to result page and also sends email to user.
def result(request, part_id, exam_id):
    participantObj = Participant.objects.get(id = part_id)
    examObj = Exam.objects.get(id = exam_id)
    resultObj = Outcome.objects.filter(participant = participantObj)
    score = Outcome.objects.filter(participant = participantObj, mark = 1).count()
    result = Result.objects.create(participant = participantObj, exam = examObj, result = score)
    context = {'participant': participantObj, 'exam': examObj, "resultObj": resultObj, "score": score}
    
    subject = 'Your Quiz has been submitted successfully.'
    message_html = render_to_string('email.html', context)
    message = EmailMessage(subject, message_html, settings.EMAIL_HOST_USER, [participantObj.email])
    message.content_subtype = 'html' 
    message.send()
    messages.success(request, 'Result has been sent to your Email Address.')
    return render(request, "result.html", context)