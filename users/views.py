"""
Views for handling common user functions, eg. signing up and authenticating.

These are used in place of the default django.contrib.auth urls & views,
since it allows for more custom behaviors (eg. returning to last page visited
after logging in rather than a static LOGIN_REDIRECT_URL, collecting metrics, etc).
"""
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm


def login(request):
    match request.method:
        case 'GET':
            form = LoginForm()

        case 'POST':
            form = LoginForm(request, data=request.POST)

            if form.is_valid():
                auth.login(request, form.get_user())

                if (next_path := request.GET.get('next')):
                    return redirect(next_path)

                return redirect('home')

        case _: raise Http404

    return render(
        request=request,
        template_name='login.html',
        context={'form': form}
    )

@login_required
def logout(request):
    if request.method != 'GET':
        raise Http404
    
    auth.logout(request)

    # TODO: Redirect to last page?
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

        case _: raise Http404

    return render(
        request=request,
        template_name='signin.html',
        context={'form': form}
    )
