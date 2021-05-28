SELECT * FROM levelupapi_game_type

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer

SELECT * FROM levelupapi_event
SELECT * FROM levelupapi_user_events

UPDATE levelupapi_event
SET name = "Drag Race Extreme"
WHERE id = 6;

CREATE VIEW GAMES_BY_USER AS
SELECT
    g.id,
    g.label,
    g.game_type_id,
    g.number_of_players,
    g.skill_level,
    u.id user_id,
    u.first_name || " " || u.last_name as full_name
FROM 
    levelupapi_game g
JOIN
    levelupapi_gamer gr ON g.gamer_id = gr.id
JOIN 
    auth_user u ON gr.user_id = u.id
;