from django.db import models
from authentication.models import CustomUser
from django.core.exceptions import ValidationError


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField(unique=True,null=False,blank=False)  # The text of the question
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    optionA = models.CharField(max_length=255,null=False,blank=False)  # Option A
    optionB = models.CharField(max_length=255,null=False,blank=False)  # Option B
    optionC = models.CharField(max_length=255,null=False,blank=False)  # Option C
    optionD = models.CharField(max_length=255,null=False,blank=False)  # Option D

    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ],null=False)

    def clean(self):
        if not (self.optionA and self.optionB and self.optionC and self.optionD):
            raise ValidationError("All options must be provided for this question.")
    def __str__(self):
        return f"Question {self.id}. Correct option : {self.correct_option}"    


class ScheduledExam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expiry_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.name} Exam scheduled for {self.user.first_name} {self.user.last_name} with Student ID : {self.user}"


class StudentAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1,null=False,blank=False)
    exam = models.ForeignKey(ScheduledExam, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} :Question no : {self.question.pk} - Selected Option : {self.selected_option}"


class Result(models.Model):
    exam = models.ForeignKey(ScheduledExam, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_id} - {self.exam.course.name} Result"
