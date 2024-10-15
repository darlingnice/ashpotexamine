from django.shortcuts import render
from django.contrib import messages
from .forms import CourseForm,QuestionForm
from exam.models import ScheduledExam
from exam.models import Question
import json
from authentication.views import list_of_exam_shuffled_questions_number
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status 


@api_view(["GET","POST"])
def exam(request,id):
    if request.method == "POST":
        # print(list_of_exam_shuffled_questions_number)
        question_number = int(request.data.get('question_number'))
        # print(question_number)
        question = Question.objects.filter(id=list_of_exam_shuffled_questions_number[question_number]).first()
        
        return Response(data={'question':question.text,"optionA":question.optionA,"optionB":question.optionB,"optionC":question.optionC,"optionD":question.optionD},status=status.HTTP_200_OK)

    record= ScheduledExam.objects.filter(id =id).first()
    return render(request=request,template_name='exam-page.html',content_type='text/html',context={'record':record})


def addCourse(request):
    
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message=f"Course {form.cleaned_data['name']} added successfully")
            form = CourseForm()
            return render(request=request,template_name='course.html',context={"form":form})   
        
        else:            
            messages.success(request=request,message=form.errors) 
            return render(request=request,template_name='course.html',context={"form":form}) 
           
    form = CourseForm()    
    return  render(request=request,template_name='course.html',context={'form':form})




def addQuestion(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message=f"Question added successfully")
            form = QuestionForm()
            return render(request=request,template_name='questions.html',context={"form":form})  
        else:            
            messages.success(request=request,message=form.errors) 
            form = QuestionForm()
            return render(request=request,template_name='questions.html',context={"form":form})     
    form = QuestionForm()  
    return  render(request=request,template_name='questions.html',context={'form':form})