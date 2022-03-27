from django.shortcuts import render

from . import queries


def index(request):
    headline = queries.headline_post()
    remaining = queries.post_summaries(offset=1)

    return render(
        request=request,
        template_name='index.html',
        context={'headline': headline, 'remaining': remaining},
    )
