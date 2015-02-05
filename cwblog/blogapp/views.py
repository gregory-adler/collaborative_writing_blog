from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from blogapp.models import Story, Submission


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


@login_required
def post_submission(request, page):
    story_id = request.POST["story_id"]
    if not Submission.objects.filter(story=story_id, author=request.user).exists():
        if request.POST["submission"] == "" or len(request.POST["submission"])>150:
            pass
        else:
            new_submission = Submission()
            new_submission.text = request.POST["submission"]
            new_submission.story = Story.objects.get(pk=story_id)
            new_submission.author = request.user
            new_submission.date = timezone.now()
            new_submission.save()

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
    if not Submission.objects.filter(voted_on=request.user).filter(pk=submission_id).exists():
        submission = Submission.objects.get(pk=submission_id)
        if submission.votes <= -4:
            submission.delete()
        else:
            submission.votes -= 1
            submission.voted_on.add(request.user)
            submission.save()
    return redirect(main, page)

@login_required
def add_to_story(submission):
    submission.story.body = submission.story.body + '\n' + submission.text
    submission.story.save()
    submissions = Submission.objects.filter(story=submission.story)
    for i in submissions:
        i.delete()

@login_required
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


def new_story(request):
    return render(request, 'blogapp/new_story.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST.get('username'),
                                    password=request.POST.get('password1'))
            login(request, new_user)
            return redirect(home)
    else:
        form = UserCreationForm()
    return render(request, 'blogapp/register.html', dict(form=form))


def try_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(home)
            else:
                messages.error(request, "Your account has been disabled.")
                return render(request, 'blogapp/login.html', dict(messages=messages.get_messages(request)))
        else:
            messages.error(request, "Incorrect username/password combination.")
            return render(request, 'blogapp/login.html', dict(messages=messages.get_messages(request)))
    else:
        return render(request, 'blogapp/login.html')


@login_required()
def try_logout(request):
    logout(request)
    return redirect(home)
