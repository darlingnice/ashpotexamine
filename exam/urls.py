from django.urls import path
from . import views


urlpatterns =[
    path('take/<int:id>', views.exam, name='exam'),
    path('course/',views.addCourse,name="add_course"),
    path('question/',views.addQuestion,name="add_question"),
    path('submit/',views.submitExam,name="submitExam"),
]