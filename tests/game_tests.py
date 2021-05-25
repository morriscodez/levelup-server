import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Game_Type

class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """

        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8",
            "email": "steve@stevebrownloee.com",
            "address": "steve@stevebrownlee.com",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        #initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse teh JSON in the response body
        json_response = json.loads(response.contet)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /game_types
        # endpoint for creating game types
        gametype = Game_Type()
        gametype.label = "Board game"
        gametype.save()

    def test_create_game(self):
        """
        Ensure we can create a new game
        """
        # Define game properties
        url = "/games"
        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "title": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token) 

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["maker"], "Milton Bradley")
        self.assertEqual(json_response["skill_level"], 5)
        self.assertEqual(json_response["number_of_players"], 6)
