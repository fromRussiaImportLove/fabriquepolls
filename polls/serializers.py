from .models import Poll, Question, Answer, Variant
from rest_framework import serializers
from datetime import datetime


class PollSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(initial=datetime.today, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'start_date', 'end_date']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'type_question', 'poll', 'text', 'variants']


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'question', 'text']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user_poll_id', 'question', 'answer']
