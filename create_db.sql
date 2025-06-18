-- Connect to postgres database to create our new database
\c postgres;

-- Create the database
CREATE DATABASE cityshine;

-- Connect to the new database
\c cityshine;

-- Enable PostGIS extension
CREATE EXTENSION postgis;