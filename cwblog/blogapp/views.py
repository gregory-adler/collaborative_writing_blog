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

    if request.POST["submission"]== "":
        pass
    else:
        new_submission = Submission() 
        new_submission.text = request.POST["submission"]
        new_submission.story = Story.objects.get(pk=page)
        new_submission.date = timezone.now()
        new_submission.save()

    return redirect(main, page)


@login_required
def like_button(request, page, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    submission.votes += 1
    submission.save()
    if submission.votes >= 10:
        add_to_story(submission)
    return redirect(main, page)


@login_required
def dislike_button(request, page, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    if submission.votes ==-4:
        submissin.delete()
    else:
        submission.votes -= 1
        submission.save()
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
