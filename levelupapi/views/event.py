# """View module for handling requests about games"""
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Event, Game, Gamer, User_Event
from django.contrib.auth.models import User
from rest_framework.decorators import action

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
        """Handle GET requests to events resource

            Returns:
                Response -- JSON serialized list of events
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.all()

        for event in events:
            event.joined = None

            try:
                User_Event.objects.get(event=event, gamer=gamer)
                event.joined = True
            except User_Event.DoesNotExist:
                event.joined = False


        game = self.request.query_params.get('gameId', None)
        if game is not None:
            events.filter(game__id=game)

        serializer = EventSerializer(
            events, many=True, context={'request': request}
        )
        return Response(serializer.data)


    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):

        if request.method == "POST":
            event = Event.objects.get(pk=pk)

            gamer= Gamer.objects.get(user=request.auth.user)

            try:
                registration = User_Event.objects.get(
                    event=event, gamer=gamer)
                return Response(
                    {'message': 'Gamer already signed up for this event.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )    
            except User_Event.DoesNotExist:
                registration = User_Event()
                registration.event = event
                registration.gamer = gamer
                registration.save()

                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":

            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return Response(
                    {'message': 'Event does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            gamer = Gamer.objects.get(user=request.auth.user)

            try:
                registration = User_Event.objects.get(
                    event=event, gamer=gamer)
                registration.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except User_Event.DoesNotExist:
                return Response(
                    {'message': 'Not currently registered for event.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


        
        
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
        fields = ('id', 'name', 'time', 'date', 'description', 'address', 'game', 'organizer', 'joined')