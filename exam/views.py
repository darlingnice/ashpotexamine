from django.shortcuts import render


def exam(request):
    return render(request=request,template_name='exam-page.html',content_type='text/html',context={})