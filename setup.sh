
psql -U postgres -h 127.0.0.1 -f setup\db_setup\db_creation.sql

psql -U postgres -h 127.0.0.1 -d nba -f setup\db_setup\table_creation.sql