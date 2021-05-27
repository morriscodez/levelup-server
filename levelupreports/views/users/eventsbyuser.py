"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Game, Event, events
from levelupreports.views import Connection

def userevent_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory= sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    e.id,
                    e.organizer_id,
                    e.description,
                    e.name,
                    e.date,
                    e.address,
                    e.game_id,
                    e.time,
                    u.id user_id,
                    u.first_name || " " || u.last_name as full_name
                FROM 
                    levelupapi_event e
                JOIN
                    levelupapi_gamer gr ON e.organizer_id = gr.id
                JOIN 
                    auth_user u ON gr.user_id = u.id
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "full_name": "Admina Straytor",
            #         "events": [
            #             {
            #                 "id": 1,
            #                 "title": "Foo",
            #                 "maker": "Bar Games",
            #                 "skill_level": 3,
            #                 "number_of_players": 4,
            #                 "gametype_id": 2
            #                 "attendees": {

            #                           }
            #             },
            #         ]
            #     }
            # }

            events_by_user = {}

            for row in dataset:
                # Create a Game instance and set its properties
                event = Event()
                event.organizer_id = row["organizer_id"]
                event.name = row["name"]
                event.description = row["description"]
                event.address = row["address"]
                event.game_id = row["game_id"]
                event.time = row["time"]
                
                # Store the user's id
                uid = row["user_id"]


                # If the user's id is already a key in the dictionary
                if uid in events_by_user:

                    # Add the current game to the 'events' list for it
                    events_by_user[uid]['events'].append(event)

                else:
                    # Otherwise, create the key and dictionary value
                    events_by_user[uid] = {}
                    events_by_user[uid]["id"] = uid
                    events_by_user[uid]["full_name"] = row["full_name"]
                    events_by_user[uid]["events"] = [event]
                    
        
        # Get only the values from the dictionary and create a list from them
        list_of_users_with_events = events_by_user.values()

        # Specific the Django template and provide data context
        template = 'users/list_with_events.html'
        context = {
            'userevent_list': list_of_users_with_events
        }

        return render(request, template, context)