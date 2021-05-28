"""View module for handling requests about games"""
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Game, Game_Type, Gamer, game_type

class Games(ViewSet):

    permission_classes = [ DjangoModelPermissions ]
    queryset = Game.objects.none()

    
    def create(self, request):

        # gamer = Gamer.objects.get(user=request.auth.user)

        game = Game()
        game.label = request.data["label"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]

        gametype = Game_Type.objects.get(pk=request.data["gameTypeId"])
        game.game_type = gametype

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):

        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        games = Game.objects.all()

        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type__id=game_type)

        serializer = GameSerializer(
            games, many=True, context={'request': request}
        )
        return Response(serializer.data)


    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=pk)

        game.label = request.data['label']
        game.number_of_players = request.data['numberOfPlayers']
        game.skill_level = request.data['skillLevel']
        game.gamer = gamer

        gametype = Game_Type.objects.get(pk=request.data['gameTypeId'])
        game.gametype = gametype
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'label', 'number_of_players', 'skill_level', 'game_type')
        depth = 1

        