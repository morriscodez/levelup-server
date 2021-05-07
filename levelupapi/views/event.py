# """View module for handling requests about games"""
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Event, Game, Gamer
from django.contrib.auth.models import User

class EventView(ViewSet):
    def create(self, request):
        event = Event()
        
        #name description date address gameFK
        gamer = Gamer.objects.get(user=request.auth.user)
        event.name = request.data["name"]
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.address = request.data["address"]
        event.game = Game.objects.get(pk=request.data["gameId"])
        event.organizer = gamer
        event.time = request.data["time"]

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk):

        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        organizer = Gamer.objects.get(user=request.auth.user)
        
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.name = request.data["name"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.address = request.data["address"]
        event.organizer = organizer
        game = Game.objects.get(pk=request.data["gameId"])
        event.game = game
        event.save()


    def list(self, request):

        events = Event.objects.all()

        game = self.request.query_params.get('game', None)
        if game is not None:
            events.filter(game__id=game)

        serializer = EventSerializer(
            events, many=True, context={'request': request}
        )
        return Response(serializer.data)


        
        
class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class EventGamerSerializer(serializers.ModelSerializer):
    user = EventUserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'label', 'number_of_players', 'skill_level')

class EventSerializer(serializers.ModelSerializer):
    organizer = EventGamerSerializer(many=False)
    game = GameSerializer(many=False)
    
    class Meta:
        model = Event
        fields = ('id', 'name', 'time', 'date', 'description', 'address', 'game', 'organizer')