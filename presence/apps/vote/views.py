from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from models import UserVote
from forms import UserVoteForm


def vote(request):
    if request.method == "POST":
        form = UserVoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote = UserVote.objects.vote(request.user, vote.vote)
    else:
        form = UserVoteForm()
    return HttpResponseRedirect(reverse('dashboard'))
