from django.db import models
from authentication.models import CustomUser
from django.core.exceptions import ValidationError



class Stack(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255,unique=True)
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE, related_name='courses')  # Relationship to Stack
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MC', 'Multiple Choice'),  # For multiple-choice questions
        ('TF', 'True/False'),       # For true/false questions
    ]
    
    text = models.TextField()  # The text of the question
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)

    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES)  # Type of question

    # Multiple choice fields
    optionA = models.CharField(max_length=255, blank=True, null=True)  # Option A
    optionB = models.CharField(max_length=255, blank=True, null=True)  # Option B
    optionC = models.CharField(max_length=255, blank=True, null=True)  # Option C
    optionD = models.CharField(max_length=255, blank=True, null=True)  # Option D

    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
        ('T', 'True'),
        ('F', 'False'),
    ])  # Indicates the correct option

    def __str__(self):
        return self.text

    def clean(self):
        # Custom validation logic
        if self.question_type == 'MC':
            # Ensure all options are provided for multiple-choice questions
            if not (self.optionA and self.optionB and self.optionC and self.optionD):
                raise ValidationError("All options must be provided for multiple choice questions.")
            # Ensure the correct option is among A, B, C, D
            if self.correct_option not in ['A', 'B', 'C', 'D']:
                raise ValidationError("Correct option must be one of A, B, or C, or D. not True or False")

        elif self.question_type == 'TF':
            # Ensure options are not set for true/false questions
            if self.optionA or self.optionB or self.optionC or self.optionD:
                raise ValidationError("Options must not be set for True/False questions.")
            # Correct option must be either 'T' or 'F'
            if self.correct_option not in ['T', 'F']:
                raise ValidationError("Correct option must be either 'True' or 'False'.")

            
       
       

class ScheduledExam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField()  # Duration in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.name} Exam"


class StudentAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    exam = models.ForeignKey(ScheduledExam, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"


class Result(models.Model):
    exam = models.ForeignKey(ScheduledExam, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.course.name} Result"
