from django.urls import path

from events.views import EventDetailView, CreateEventIdeaView

app_name = "events"
urlpatterns = [
    path("<int:event_id>/", EventDetailView.as_view(), name = 'event-detail'),
    path("<int:event_id>/ideas/", CreateEventIdeaView.as_view(), name = 'create-idea'),
]
