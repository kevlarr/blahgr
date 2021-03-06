from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from .forms import CommentForm, PostForm
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
            form = PostForm(label_suffix='')

        case 'POST':
            form = PostForm(request.POST, label_suffix='')
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
        template_name='form.html',
        context={'form': form},
    )


def details(request, post_id):
    post = queries.post(post_id)

    comment_form = CommentForm(label_suffix='') if request.user.is_authenticated else None

    return render(
        request=request,
        template_name='details.html',
        context={'post': post, 'comment_form': comment_form},
    )


def edit(request, post_id):
    if request.method not in ('GET', 'POST'):
        raise Http404

    post = queries.post(post_id)

    # This doesn't use `login_required` because it shouldn't redirect,
    # so check if not authenticated
    if not request.user.is_authenticated or request.user.id != post.author.id:
        return HttpResponse('Unauthorized', status=401)

    match request.method:
        case 'GET':
            form = PostForm(instance=post, label_suffix='')

        case 'POST':
            form = PostForm(request.POST, instance=post, label_suffix='')

            if form.is_valid():
                form.save()
                messages.success(request, 'Thanks for sharing!')

                return redirect('blog-details', post.id)

            else:
                # Get rid of the impersonal 'Post with this Author and Title already exists'
                del form.errors['__all__']
                form.errors['title'] = ['You have already used this title']

    return render(
        request=request,
        template_name='form.html',
        context={'form': form},
    )


def delete(request, post_id):
    if request.method != 'POST':
        raise Http404

    post = queries.post(post_id)

    # This doesn't use `login_required` because it shouldn't redirect,
    # so check if not authenticated
    if not request.user.is_authenticated or request.user.id != post.author.id:
        return HttpResponse('Unauthorized', status=401)

    post.delete()

    return redirect('blog-index')


@login_required
def new_comment(request, post_id):
    if request.method != 'POST':
        raise Http404

    post = queries.post(post_id)
    form = CommentForm(request.POST, label_suffix='')

    if not form.is_valid():
        # Best UX for an invalid form? This is a different route than the
        # form is display on, so redirecting will lose error message but rendering
        # the form will then have a different URL
        return render(
            request=request,
            template_name='details.html',
            context={'post': post, 'comment_form': form},
        )

    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    comment.save()

    messages.success(request, 'Thanks for adding to the discussion!')

    return redirect('blog-details', post.id)


def delete_comment(request, comment_id):
    if request.method != 'POST':
        raise Http404

    comment = queries.comment(comment_id)

    if not request.user.is_authenticated or request.user.id != comment.author.id:
        return HttpResponse('Unauthorized', status=401)

    comment.delete()

    return redirect('blog-details', comment.post_id)
