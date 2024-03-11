from rest_framework import serializers
from projects.models import Participant, Result, Exam, Question, Outcome

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many = True)
    class Meta:
        model = Exam
        fields = '__all__'

class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(many = False)
    exam = ExamSerializer(many = False)

    class Meta:
        model = Result
        fields = '__all__'