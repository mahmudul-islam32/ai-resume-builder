-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS ai_resume;

-- Use the database
\c ai_resume;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
