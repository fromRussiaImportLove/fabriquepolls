from datetime import datetime

from django.http import Http404
from rest_framework import permissions, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answer, Poll, Question, Variant
from .serializers import (
    AnswerSerializer, PollSerializer, QuestionSerializer, VariantSerializer)


class PollList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollActiveList(APIView):
    def get(self, request, format=None):
        today = datetime.today()
        polls = Poll.objects.exclude(end_date__lt=today)
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)


class PollDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, poll_id):
        try:
            return Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            raise Http404

    def get(self, request, poll_id, format=None):
        poll = self.get_object(poll_id)
        serializer = PollSerializer(poll)
        return Response(serializer.data)

    def put(self, request, poll_id, format=None):
        poll = self.get_object(poll_id)
        serializer = PollSerializer(poll, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, poll_id, format=None):
        poll = self.get_object(poll_id)
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PollQuestions(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, poll_id):
        try:
            return Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            raise Http404

    def get(self, request, poll_id, format=None):
        poll = self.get_object(poll_id)
        questions = poll.questions.filter(poll=poll)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, poll_id, format=None):
        poll = self.get_object(poll_id)
        request.data['poll'] = poll.id
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollAnswer(APIView):
    def get_object(self, poll_id):
        try:
            return Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            raise Http404

    def get(self, request, poll_id, format=None):
        poll = self.get_object(poll_id)
        questions = Question.objects.filter(poll=poll)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, poll_id, format=None):
        poll = self.get_object(poll_id)
        questions = poll.questions.filter(poll=poll)
        questions_id = {q.id for q in questions}

        user_poll_id = request.data.get('user_poll_id')
        answers = request.data.get('answers')
        answers_id = {answer.get('question') for answer in answers}

        if questions_id.difference(answers_id) != set():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for answer in answers:
            question = answer.get('question')
            result = answer.get('answer')
            data_set = {
                'user_poll_id': user_poll_id,
                'question': question,
                'answer': result,
            }
            serializer = AnswerSerializer(data=data_set)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


class QuestionDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, question_id):
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, question_id, format=None):
        question = self.get_object(question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, question_id, format=None):
        question = self.get_object(question_id)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id, format=None):
        question = self.get_object(question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionVariants(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, question_id):
        try:
            question = Question.objects.get(id=question_id)
            if question.type_question == 'open':
                raise ParseError(
                    detail='Open question shoudn\'t have variants.')
            return question
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, question_id, format=None):
        question = self.get_object(question_id)
        variants = question.variants.filter(question=question)
        serializer = VariantSerializer(variants, many=True)
        return Response(serializer.data)

    def post(self, request, question_id, format=None):
        question = self.get_object(question_id)
        text = request.data['text']
        serializer = VariantSerializer(
            data={'question': question.id, 'text': text})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VariantDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, variant_id):
        try:
            return Variant.objects.get(id=variant_id)
        except Variant.DoesNotExist:
            raise Http404

    def get(self, request, variant_id, format=None):
        variant = self.get_object(variant_id)
        serializer = VariantSerializer(variant)
        return Response(serializer.data)

    def put(self, request, variant_id, format=None):
        variant = self.get_object(variant_id)
        serializer = VariantSerializer(variant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, variant_id, format=None):
        variant = self.get_object(variant_id)
        variant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAnswers(APIView):
    def get(self, request, user_poll_id, format=None):
        if Answer.objects.filter(user_poll_id=user_poll_id).count() == 0:
            raise Http404
        user_answers = Answer.objects.filter(user_poll_id=user_poll_id)
        serializer = AnswerSerializer(user_answers, many=True)
        return Response(serializer.data)
