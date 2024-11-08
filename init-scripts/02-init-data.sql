USE steam_games_data_warehouse;

INSERT INTO dim_game (game_id, name, required_age, price, metacritic_score, achievements) VALUES
(1, 'Half-Life 2', 18, 9.99, 96, 100),
(2, 'Portal 2', 12, 19.99, 95, 51),
(3, 'Counter-Strike: Global Offensive', 18, 0.00, 88, 167),
(4, 'Dota 2', 0, 0.00, 90, 45),
(5, 'Team Fortress 2', 12, 0.00, 92, 520),
(6, 'Left 4 Dead 2', 18, 9.99, 89, 73),
(7, 'Grand Theft Auto V', 18, 29.99, 96, 77),
(8, 'The Witcher 3: Wild Hunt', 18, 39.99, 93, 78),
(9, 'Minecraft', 7, 26.99, 93, 113),
(10, 'Red Dead Redemption 2', 18, 59.99, 93, 45);

INSERT INTO dim_platform (windows, mac, linux) VALUES
(1, 1, 1),  -- All platforms
(1, 1, 0),  -- Windows & Mac
(1, 0, 1),  -- Windows & Linux
(1, 0, 0),  -- Windows only
(0, 1, 0);  -- Mac only

INSERT INTO dim_time (release_date, year, month, day) VALUES
('2004-11-16', 2004, 11, 16),
('2011-04-19', 2011, 4, 19),
('2012-08-21', 2012, 8, 21),
('2013-07-09', 2013, 7, 9),
('2007-10-10', 2007, 10, 10),
('2009-11-17', 2009, 11, 17),
('2015-04-14', 2015, 4, 14),
('2015-05-19', 2015, 5, 19),
('2011-11-18', 2011, 11, 18),
('2019-12-05', 2019, 12, 5);

INSERT INTO dim_ownership (estimated_owners_min, estimated_owners_max) VALUES
(20000000, 50000000),
(10000000, 20000000),
(50000000, 100000000),
(100000000, 200000000),
(20000000, 50000000),
(15000000, 20000000),
(10000000, 20000000),
(10000000, 20000000),
(30000000, 50000000),
(5000000, 10000000);

-- Insert game sales facts
INSERT INTO fact_game_sales 
(game_key, platform_key, time_key, ownership_key, recommendations, 
positive_reviews, negative_reviews, average_playtime_forever, peak_ccu) VALUES
(1, 1, 1, 1, 150000, 140000, 10000, 720, 50000),
(2, 1, 2, 2, 200000, 190000, 10000, 600, 45000),
(3, 4, 3, 3, 500000, 450000, 50000, 1200, 1000000),
(4, 1, 4, 4, 1000000, 800000, 200000, 1500, 800000),
(5, 1, 5, 5, 300000, 250000, 50000, 800, 100000),
(6, 4, 6, 6, 250000, 200000, 50000, 500, 80000),
(7, 4, 7, 7, 400000, 350000, 50000, 1000, 200000),
(8, 4, 8, 8, 350000, 330000, 20000, 1200, 150000),
(9, 1, 9, 9, 450000, 400000, 50000, 900, 250000),
(10, 4, 10, 10, 300000, 270000, 30000, 1100, 180000);

-- Add some test data for concurrent transaction testing
INSERT INTO dim_game (game_id, name, required_age, price, metacritic_score, achievements) VALUES
(11, 'Test Game A', 0, 29.99, 85, 50),
(12, 'Test Game B', 0, 19.99, 80, 30),
(13, 'Test Game C', 0, 39.99, 90, 75);

-- Add some data that will be fragmented across nodes
-- These could be used for testing replication and consistency
INSERT INTO dim_game (game_id, name, required_age, price, metacritic_score, achievements) VALUES
(14, 'Node2 Test Game 1', 0, 15.99, 75, 25),
(15, 'Node2 Test Game 2', 0, 25.99, 82, 40),
(16, 'Node3 Test Game 1', 0, 35.99, 88, 60),
(17, 'Node3 Test Game 2', 0, 45.99, 91, 80);
