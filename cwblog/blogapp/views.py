from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from blogapp.forms import PostForm
from datetime import datetime
from blogapp.models import Story, Submission
from django.shortcuts import redirect



def main(request):

    stories = Story.objects.all().order_by('-date')
    submissions = Submission.objects.all()
    paginator = Paginator(stories, 1)

    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        stories = paginator.page(page)
    except (InvalidPage, EmptyPage):
        stories = paginator.page(paginator.num_pages)

    return render(request, 'blogapp/main.html', dict(stories=stories, submissions=submissions))


def post_submission(request):

    page = request.GET.get('page')
    new_submission = Submission() 
    new_submission.text= request.POST["submission"]
    new_submission.story= Story.objects.get(pk=1)
    new_submission.date=  datetime.now()
    new_submission.save()

    stories = Story.objects.all().order_by('-date')
    submissions = Submission.objects.all()

    return redirect(main)
 
    
