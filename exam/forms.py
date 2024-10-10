from django import forms
from .models import Course, Question, ScheduledExam, StudentAnswer, Result


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'name':forms.TextInput(attrs={'id':'course-name','name':'course-name',         'placeholder':'Course name'}),
            
            'description':forms.Textarea(attrs={'rows':'20','cols':'100','id':'course-description','name':'course-description'})

        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text','course','optionA','optionB','optionC','optionD','correct_option']

        widgets ={
            'text':forms.Textarea(attrs={'rows':'20','cols':'100','id':'question'})
        }



class ScheduledExamForm(forms.ModelForm):
    class Meta:
        model = ScheduledExam
        fields = ['course', 'user','expiry_date', 'duration']


# class StudentAnswerForm(forms.ModelForm):
#     class Meta:
#         model = StudentAnswer
#         fields = ['user', 'question', 'exam']


# class ResultForm(forms.ModelForm):
#     class Meta:
#         model = Result
#         fields = ['exam', 'user', 'score', 'total_questions']
