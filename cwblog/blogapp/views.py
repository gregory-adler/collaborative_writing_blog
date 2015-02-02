from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone
from blogapp.models import Story, Submission
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


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


class Register(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'blogapp/register.html'
    success_url = '/'


# class Login(AuthenticationForm):
#
#     def form_valid(self, form):
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user = authenticate(username=username, password=password)
#
#         if user is not None and user.is_active:
#             login(self.request, user)
#             return super(Register, self).form_valid(form)
#         else:
#             return self.form_invalid(form)


def login_page(request):

   return render(request, 'blogapp/login.html', dict())


def register_user(request):

    return HttpResponseForbidden()

def logout(request):

    return redirect(home)
