from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout

from blogapp.models import Story, Submission


def home(request):
    return redirect(main, 1)


def main(request, page):

    stories = Story.objects.all().order_by('date')
    submissions = Submission.objects.all().order_by('-votes')
    paginator = Paginator(stories, 1)

    try:
        stories = paginator.page(page)
    except (InvalidPage, EmptyPage):
        stories = paginator.page(paginator.num_pages)

    return render(request, 'blogapp/main.html', dict(stories=stories, submissions=submissions))


@login_required
def post_submission(request, page):
<<<<<<< HEAD
    story_id = request.POST["story_id"]
    if not Submission.objects.filter(story=story_id, author=request.user).exists():
        if request.POST["submission"] == "":
            pass
        else:
            new_submission = Submission()
            new_submission.text = request.POST["submission"]
            new_submission.story = Story.objects.get(pk=story_id)
            new_submission.author = request.user
            new_submission.date = timezone.now()
            new_submission.save()
=======

    if request.POST["submission"]== "" or len(request.POST["submission"])>150:
        pass
    else:
        new_submission = Submission() 
        new_submission.text = request.POST["submission"]
        new_submission.story = Story.objects.get(pk=page)
        new_submission.date = timezone.now()
        new_submission.save()
>>>>>>> 53f9e928140d3c2e393734b86c46b48721b69663

    return redirect(main, page)


@login_required
def like_button(request, page, submission_id):
    if not Submission.objects.filter(voted_on=request.user).filter(pk=submission_id).exists():
        submission = Submission.objects.get(pk=submission_id)
        submission.votes += 1
        submission.voted_on.add(request.user)
        submission.save()
        if submission.votes >= 10:
            add_to_story(submission)
    return redirect(main, page)


@login_required
def dislike_button(request, page, submission_id):
<<<<<<< HEAD
    if not Submission.objects.filter(voted_on=request.user).filter(pk=submission_id).exists():
        submission = Submission.objects.get(pk=submission_id)
        if submission.votes <= -5:
            submission.delete()
        else:
            submission.votes -= 1
            submission.voted_on.add(request.user)
            submission.save()
=======
    submission = Submission.objects.get(pk=submission_id)
    if submission.votes ==-4:
        submissin.delete()
    else:
        submission.votes -= 1
        submission.save()
>>>>>>> 53f9e928140d3c2e393734b86c46b48721b69663
    return redirect(main, page)


def add_to_story(submission):
    submission.story.body = submission.story.body + '\n' + submission.text
    submission.story.save()
    submissions = Submission.objects.all()

    for i in submissions:
        if i== submission:
            pass
        else:
            if i.story== submission.story:
                i.delete()

    submission.delete()

def add_new_story(request):

    if request.POST["story_text"]== "" or len(request.POST["new_story"])>150:
        return redirect(home)

    if request.POST["new_story"]== "" or len(request.POST["new_story"])>100:
        return redirect(home)
    else:
        new_story = Story() 
        new_story.title = request.POST["new_story"]
        new_story.body = request.POST["story_text"]
        new_story.date = timezone.now()
        new_story.save()

    return redirect(main, new_story.pk)


def new_story (request):
     return render(request, 'blogapp/new_story.html')


class RegisterView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'blogapp/register.html'
    success_url = '/login/'


def login_page(request):
    return render(request, 'blogapp/login.html', {})


def try_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            return redirect(home)
        else:
            return HttpResponse("Your account is disabled.")
    else:
        return HttpResponse("Invalid login details supplied.")


@login_required
def try_logout(request):
    logout(request)
    return redirect(home)
