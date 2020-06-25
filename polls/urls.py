from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from polls import views

urlpatterns = [
    path('polls/', views.PollList.as_view()),
    path('polls/<int:poll_id>/', views.PollDetail.as_view()),
    path('polls/<int:poll_id>/questions/', views.PollQuestions.as_view()),
    path('questions/<int:question_id>/', views.QuestionDetail.as_view()),
    path('questions/<int:question_id>/variants/',
         views.QuestionVariants.as_view()),
    path('variants/<int:variant_id>/', views.VariantDetail.as_view()),
    path('user-answers/<int:user_poll_id>/', views.UserAnswers.as_view()),
    path('user-answers/active-polls/',
         views.PollActiveList.as_view()),
    path('user-answers/active-polls/<int:poll_id>/',
         views.PollAnswer.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
