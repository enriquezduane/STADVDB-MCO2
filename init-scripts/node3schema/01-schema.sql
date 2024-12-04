CREATE DATABASE IF NOT EXISTS games_database;
USE games_database;

DROP TABLE IF EXISTS games;
CREATE TABLE games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    required_age INT,
    price DECIMAL(10, 2),
    metacritic_score INT,
    achievements INT
);

DROP TABLE IF EXISTS games_for_adults;
CREATE TABLE games_for_adults AS
SELECT * FROM games
WHERE required_age >= 18;
