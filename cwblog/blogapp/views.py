from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime
from blogapp.models import Story, Submission
from django.shortcuts import redirect

def home(request):
    return redirect(main,1)

def main(request, page):

    stories = Story.objects.all().order_by('-date')
    submissions = Submission.objects.all()
    paginator = Paginator(stories, 1)

    try:
        page = page
        #page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        stories = paginator.page(page)
    except (InvalidPage, EmptyPage):
        stories = paginator.page(paginator.num_pages)

    return render(request, 'blogapp/main.html', dict(stories=stories, submissions=submissions))


def post_submission(request, page):

    #page = (int) page

    if request.POST["submission"]== "":
        pass
    else:
        new_submission = Submission() 
        new_submission.text= request.POST["submission"]
        new_submission.story= Story.objects.get(pk=page)
        new_submission.date=  datetime.now()
        new_submission.save()

    stories = Story.objects.all().order_by('-date')
    submissions = Submission.objects.all()

    return redirect(main)
 
    
