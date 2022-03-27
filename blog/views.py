from django.contrib import messages
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


def new(request):
    # TODO: Okay this is *definitely* a pattern so there must
    # be a standard abstraction for this
    match request.method:
        case 'GET':
            form = PostForm()

        case 'POST':
            form = PostForm(request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, 'Thanks for sharing!')

                return redirect('blog-details', post.id)

            messages.error(request, 'Hmm, something is not quite right..')

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
