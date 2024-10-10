from django.shortcuts import render
from django.contrib import messages
from .forms import CourseForm,QuestionForm

def exam(request):
    return render(request=request,template_name='exam-page.html',content_type='text/html',context={})


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