"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, Gamer

class Profile(ViewSet):
    """Gamer can see profile information"""

    def list(Self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.filter(registration__gamer=gamer)

        events = EventSerializer(
            events, many=True, context={'request': request}
        )
        gamer = GameSerializer(
            gamer, many=False, context={'request': request}
        )

        profile = {}
        profile["gamer"] = gamer.data
        profile["events"] = events.data

        return Response(profile)

class UserSerializer(serializer.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    