# """View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Game, Game_Type, Gamer, game_type

class Game(ViewSet):

    def create(self, request):

        # gamer = Gamer.objects.get(user=request.auth.user)

        game = Game()
        game.label = request.data["label"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]

        gametype = Game_Type.objects.get(pk=request.data["game_TypeId"])
        game.Game_Type = gametype

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    