from django.http import Http404
from django.shortcuts import render

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


def new(request):
    # TODO: Okay this is *definitely* a pattern so there must
    # be a standard abstraction for this
    match request.method:
        case 'GET':
            form = PostForm()

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
