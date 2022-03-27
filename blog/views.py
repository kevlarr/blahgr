from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import PostForm
from . import queries


def index(request):
    headline = queries.headline_post()
    remaining = queries.post_summaries(offset=1)

    return render(
        request=request,
        template_name='index.html',
        context={'headline': headline, 'remaining': remaining},
    )


@login_required
def new(request):
    # TODO: Okay this is *definitely* a pattern so there must
    # be a standard pattern or abstraction for this
    match request.method:
        case 'GET':
            form = PostForm()

        case 'POST':
            form = PostForm(request.POST)
            exc = None

            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user

                try:
                    # Should this do `post.validate_unique` prior to saving?
                    # That would add an extra round-trip but would not advance the
                    # id sequence on a violation.
                    post.save()
                    messages.success(request, 'Thanks for sharing!')

                    return redirect('blog-details', post.id)

                except IntegrityError as e:
                    form.errors['title'] = ['You have already used this title']

        case _:
            raise Http404

    return render(
        request=request,
        template_name='new.html',
        context={'form': form},
    )


def details(request, post_id):
    post = queries.post(post_id)

    return render(
        request=request,
        template_name='details.html',
        context={'post': post, 'comments': post.comments},
    )
