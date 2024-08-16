from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Exists
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import CreateideaFrom
from .models import Event, Idea, IdeaUpvote


class EventDetailView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk = event_id)
        except Event.DoesNotExist:
            return HttpResponse('Event does not exist')

        ideas = event.ideas.all().annotate(
            is_liked = Exists(
                IdeaUpvote.objects.filter(user = request.user, my_idea = OuterRef('pk'))
            )
        )
        context = {
            "event": event,
            "idea_form": CreateideaFrom(),
            "ideas": ideas,
        }

        return render(request, "event_detail.html", context = context)


class CreateEventIdeaView(LoginRequiredMixin, View):
    def post(self, request, event_id):
        try:
            event = Event.objects.get(pk = event_id)
        except Event.DoesNotExist:
            return HttpResponse('Event does not exist')

        form = CreateideaFrom(request.POST)
        if form.is_valid():
            Idea.objects.create(
                owner = request.user,
                my_event = event,
                title = form.cleaned_data['title'],
                overview = form.cleaned_data['overview'],
            )

        return redirect('events:event-detail', event_id = event.id)


class UpvoteIdeaView(LoginRequiredMixin, View):
    def post(self, request, event_id, idea_id):
        try:
            idea = Idea.objects.get(id = idea_id, my_event_id = event_id)
        except Idea.DoesNotExist:
            return HttpResponse("Idea does not exist")

        IdeaUpvote.objects.create(
            my_idea = idea,
            user = request.user
        )

        return redirect("events:event-detail", event_id = event_id)
