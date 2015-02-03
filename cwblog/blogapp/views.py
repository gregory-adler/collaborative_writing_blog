from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login

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


def like_button(request, page, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    submission.votes += 1
    submission.save()
    if submission.votes >= 10:
        add_to_story(submission)
    return redirect(main, page)


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
    success_url = '/'


def login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            # print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('blogapp/login.html', {}, context)



def logout(request):

    return redirect(home)
