/*

This script creates the data and the necessary tables
for the basketball_scraping project.

*/

CREATE DATABASE nba;

CREATE TABLE IF NOT EXISTS nba.team (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    created_timestamp TIMESTAMP NOT NULL,
    location VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS nba.player (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    created_timestamp TIMESTAMP NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth INT,
    height FLOAT,
    weight INT
);

CREATE TABLE IF NOT EXISTS nba.game (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    created_timestamp TIMESTAMP NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    height FLOAT,
    weight INT
);