from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from blogapp.models import Story, Submission


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

