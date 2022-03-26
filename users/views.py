"""
Views for handling common user functions, eg. signing up and authenticating.

These are used in place of the default django.contrib.auth urls & views,
since it allows for more custom behaviors (eg. returning to last page visited
after logging in rather than a static LOGIN_REDIRECT_URL, collecting metrics, etc).
"""
from django.contrib import auth, messages
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm


def login(request):
    # TODO: Logic is the same as signup...
    match request.method:
        case 'GET':
            form = LoginForm()

        case 'POST':
            form = LoginForm(request, data=request.POST)

            if form.is_valid():
                auth.login(request, form.get_user())
                # TODO: Would be nice to try returning them to where they came from
                # if no auth wall on the page
                return redirect('home')

            messages.error(request, 'So close! Please try again')

        case _: raise Http404

    return render(
        request=request,
        template_name='login.html',
        context={'form': form}
    )


def logout(request):
    if request.method != 'GET':
        raise Http404
    
    auth.logout(request)

    # TODO: Would be nice to try returning them to where they came from
    # if no auth wall on the page
    return redirect('home')


def signup(request):
    match request.method:
        case 'GET':
            form = SignupForm()

        case 'POST':
            form = SignupForm(request.POST)

            if form.is_valid():
                user = form.save()
                auth.login(request, user)
                messages.success(request, 'Thanks for signing up!')
                return redirect('home')

            messages.error(request, 'Almost there! Just a few things to fix.')

        case _: raise Http404

    return render(
        request=request,
        template_name='signin.html',
        context={'form': form}
    )
