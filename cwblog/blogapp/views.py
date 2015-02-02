from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone
from blogapp.models import Story, Submission
from django.shortcuts import redirect


def home(request):
    return redirect(main, 1)


def main(request, page):

    stories = Story.objects.all().order_by('-date')
    submissions = Submission.objects.all().order_by('-votes')
    paginator = Paginator(stories, 1)

    try:
        stories = paginator.page(page)
    except (InvalidPage, EmptyPage):
        stories = paginator.page(paginator.num_pages)

    return render(request, 'blogapp/main.html', dict(stories=stories, submissions=submissions))


def post_submission(request, page):

    # page = (int) page

    if request.POST["submission"]== "":
        pass
    else:
        new_submission = Submission() 
        new_submission.text = request.POST["submission"]
        new_submission.story = Story.objects.get(pk=page)
        new_submission.date = timezone.now()
        new_submission.save()

    # stories = Story.objects.all().order_by('-date')
    # submissions = Submission.objects.all()

    return redirect(main, page)


def like_button(request, page, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    submission.votes += 1
    submission.save()
    if submission.votes >= 10:
        add_to_story(submission)
    return redirect(main, page)


def dislike_button(request, page, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    if submission.votes <= 0:
        pass
    else:
        submission.votes -= 1
        submission.save()
    return redirect(main, page)


def add_to_story(submission):
    submission.story.body = submission.story.body + '\n' + submission.text
    submission.story.save()
    submission.delete()
