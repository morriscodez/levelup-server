#View module for handling requests about game types
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Game_Type

class GameTypes(ViewSet):
    #levelup game types
    def retrieve(self, request, pk=None):
        #Handle GET request for single game type

        # Returns:
        #   Response -- JSON serialized game type

        try:
            game_type = Game_Type.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        # handle GET for all game types
        # returns serialized list

        gametypes = Game_Type.objects.all()
        serializer = GameTypeSerializer(
            gametypes, many=True, context={'request': request}
        )
        return Response(serializer.data)

class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game_Type
        fields = ('id', 'label')