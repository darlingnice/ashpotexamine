from django.contrib import admin
from .models import  Stack,Course, ScheduledExam,  StudentAnswer, Result,Question


admin.site.register(Stack)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
admin.site.register(Course)


class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'start_time', 'end_time', 'duration', 'created_at')
    list_filter = ('course',)
admin.site.register(ScheduledExam)


class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_option', 'exam', 'created_at')
    list_filter = ('exam', 'user')
admin.site.register(StudentAnswer)    


class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'total_questions', 'created_at')
    list_filter = ('exam', 'user')
admin.site.register(Result)

admin.site.register(Question)