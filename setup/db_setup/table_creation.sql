
CREATE TABLE IF NOT EXISTS team (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    created_timestamp TIMESTAMP NOT NULL,
    location VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS player (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    created_timestamp TIMESTAMP NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth INT,
    height FLOAT,
    weight INT
);

CREATE TABLE IF NOT EXISTS game (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    created_timestamp TIMESTAMP NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    height FLOAT,
    weight INT
);