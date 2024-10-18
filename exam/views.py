from django.shortcuts import render
from django.contrib import messages
from .forms import CourseForm,QuestionForm
from exam.models import ScheduledExam,CustomUser,StudentAnswer
from exam.models import Question
import json
from authentication.views import list_of_exam_shuffled_questions_number
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status 

@api_view(["GET","POST"])
def exam(request:Request,id):
    if request.method == "POST":
        question_number = int(request.data.get('question_number'))
        if(len(list_of_exam_shuffled_questions_number)>=1):               
            question = Question.objects.filter(id=list_of_exam_shuffled_questions_number[question_number]).first()
            return Response(data={'question':question.text,"optionA":question.optionA,"optionB":question.optionB,"optionC":question.optionC,"optionD":question.optionD,'correct_option':question.correct_option},status=status.HTTP_200_OK)
        else:
            return Response(data={'message':'You are unauthenticated'},status=status.HTTP_401_UNAUTHORIZED)
    record= ScheduledExam.objects.filter(id =id).first()
    return render(request=request,template_name='exam-page.html',content_type='text/html',context={'record':record})


@api_view(['POST'])
def submitExam(request:Request):
    exam_id = request.data.get('exam_id')
    answers:dict = request.data.get('answers')
    correct_options:dict = request.data.get('correct_options')
    exam = ScheduledExam.objects.filter(id=exam_id).first()
    user = CustomUser.objects.filter(user_id=exam.user).first()
    exam = ScheduledExam.objects.filter(id=int(exam_id)).first()
    try:
        studentAnswers = []
        for (question_number,answer),(_number,correct_option) in zip(answers.items(),correct_options.items()):
            question = Question.objects.filter(id=list_of_exam_shuffled_questions_number[int(question_number)-1]).first()
            studentAnswers.append(StudentAnswer(user=user,course=exam.course,question=question,selected_option=answer,correct_option=correct_option,exam=exam))            
        StudentAnswer.objects.bulk_create(studentAnswers) 
        print("saved")
        return Response(data={'message':"successful"},status=status.HTTP_201_CREATED)   
    except Exception as e: 
        return Response(data={'message':f"{e}"},status=status.HTTP_400_BAD_REQUEST)      
       

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