from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages

from models import UserVote
from forms import UserVoteForm


def vote(request):
    if request.method == "POST":
        form = UserVoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote = UserVote.objects.vote(request.user, vote.vote)
            messages.info(request, "Your mood is %s" % vote.get_vote_display())
    else:
        form = UserVoteForm()
    return HttpResponseRedirect(reverse('dashboard'))
