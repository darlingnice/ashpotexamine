from django.contrib import admin
from .models import Course, Exam, Question, Option, StudentAnswer, Result

admin.site.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

admin.site.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'start_time', 'end_time', 'duration', 'created_at')
    list_filter = ('course',)

admin.site.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'course', 'question_type', 'created_at')
    list_filter = ('course', 'question_type')
    search_fields = ('text',)

admin.site.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    list_filter = ('question', 'is_correct')

admin.site.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_option', 'exam', 'created_at')
    list_filter = ('exam', 'user')

admin.site.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'total_questions', 'created_at')
    list_filter = ('exam', 'user')
