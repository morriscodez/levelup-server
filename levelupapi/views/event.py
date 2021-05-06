# """View module for handling requests about games"""
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Event, Game

class EventView(ViewSet):
    def create(self, request):
        event = Event()
        
        #name description date address gameFK
        event.name = request.data["name"]
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.address = request.data["address"]
        event.game = Game.objects.get(pk=request.data["gameId"])

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        event = Event.objects.get(pk=pk)
        event.name = request.data["name"]
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.address = request.data["address"]
        event.game = Game.objects.get(pk=request.data["gameId"])

        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    